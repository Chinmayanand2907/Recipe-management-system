from flask import Flask, render_template, request, redirect, url_for, flash, abort, session
from flask_bootstrap import Bootstrap
from forms import RecipeForm, IngredientForm, SearchForm, LoginForm, RegistrationForm
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import mysql_db as db
from dotenv import load_dotenv
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'development-key')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}
Bootstrap(app)

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Add context processor for current date
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Add user context processor
@app.context_processor
def inject_user():
    user = None
    if 'user_id' in session:
        # Get user info from db
        user = {'username': session.get('username')}
    return {'user': user}

# Add custom Jinja2 filter for date formatting
@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    if not date:
        return ''
    # Convert string to datetime if needed
    if isinstance(date, str):
        try:
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return date  # Return the original string if parsing fails
    
    if fmt:
        return date.strftime(fmt)
    return date.strftime('%Y-%m-%d')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    # Get latest recipes (limited to 6)
    latest_recipes = db.get_latest_recipes(6)
    # Get recipe categories
    categories = db.get_all_categories()
    # Prepare search form
    search_form = SearchForm()
    return render_template('index.html', 
                          latest_recipes=latest_recipes, 
                          categories=categories,
                          search_form=search_form)

@app.route('/recipes')
def recipes():
    # Get category filter if exists
    category_id = request.args.get('category', None)
    
    if category_id:
        # Get recipes by category
        recipes_list = db.get_recipes_by_category(category_id)
        category_name = db.get_category_name(category_id)
        title = f"Recipes in {category_name}"
    else:
        # Get all recipes
        recipes_list = db.get_all_recipes()
        title = "All Recipes"
    
    # Get all categories for sidebar
    categories = db.get_all_categories()
    search_form = SearchForm()
    
    return render_template('recipes.html', 
                          recipes=recipes_list, 
                          categories=categories,
                          title=title,
                          search_form=search_form)

@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    # Get detailed recipe information
    recipe = db.get_recipe_details(recipe_id)
    
    if not recipe:
        abort(404)
    
    search_form = SearchForm()
    return render_template('recipe_detail.html', 
                          recipe=recipe,
                          search_form=search_form)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    
    if not query:
        return redirect(url_for('recipes'))
    
    # Search for recipes
    recipes_list = db.search_recipes(query)
    categories = db.get_all_categories()
    search_form = SearchForm(query=query)
    
    return render_template('recipes.html', 
                          recipes=recipes_list, 
                          categories=categories,
                          title=f"Search results for '{query}'",
                          search_form=search_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = db.authenticate_user(form.username.data, form.password.data)
        
        if user:
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            flash(f'Welcome back, {user["username"]}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')
    
    return render_template('login.html', form=form, search_form=SearchForm())

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        # Register new user
        user = db.register_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        
        if user:
            # Automatically log in the user
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            
            flash(f'Account created successfully! Welcome, {user["username"]}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Registration failed. Please try again.', 'danger')
    
    return render_template('register.html', form=form, search_form=SearchForm())

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/add_recipe', methods=['GET', 'POST'])
@app.route('/add_recipe/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def add_recipe(recipe_id=None):
    form = RecipeForm()
    edit_mode = recipe_id is not None
    existing_recipe = None
    
    # Populate category choices
    categories = db.get_all_categories()
    form.category_id.choices = [(c['category_id'], c['name']) for c in categories]
    
    # If editing an existing recipe, populate the form with existing data
    if edit_mode and request.method == 'GET':
        existing_recipe = db.get_recipe_details(recipe_id)
        if existing_recipe:
            form.title.data = existing_recipe['title']
            form.description.data = existing_recipe['description']
            form.prep_time.data = existing_recipe['prep_time']
            form.cook_time.data = existing_recipe['cook_time']
            form.servings.data = existing_recipe['servings']
            form.difficulty.data = existing_recipe['difficulty']
            form.category_id.data = existing_recipe['category_id']
            
            # Populate ingredients
            ingredients_text = ""
            for ingredient in existing_recipe['ingredients']:
                ingredient_str = ""
                if 'notes' in ingredient and ingredient['notes']:
                    ingredient_str = ingredient['notes']
                else:
                    # Format ingredient with quantity and unit if available
                    if 'quantity' in ingredient and ingredient['quantity']:
                        ingredient_str += str(ingredient['quantity']) + " "
                    if 'unit' in ingredient and ingredient['unit']:
                        ingredient_str += ingredient['unit'] + " "
                    if 'ingredient' in ingredient:
                        ingredient_str += ingredient['ingredient']
                
                if ingredient_str:
                    ingredients_text += f"{ingredient_str}\n"
            
            form.ingredients.data = ingredients_text.strip()
            
            # Populate instructions
            instructions_text = ""
            for step in existing_recipe['steps']:
                if 'instruction' in step:
                    instructions_text += f"{step['instruction']}\n"
            
            form.instructions.data = instructions_text.strip()
            
            if existing_recipe.get('notes'):
                form.notes.data = existing_recipe['notes']
    
    if form.validate_on_submit():
        # Handle image upload if provided
        image_path = None
        if form.image.data:
            file = form.image.data
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f"{timestamp}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                image_path = f"uploads/{filename}"
        elif edit_mode and existing_recipe and 'image_url' in existing_recipe:
            # Keep existing image if no new image is uploaded
            image_path = existing_recipe['image_url']
        
        # Create recipe data
        recipe_data = {
            'title': form.title.data,
            'description': form.description.data,
            'prep_time': form.prep_time.data,
            'cook_time': form.cook_time.data,
            'servings': form.servings.data,
            'difficulty': form.difficulty.data,
            'user_id': session['user_id'],  # Use the logged-in user's ID
            'category_id': form.category_id.data,
            'image_url': image_path,
            'notes': form.notes.data if hasattr(form, 'notes') else None
        }
        
        # Parse ingredients
        ingredients = []
        for ingredient_line in form.ingredients.data.split('\n'):
            if ingredient_line.strip():
                ingredients.append(ingredient_line.strip())
        
        # Parse steps
        steps = []
        for step in form.instructions.data.split('\n'):
            if step.strip():
                steps.append(step.strip())
        
        # Add or update recipe in database
        if edit_mode:
            # Verify this recipe belongs to current user
            if existing_recipe and existing_recipe['user_id'] != session['user_id']:
                flash('You do not have permission to edit this recipe.', 'danger')
                return redirect(url_for('recipes'))
                
            success = db.update_recipe(
                recipe_id,
                recipe_data,
                ingredients,
                steps
            )
            flash_message = 'Recipe updated successfully!' if success else 'Error updating recipe. Please try again.'
        else:
            new_recipe_id = db.add_recipe(
                recipe_data['title'],
                recipe_data['description'],
                recipe_data['prep_time'],
                recipe_data['cook_time'],
                recipe_data['servings'],
                recipe_data['difficulty'],
                recipe_data['user_id'],
                recipe_data['category_id'],
                recipe_data['image_url'],
                ingredients,
                steps,
                recipe_data['notes']
            )
            success = new_recipe_id is not None
            recipe_id = new_recipe_id if success else None
            flash_message = 'Recipe added successfully!' if success else 'Error adding recipe. Please try again.'
        
        if success:
            flash(flash_message, 'success')
            return redirect(url_for('recipe_detail', recipe_id=recipe_id))
        else:
            flash(flash_message, 'danger')
    
    # Get ingredients for the form
    all_ingredients = db.get_all_ingredients()
    
    search_form = SearchForm()
    return render_template('recipe_form.html', 
                          form=form, 
                          ingredients=all_ingredients,
                          edit_mode=edit_mode,
                          search_form=search_form)

@app.route('/ingredients')
def ingredients():
    all_ingredients = db.get_all_ingredients()
    search_form = SearchForm()
    return render_template('ingredients.html', 
                          ingredients=all_ingredients,
                          search_form=search_form)

@app.route('/add_ingredient', methods=['GET', 'POST'])
@login_required
def add_ingredient():
    form = IngredientForm()
    if form.validate_on_submit():
        result = db.add_ingredient(
            form.name.data,
            form.description.data,
            form.is_allergen.data
        )
        
        if result:
            flash('Ingredient added successfully!', 'success')
            return redirect(url_for('ingredients'))
        else:
            flash('Error adding ingredient. Please try again.', 'danger')
    
    search_form = SearchForm()
    return render_template('add_ingredient.html', 
                          form=form,
                          search_form=search_form)

@app.route('/delete_recipe/<int:recipe_id>', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    # Check if the recipe belongs to the current user
    recipe = db.get_recipe_details(recipe_id)
    
    if not recipe:
        flash('Recipe not found.', 'danger')
        return redirect(url_for('recipes'))
        
    if recipe['user_id'] != session['user_id']:
        flash('You do not have permission to delete this recipe.', 'danger')
        return redirect(url_for('recipes'))
        
    if db.delete_recipe(recipe_id):
        flash('Recipe deleted successfully!', 'success')
    else:
        flash('Error deleting recipe.', 'danger')
    
    return redirect(url_for('recipes'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', search_form=SearchForm()), 404

if __name__ == '__main__':
    # Initialize the database if it doesn't exist
    db.initialize_database()
    app.run(debug=True) 