import mysql_db as db
import os

def setup_mysql_database():
    print("Setting up MySQL database for Recipe Management System...")
    
    # Ensure uploads directory exists
    os.makedirs('static/uploads', exist_ok=True)
    
    # Initialize the database
    db.initialize_database()
    
    print("\nDatabase setup complete!")
    print("\nDefault users created:")
    print("  Username: john_doe")
    print("  Password: password")
    print("\n  Username: jane_smith")
    print("  Password: password")
    
    print("\nYou can now run the application with:")
    print("  python mysql_app.py")

if __name__ == "__main__":
    try:
        setup_mysql_database()
    except Exception as e:
        print(f"Error setting up database: {e}")
        
        # Check if it's a connection issue
        if "Can't connect to MySQL server" in str(e):
            print("\nMake sure MySQL server is running!")
            print("You may need to update the database configuration in mysql_db.py:")
            print("  - Check the host, username, password, and database name")
            print("  - Ensure MySQL server is running")
            print("  - Ensure the user has permission to create databases") 