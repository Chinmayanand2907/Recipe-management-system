from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, IntegerField, SelectField, BooleanField, FloatField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange, EqualTo, ValidationError
import recipe_db as db

class RecipeForm(FlaskForm):
    title = StringField('Recipe Title', validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    prep_time = IntegerField('Preparation Time (minutes)', validators=[DataRequired(), NumberRange(min=1)])
    cook_time = IntegerField('Cooking Time (minutes)', validators=[DataRequired(), NumberRange(min=0)])
    servings = IntegerField('Servings', validators=[DataRequired(), NumberRange(min=1)])
    difficulty = SelectField('Difficulty', choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    image = FileField('Recipe Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()], description='Enter each ingredient on a new line with quantity and unit (e.g., 2 cups flour)')
    instructions = TextAreaField('Instructions', validators=[DataRequired()], description='Enter each step on a new line')
    notes = TextAreaField('Notes & Tips', validators=[Optional()], description='Optional additional information, tips, or variations')
    submit = SubmitField('Save Recipe')

class IngredientForm(FlaskForm):
    name = StringField('Ingredient Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[Optional()])
    is_allergen = BooleanField('Is an Allergen')
    submit = SubmitField('Add Ingredient')

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = db.get_user_by_username(username.data)
        if user:
            raise ValidationError('Username already taken. Please choose another one.')
    
    def validate_email(self, email):
        user = db.get_user_by_email(email.data)
        if user:
            raise ValidationError('Email already registered. Please use a different email or login.') 