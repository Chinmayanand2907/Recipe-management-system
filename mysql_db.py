import mysql.connector
import os
from datetime import datetime
import hashlib

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Change to your MySQL username
    'password': 'chinmay@182907',  # Change to your MySQL password
    'database': 'recipe_management'
}

def get_connection():
    """Get a connection to the MySQL database"""
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

def dict_cursor(conn):
    """Create a cursor that returns results as dictionaries"""
    cursor = conn.cursor(dictionary=True)
    return cursor

def initialize_database():
    """Create the database and initialize tables if they don't exist"""
    # First, try connecting to MySQL server without specifying a database
    try:
        config_without_db = DB_CONFIG.copy()
        del config_without_db['database']
        conn = mysql.connector.connect(**config_without_db)
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.execute(f"USE {DB_CONFIG['database']}")
        
        # Create tables manually instead of using the schema file
        try:
            # Drop tables if they exist
            cursor.execute("DROP TABLE IF EXISTS recipe_ingredients")
            cursor.execute("DROP TABLE IF EXISTS recipe_steps")
            cursor.execute("DROP TABLE IF EXISTS recipes")
            cursor.execute("DROP TABLE IF EXISTS ingredients") 
            cursor.execute("DROP TABLE IF EXISTS categories")
            cursor.execute("DROP TABLE IF EXISTS units")
            cursor.execute("DROP TABLE IF EXISTS users")
            
            # Create users table
            cursor.execute("""
            CREATE TABLE users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                email VARCHAR(100) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # Create categories table
            cursor.execute("""
            CREATE TABLE categories (
                category_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) NOT NULL UNIQUE,
                description TEXT
            )
            """)
            
            # Create units table
            cursor.execute("""
            CREATE TABLE units (
                unit_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(20) NOT NULL UNIQUE,
                abbreviation VARCHAR(10)
            )
            """)
            
            # Create ingredients table
            cursor.execute("""
            CREATE TABLE ingredients (
                ingredient_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE,
                description TEXT,
                is_allergen BOOLEAN DEFAULT FALSE
            )
            """)
            
            # Create recipes table
            cursor.execute("""
            CREATE TABLE recipes (
                recipe_id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                description TEXT,
                prep_time INT,
                cook_time INT,
                servings INT,
                difficulty VARCHAR(20) CHECK (difficulty IN ('Easy', 'Medium', 'Hard')),
                image_url VARCHAR(255),
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
                user_id INT NOT NULL,
                category_id INT,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (category_id) REFERENCES categories(category_id)
            )
            """)
            
            # Create recipe_ingredients junction table
            cursor.execute("""
            CREATE TABLE recipe_ingredients (
                recipe_id INT,
                ingredient_id INT,
                quantity DECIMAL(10,2) NOT NULL,
                unit_id INT,
                notes TEXT,
                PRIMARY KEY (recipe_id, ingredient_id),
                FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE,
                FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id),
                FOREIGN KEY (unit_id) REFERENCES units(unit_id)
            )
            """)
            
            # Create recipe_steps table
            cursor.execute("""
            CREATE TABLE recipe_steps (
                step_id INT AUTO_INCREMENT PRIMARY KEY,
                recipe_id INT,
                step_number INT NOT NULL,
                instruction TEXT NOT NULL,
                FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE
            )
            """)
            
            # Insert sample users
            cursor.execute("""
            INSERT INTO users (username, email, password_hash) VALUES 
            ('john_doe', 'john@example.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'),
            ('jane_smith', 'jane@example.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8')
            """)
            
            # Insert sample categories
            cursor.execute("""
            INSERT INTO categories (name, description) VALUES
            ('Breakfast', 'Morning meals to start your day'),
            ('Lunch', 'Midday meals'),
            ('Dinner', 'Evening meals'),
            ('Dessert', 'Sweet treats to enjoy'),
            ('Vegetarian', 'Meals without meat'),
            ('Vegan', 'Plant-based meals without animal products')
            """)
            
            # Insert sample units
            cursor.execute("""
            INSERT INTO units (name, abbreviation) VALUES
            ('Gram', 'g'),
            ('Kilogram', 'kg'),
            ('Milliliter', 'ml'),
            ('Liter', 'L'),
            ('Teaspoon', 'tsp'),
            ('Tablespoon', 'tbsp'),
            ('Cup', 'cup'),
            ('Piece', 'pc')
            """)
            
            # Insert sample ingredients
            cursor.execute("""
            INSERT INTO ingredients (name, description, is_allergen) VALUES
            ('Chicken', 'Boneless chicken meat', FALSE),
            ('Flour', 'All-purpose wheat flour', TRUE),
            ('Salt', 'Table salt', FALSE),
            ('Sugar', 'White granulated sugar', FALSE),
            ('Egg', 'Chicken eggs', TRUE),
            ('Milk', 'Cow milk', TRUE),
            ('Tomato', 'Fresh red tomatoes', FALSE),
            ('Onion', 'Yellow onions', FALSE),
            ('Garlic', 'Garlic cloves', FALSE),
            ('Olive Oil', 'Extra virgin olive oil', FALSE),
            ('Baking Powder', 'Leavening agent for baking', FALSE)
            """)
            
            # Insert sample recipes
            cursor.execute("""
            INSERT INTO recipes (title, description, prep_time, cook_time, servings, difficulty, user_id, category_id) VALUES
            ('Classic Pancakes', 'Fluffy breakfast pancakes that everyone will love', 15, 20, 4, 'Easy', 1, 1),
            ('Chicken Stir Fry', 'Quick and healthy dinner option', 20, 15, 2, 'Medium', 2, 3)
            """)
            
            # Insert sample recipe ingredients
            cursor.execute("""
            INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit_id, notes) VALUES
            (1, 2, 2, 7, 'Sifted'),
            (1, 4, 2, 5, NULL),
            (1, 5, 2, 8, 'Beaten'),
            (1, 6, 1.5, 7, NULL),
            (1, 3, 0.5, 5, NULL),
            (1, 11, 1, 5, NULL),
            (2, 1, 500, 1, 'Sliced'),
            (2, 7, 2, 8, 'Diced'),
            (2, 8, 1, 8, 'Sliced'),
            (2, 9, 3, 8, 'Minced')
            """)
            
            # Insert recipe steps one by one to avoid any issues with quotes or special characters
            cursor.execute("INSERT INTO recipe_steps (recipe_id, step_number, instruction) VALUES (1, 1, 'In a large bowl, sift together the flour, baking powder, salt and sugar.')")
            cursor.execute("INSERT INTO recipe_steps (recipe_id, step_number, instruction) VALUES (1, 2, 'Make a well in the center and pour in the milk, egg and melted butter; mix until smooth.')")
            cursor.execute("INSERT INTO recipe_steps (recipe_id, step_number, instruction) VALUES (1, 3, 'Heat a lightly oiled griddle or frying pan over medium-high heat.')")
            cursor.execute("INSERT INTO recipe_steps (recipe_id, step_number, instruction) VALUES (1, 4, 'Pour or scoop the batter onto the griddle, using approximately 1/4 cup for each pancake.')")
            cursor.execute("INSERT INTO recipe_steps (recipe_id, step_number, instruction) VALUES (1, 5, 'Cook until bubbles form and the edges are dry, then flip and cook until browned on the other side.')")
            cursor.execute("INSERT INTO recipe_steps (recipe_id, step_number, instruction) VALUES (2, 1, 'Slice the chicken into thin strips.')")
            cursor.execute("INSERT INTO recipe_steps (recipe_id, step_number, instruction) VALUES (2, 2, 'Heat oil in a wok or large skillet over high heat.')")
            cursor.execute("INSERT INTO recipe_steps (recipe_id, step_number, instruction) VALUES (2, 3, 'Add chicken and stir-fry for 5-6 minutes until no longer pink.')")
            cursor.execute("INSERT INTO recipe_steps (recipe_id, step_number, instruction) VALUES (2, 4, 'Add garlic and onions, stir-fry for 1 minute.')")
            cursor.execute("INSERT INTO recipe_steps (recipe_id, step_number, instruction) VALUES (2, 5, 'Add tomatoes and other vegetables, stir-fry for 2-3 minutes.')")
            cursor.execute("INSERT INTO recipe_steps (recipe_id, step_number, instruction) VALUES (2, 6, 'Season with soy sauce and serve hot with rice.')")
            
            conn.commit()
            print(f"Database {DB_CONFIG['database']} initialized successfully.")
            
        except mysql.connector.Error as err:
            print(f"Error creating tables: {err}")
            conn.rollback()
        
        conn.close()
        
        # Create placeholder images
        create_placeholder_images()
    except mysql.connector.Error as err:
        print(f"Error initializing database: {err}")

def create_placeholder_images():
    """Create placeholder images for sample recipes"""
    # Check if the uploads directory exists
    uploads_dir = "static/uploads"
    os.makedirs(uploads_dir, exist_ok=True)
    
    # Create placeholder images with basic colors
    placeholder_files = [
        (os.path.join(uploads_dir, "placeholder_pancakes.jpg"), (245, 222, 179)),  # wheat color for pancakes
        (os.path.join(uploads_dir, "placeholder_stirfry.jpg"), (144, 238, 144))   # light green for stir fry
    ]
    
    try:
        from PIL import Image
        
        for file_path, color in placeholder_files:
            if not os.path.exists(file_path):
                # Create a 400x300 image with the given color
                img = Image.new('RGB', (400, 300), color)
                img.save(file_path)
        
        # Update the image URLs in the database
        conn = get_connection()
        cursor = dict_cursor(conn)
        cursor.execute("UPDATE recipes SET image_url = %s WHERE recipe_id = %s", ('uploads/placeholder_pancakes.jpg', 1))
        cursor.execute("UPDATE recipes SET image_url = %s WHERE recipe_id = %s", ('uploads/placeholder_stirfry.jpg', 2))
        conn.commit()
        conn.close()
        
        print("Placeholder images created successfully.")
    except ImportError:
        print("PIL (Pillow) library not installed. Placeholder images not created.")
        print("You can install it with: pip install Pillow")
        
        # Create empty files as fallback
        for file_path, _ in placeholder_files:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    f.write('')

def get_all_recipes():
    """Get all recipes with basic information"""
    conn = get_connection()
    cursor = dict_cursor(conn)
    
    query = """
    SELECT r.recipe_id, r.title, r.description, r.prep_time, r.cook_time, 
           r.difficulty, r.servings, r.notes, r.created_at, r.image_url, 
           c.category_id, c.name as category, u.username as author, r.user_id
    FROM recipes r
    LEFT JOIN categories c ON r.category_id = c.category_id
    LEFT JOIN users u ON r.user_id = u.user_id
    ORDER BY r.created_at DESC
    """
    
    cursor.execute(query)
    recipes = cursor.fetchall()
    
    # Process recipes to ensure all fields have valid values
    processed_recipes = []
    for recipe in recipes:
        # Add defaults for any missing fields
        recipe['prep_time'] = recipe.get('prep_time', 0) or 0
        recipe['cook_time'] = recipe.get('cook_time', 0) or 0
        recipe['category'] = recipe.get('category', 'Uncategorized')
        recipe['category_id'] = recipe.get('category_id', 1)
        recipe['difficulty'] = recipe.get('difficulty', 'Medium')
        recipe['title'] = recipe.get('title', 'Untitled Recipe')
        recipe['description'] = recipe.get('description', 'No description available')
        processed_recipes.append(recipe)
    
    conn.close()
    return processed_recipes

def get_latest_recipes(limit=6):
    """Get the most recent recipes"""
    conn = get_connection()
    cursor = dict_cursor(conn)
    
    query = """
    SELECT r.recipe_id, r.title, r.description, r.prep_time, r.cook_time, 
           r.difficulty, r.servings, r.notes, r.created_at, r.image_url, 
           c.category_id, c.name as category, u.username as author, r.user_id
    FROM recipes r
    LEFT JOIN categories c ON r.category_id = c.category_id
    LEFT JOIN users u ON r.user_id = u.user_id
    ORDER BY r.created_at DESC
    LIMIT %s
    """
    
    cursor.execute(query, (limit,))
    recipes = cursor.fetchall()
    
    # Process recipes to ensure all fields have valid values
    processed_recipes = []
    for recipe in recipes:
        # Add defaults for any missing fields
        recipe['prep_time'] = recipe.get('prep_time', 0) or 0
        recipe['cook_time'] = recipe.get('cook_time', 0) or 0
        recipe['category'] = recipe.get('category', 'Uncategorized')
        recipe['category_id'] = recipe.get('category_id', 1)
        recipe['difficulty'] = recipe.get('difficulty', 'Medium')
        recipe['title'] = recipe.get('title', 'Untitled Recipe')
        recipe['description'] = recipe.get('description', 'No description available')
        processed_recipes.append(recipe)
    
    conn.close()
    return processed_recipes

def get_recipes_by_category(category_id):
    """Get recipes by category"""
    conn = get_connection()
    cursor = dict_cursor(conn)
    
    query = """
    SELECT r.recipe_id, r.title, r.description, r.prep_time, r.cook_time, 
           r.difficulty, r.servings, r.notes, r.created_at, r.image_url, 
           c.category_id, c.name as category, u.username as author, r.user_id
    FROM recipes r
    JOIN categories c ON r.category_id = c.category_id
    LEFT JOIN users u ON r.user_id = u.user_id
    WHERE r.category_id = %s
    ORDER BY r.created_at DESC
    """
    
    cursor.execute(query, (category_id,))
    recipes = cursor.fetchall()
    
    # Process recipes to ensure all fields have valid values
    processed_recipes = []
    for recipe in recipes:
        # Add defaults for any missing fields
        recipe['prep_time'] = recipe.get('prep_time', 0) or 0
        recipe['cook_time'] = recipe.get('cook_time', 0) or 0
        recipe['category'] = recipe.get('category', 'Uncategorized')
        recipe['category_id'] = recipe.get('category_id', 1)
        recipe['difficulty'] = recipe.get('difficulty', 'Medium')
        recipe['title'] = recipe.get('title', 'Untitled Recipe')
        recipe['description'] = recipe.get('description', 'No description available')
        processed_recipes.append(recipe)
    
    conn.close()
    return processed_recipes

def get_category_name(category_id):
    """Get the name of a category"""
    conn = get_connection()
    cursor = dict_cursor(conn)
    
    query = "SELECT name FROM categories WHERE category_id = %s"
    
    cursor.execute(query, (category_id,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        return result['name']
    return "Unknown Category"

def get_recipe_details(recipe_id):
    """Get detailed information for a specific recipe"""
    conn = get_connection()
    cursor = dict_cursor(conn)
    
    try:
        # Get basic recipe information
        recipe_query = """
        SELECT r.*, c.name as category, u.username as author
        FROM recipes r
        LEFT JOIN categories c ON r.category_id = c.category_id
        LEFT JOIN users u ON r.user_id = u.user_id
        WHERE r.recipe_id = %s
        """
        
        cursor.execute(recipe_query, (recipe_id,))
        recipe = cursor.fetchone()
        
        if not recipe:
            return None
        
        # Get ingredients
        ingredients_query = """
        SELECT ri.quantity, ri.notes, i.ingredient_id, i.name as ingredient, i.is_allergen, u.name as unit, u.abbreviation
        FROM recipe_ingredients ri
        JOIN ingredients i ON ri.ingredient_id = i.ingredient_id
        LEFT JOIN units u ON ri.unit_id = u.unit_id
        WHERE ri.recipe_id = %s
        """
        
        cursor.execute(ingredients_query, (recipe_id,))
        ingredients = cursor.fetchall()
        
        # Get preparation steps
        steps_query = """
        SELECT step_number, instruction
        FROM recipe_steps
        WHERE recipe_id = %s
        ORDER BY step_number
        """
        
        cursor.execute(steps_query, (recipe_id,))
        steps = cursor.fetchall()
        
        # Add ingredients and steps to recipe
        recipe['ingredients'] = ingredients
        recipe['steps'] = steps
        
        conn.close()
        return recipe
    except mysql.connector.Error as err:
        print(f"Error getting recipe details: {err}")
        conn.close()
        return None

def search_recipes(search_term):
    """Search for recipes by title, description, or ingredients"""
    conn = get_connection()
    cursor = dict_cursor(conn)
    
    # Using LIKE with wildcards for search
    search_pattern = f"%{search_term}%"
    
    query = """
    SELECT DISTINCT r.recipe_id, r.title, r.description, r.prep_time, r.cook_time, 
           r.difficulty, r.servings, r.notes, r.created_at, r.image_url, 
           c.category_id, c.name as category, u.username as author, r.user_id
    FROM recipes r
    LEFT JOIN categories c ON r.category_id = c.category_id
    LEFT JOIN users u ON r.user_id = u.user_id
    LEFT JOIN recipe_ingredients ri ON r.recipe_id = ri.recipe_id
    LEFT JOIN ingredients i ON ri.ingredient_id = i.ingredient_id
    WHERE r.title LIKE %s
       OR r.description LIKE %s
       OR i.name LIKE %s
    ORDER BY r.created_at DESC
    """
    
    cursor.execute(query, (search_pattern, search_pattern, search_pattern))
    recipes = cursor.fetchall()
    
    # Process recipes to ensure all fields have valid values
    processed_recipes = []
    for recipe in recipes:
        # Add defaults for any missing fields
        recipe['prep_time'] = recipe.get('prep_time', 0) or 0
        recipe['cook_time'] = recipe.get('cook_time', 0) or 0
        recipe['category'] = recipe.get('category', 'Uncategorized')
        recipe['category_id'] = recipe.get('category_id', 1)
        recipe['difficulty'] = recipe.get('difficulty', 'Medium')
        recipe['title'] = recipe.get('title', 'Untitled Recipe')
        recipe['description'] = recipe.get('description', 'No description available')
        processed_recipes.append(recipe)
    
    conn.close()
    return processed_recipes

def add_recipe(title, description, prep_time, cook_time, servings, 
               difficulty, user_id, category_id, image_url, ingredients, steps, notes=None):
    """Add a new recipe with ingredients and preparation steps"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Insert the recipe
        recipe_query = """
        INSERT INTO recipes (title, description, prep_time, cook_time, servings, difficulty, 
                          user_id, category_id, image_url, notes, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """
        
        cursor.execute(recipe_query, (
            title, description, prep_time, cook_time, servings, 
            difficulty, user_id, category_id, image_url, notes
        ))
        
        # Get the ID of the newly inserted recipe
        recipe_id = cursor.lastrowid
        
        # Process ingredients
        for i, ingredient_text in enumerate(ingredients):
            # Try to parse the ingredient text
            # Assuming format like "2 cups flour, sifted" or simple names
            parts = ingredient_text.split(' ', 2)
            
            quantity = None
            unit_id = None
            ingredient_name = ingredient_text
            notes = None
            
            if len(parts) >= 2:
                try:
                    # Try to parse the first part as a number
                    quantity = float(parts[0])
                    
                    # Check if second part is a unit
                    unit_query = "SELECT unit_id FROM units WHERE name = %s OR abbreviation = %s"
                    cursor.execute(unit_query, (parts[1], parts[1]))
                    unit_result = cursor.fetchone()
                    
                    if unit_result:
                        unit_id = unit_result[0]
                        ingredient_name = ' '.join(parts[2:]) if len(parts) > 2 else ''
                    else:
                        ingredient_name = ' '.join(parts[1:])
                    
                    # Check for notes after comma
                    if ',' in ingredient_name:
                        name_parts = ingredient_name.split(',', 1)
                        ingredient_name = name_parts[0].strip()
                        notes = name_parts[1].strip()
                except ValueError:
                    # If first part isn't a number, use the full text as the ingredient name
                    ingredient_name = ingredient_text
            
            # Clean up ingredient name
            ingredient_name = ingredient_name.strip()
            
            if not ingredient_name:
                continue
            
            # Check if ingredient exists, create if not
            cursor.execute("SELECT ingredient_id FROM ingredients WHERE name = %s", (ingredient_name,))
            ingredient_result = cursor.fetchone()
            
            if ingredient_result:
                ingredient_id = ingredient_result[0]
            else:
                # Create new ingredient
                cursor.execute("INSERT INTO ingredients (name) VALUES (%s)", (ingredient_name,))
                ingredient_id = cursor.lastrowid
            
            # Add to recipe_ingredients junction table
            recipe_ingredient_query = """
            INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit_id, notes)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            cursor.execute(recipe_ingredient_query, (recipe_id, ingredient_id, quantity, unit_id, notes))
        
        # Add preparation steps
        for i, step_text in enumerate(steps):
            step_query = """
            INSERT INTO recipe_steps (recipe_id, step_number, instruction)
            VALUES (%s, %s, %s)
            """
            
            cursor.execute(step_query, (recipe_id, i + 1, step_text))
        
        conn.commit()
        conn.close()
        return recipe_id
    except mysql.connector.Error as err:
        print(f"Error adding recipe: {err}")
        conn.rollback()
        conn.close()
        return None

def delete_recipe(recipe_id):
    """Delete a recipe and its related information"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Due to foreign key constraints and ON DELETE CASCADE,
        # we only need to delete from the recipes table
        delete_query = "DELETE FROM recipes WHERE recipe_id = %s"
        cursor.execute(delete_query, (recipe_id,))
        
        affected_rows = cursor.rowcount
        conn.commit()
        conn.close()
        
        return affected_rows > 0
    except mysql.connector.Error as err:
        print(f"Error deleting recipe: {err}")
        conn.rollback()
        conn.close()
        return False

def get_all_ingredients():
    """Get all ingredients"""
    conn = get_connection()
    cursor = dict_cursor(conn)
    
    cursor.execute("SELECT * FROM ingredients ORDER BY name")
    ingredients = cursor.fetchall()
    
    conn.close()
    return ingredients

def add_ingredient(name, description, is_allergen):
    """Add a new ingredient"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        query = """
        INSERT INTO ingredients (name, description, is_allergen)
        VALUES (%s, %s, %s)
        """
        
        cursor.execute(query, (name, description, is_allergen))
        ingredient_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        return ingredient_id
    except mysql.connector.Error as err:
        print(f"Error adding ingredient: {err}")
        conn.rollback()
        conn.close()
        return None

def get_all_categories():
    """Get all categories"""
    conn = get_connection()
    cursor = dict_cursor(conn)
    
    cursor.execute("SELECT * FROM categories ORDER BY name")
    categories = cursor.fetchall()
    
    conn.close()
    return categories

def get_all_units():
    """Get all measurement units"""
    conn = get_connection()
    cursor = dict_cursor(conn)
    
    cursor.execute("SELECT * FROM units ORDER BY name")
    units = cursor.fetchall()
    
    conn.close()
    return units

def update_recipe(recipe_id, recipe_data, ingredients, steps):
    """Update an existing recipe with new data"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Update recipe table
        update_query = """
        UPDATE recipes
        SET title = %s, description = %s, prep_time = %s, cook_time = %s,
            servings = %s, difficulty = %s, category_id = %s, notes = %s,
            updated_at = NOW()
        """
        
        params = [
            recipe_data['title'],
            recipe_data['description'],
            recipe_data['prep_time'],
            recipe_data['cook_time'],
            recipe_data['servings'],
            recipe_data['difficulty'],
            recipe_data['category_id'],
            recipe_data['notes']
        ]
        
        # Add image if provided
        if 'image_url' in recipe_data and recipe_data['image_url']:
            update_query += ", image_url = %s"
            params.append(recipe_data['image_url'])
        
        # Finalize the query with the WHERE clause
        update_query += " WHERE recipe_id = %s"
        params.append(recipe_id)
        
        cursor.execute(update_query, params)
        
        # Delete existing ingredients and steps to replace with new ones
        cursor.execute("DELETE FROM recipe_ingredients WHERE recipe_id = %s", (recipe_id,))
        cursor.execute("DELETE FROM recipe_steps WHERE recipe_id = %s", (recipe_id,))
        
        # Add new ingredients
        for i, ingredient_text in enumerate(ingredients):
            # Try to parse the ingredient text
            parts = ingredient_text.split(' ', 2)
            
            quantity = None
            unit_id = None
            ingredient_name = ingredient_text
            notes = None
            
            if len(parts) >= 2:
                try:
                    # Try to parse the first part as a number
                    quantity = float(parts[0])
                    
                    # Check if second part is a unit
                    unit_query = "SELECT unit_id FROM units WHERE name = %s OR abbreviation = %s"
                    cursor.execute(unit_query, (parts[1], parts[1]))
                    unit_result = cursor.fetchone()
                    
                    if unit_result:
                        unit_id = unit_result[0]
                        ingredient_name = ' '.join(parts[2:]) if len(parts) > 2 else ''
                    else:
                        ingredient_name = ' '.join(parts[1:])
                    
                    # Check for notes after comma
                    if ',' in ingredient_name:
                        name_parts = ingredient_name.split(',', 1)
                        ingredient_name = name_parts[0].strip()
                        notes = name_parts[1].strip()
                except ValueError:
                    # If first part isn't a number, use the full text as the ingredient name
                    ingredient_name = ingredient_text
            
            # Clean up ingredient name
            ingredient_name = ingredient_name.strip()
            
            if not ingredient_name:
                continue
            
            # Check if ingredient exists, create if not
            cursor.execute("SELECT ingredient_id FROM ingredients WHERE name = %s", (ingredient_name,))
            ingredient_result = cursor.fetchone()
            
            if ingredient_result:
                ingredient_id = ingredient_result[0]
            else:
                # Create new ingredient
                cursor.execute("INSERT INTO ingredients (name) VALUES (%s)", (ingredient_name,))
                ingredient_id = cursor.lastrowid
            
            # Add to recipe_ingredients junction table
            recipe_ingredient_query = """
            INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit_id, notes)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            cursor.execute(recipe_ingredient_query, (recipe_id, ingredient_id, quantity, unit_id, notes))
        
        # Add new preparation steps
        for i, step_text in enumerate(steps):
            step_query = """
            INSERT INTO recipe_steps (recipe_id, step_number, instruction)
            VALUES (%s, %s, %s)
            """
            
            cursor.execute(step_query, (recipe_id, i + 1, step_text))
        
        conn.commit()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error updating recipe: {err}")
        conn.rollback()
        conn.close()
        return False

def get_user_by_username(username):
    """Get a user by their username"""
    conn = get_connection()
    cursor = dict_cursor(conn)
    
    query = "SELECT * FROM users WHERE username = %s"
    
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    
    conn.close()
    return user

def verify_password(stored_hash, provided_password):
    """Verify if the provided password matches the stored hash"""
    # Simple password verification using SHA-256
    # In a production environment, use a proper password hashing library like bcrypt
    hashed_provided = hashlib.sha256(provided_password.encode()).hexdigest()
    return stored_hash == hashed_provided

def authenticate_user(username, password):
    """Authenticate a user by username and password"""
    user = get_user_by_username(username)
    
    if not user:
        return None
    
    if verify_password(user['password_hash'], password):
        return user
    
    return None

def get_user_by_email(email):
    """Get a user by their email"""
    conn = get_connection()
    cursor = dict_cursor(conn)
    
    query = "SELECT * FROM users WHERE email = %s"
    
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    
    conn.close()
    return user

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, email, password):
    """Register a new user"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Hash the password
        password_hash = hash_password(password)
        
        # Insert new user
        query = """
        INSERT INTO users (username, email, password_hash, created_at)
        VALUES (%s, %s, %s, NOW())
        """
        
        cursor.execute(query, (username, email, password_hash))
        conn.commit()
        
        # Get the new user ID
        user_id = cursor.lastrowid
        
        # Return the new user
        user = {
            'user_id': user_id,
            'username': username,
            'email': email
        }
        
        conn.close()
        return user
    except mysql.connector.Error as err:
        conn.rollback()
        conn.close()
        print(f"Database error: {err}")
        return None

if __name__ == '__main__':
    # Test connection
    try:
        conn = get_connection()
        print("MySQL connection successful!")
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}") 