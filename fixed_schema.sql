-- Recipe Management System Database Schema for MySQL

-- Drop tables if they exist to avoid conflicts
DROP TABLE IF EXISTS recipe_ingredients;
DROP TABLE IF EXISTS recipe_steps;
DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS ingredients;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS units;
DROP TABLE IF EXISTS users;

-- Create users table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create categories table
CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

-- Create units table for measurement units
CREATE TABLE units (
    unit_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20) NOT NULL UNIQUE,
    abbreviation VARCHAR(10)
);

-- Create ingredients table
CREATE TABLE ingredients (
    ingredient_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    is_allergen BOOLEAN DEFAULT FALSE
);

-- Create recipes table
CREATE TABLE recipes (
    recipe_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    prep_time INT, -- in minutes
    cook_time INT, -- in minutes
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
);

-- Create recipe_ingredients junction table
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
);

-- Create recipe_steps table for preparation steps
CREATE TABLE recipe_steps (
    step_id INT AUTO_INCREMENT PRIMARY KEY,
    recipe_id INT,
    step_number INT NOT NULL,
    instruction TEXT NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE
);

-- Sample users
INSERT INTO users (username, email, password_hash) VALUES 
('john_doe', 'john@example.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'), -- password: password
('jane_smith', 'jane@example.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'); -- password: password

-- Sample categories
INSERT INTO categories (name, description) VALUES
('Breakfast', 'Morning meals to start your day'),
('Lunch', 'Midday meals'),
('Dinner', 'Evening meals'),
('Dessert', 'Sweet treats to enjoy'),
('Vegetarian', 'Meals without meat'),
('Vegan', 'Plant-based meals without animal products');

-- Sample units
INSERT INTO units (name, abbreviation) VALUES
('Gram', 'g'),
('Kilogram', 'kg'),
('Milliliter', 'ml'),
('Liter', 'L'),
('Teaspoon', 'tsp'),
('Tablespoon', 'tbsp'),
('Cup', 'cup'),
('Piece', 'pc');

-- Sample ingredients
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
('Baking Powder', 'Leavening agent for baking', FALSE);

-- Sample recipes
INSERT INTO recipes (title, description, prep_time, cook_time, servings, difficulty, user_id, category_id) VALUES
('Classic Pancakes', 'Fluffy breakfast pancakes that everyone will love', 15, 20, 4, 'Easy', 1, 1),
('Chicken Stir Fry', 'Quick and healthy dinner option', 20, 15, 2, 'Medium', 2, 3);

-- Sample recipe ingredients
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit_id, notes) VALUES
(1, 2, 2, 7, 'Sifted'),  -- 2 cups flour for pancakes
(1, 4, 2, 5, NULL),      -- 2 tsp sugar for pancakes
(1, 5, 2, 8, 'Beaten'),  -- 2 eggs for pancakes
(1, 6, 1.5, 7, NULL),    -- 1.5 cups milk for pancakes
(1, 3, 0.5, 5, NULL),    -- 0.5 tsp salt for pancakes
(1, 11, 1, 5, NULL),     -- 1 tsp baking powder for pancakes
(2, 1, 500, 1, 'Sliced'),-- 500g chicken for stir fry
(2, 7, 2, 8, 'Diced'),   -- 2 tomatoes for stir fry
(2, 8, 1, 8, 'Sliced'),  -- 1 onion for stir fry
(2, 9, 3, 8, 'Minced');  -- 3 garlic cloves for stir fry

-- Sample recipe steps (with properly escaped strings)
INSERT INTO recipe_steps (recipe_id, step_number, instruction) VALUES
(1, 1, 'In a large bowl, sift together the flour, baking powder, salt and sugar.');
INSERT INTO recipe_steps (recipe_id, step_number, instruction) VALUES
(1, 2, 'Make a well in the center and pour in the milk, egg and melted butter; mix until smooth.');
INSERT INTO recipe_steps (recipe_id, step_number, instruction) VALUES
(1, 3, 'Heat a lightly oiled griddle or frying pan over medium-high heat.');
INSERT INTO recipe_steps (recipe_id, step_number, instruction) VALUES
(1, 4, 'Pour or scoop the batter onto the griddle, using approximately 1/4 cup for each pancake.');
INSERT INTO recipe_steps (recipe_id, step_number, instruction) VALUES
(1, 5, 'Cook until bubbles form and the edges are dry, then flip and cook until browned on the other side.');
INSERT INTO recipe_steps (recipe_id, step_number, instruction) VALUES
(2, 1, 'Slice the chicken into thin strips.');
INSERT INTO recipe_steps (recipe_id, step_number, instruction) VALUES
(2, 2, 'Heat oil in a wok or large skillet over high heat.');
INSERT INTO recipe_steps (recipe_id, step_number, instruction) VALUES
(2, 3, 'Add chicken and stir-fry for 5-6 minutes until no longer pink.');
INSERT INTO recipe_steps (recipe_id, step_number, instruction) VALUES
(2, 4, 'Add garlic and onions, stir-fry for 1 minute.');
INSERT INTO recipe_steps (recipe_id, step_number, instruction) VALUES
(2, 5, 'Add tomatoes and other vegetables, stir-fry for 2-3 minutes.');
INSERT INTO recipe_steps (recipe_id, step_number, instruction) VALUES
(2, 6, 'Season with soy sauce and serve hot with rice.'); 