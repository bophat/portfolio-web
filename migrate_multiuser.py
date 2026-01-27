"""
Migration script for multi-user portfolio system.
Adds public_id to users and user_id to all portfolio tables.
"""
import pymysql

# Database connection settings (for Docker MySQL)
DB_CONFIG = {
    "host": "db",
    "user": "portfolio_user", 
    "password": "portfolio_password",
    "database": "portfolio_db"
}


def migrate():
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # 1. Add public_id to users table
        print("Adding public_id to users table...")
        try:
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN public_id VARCHAR(20) UNIQUE
            """)
            conn.commit()
            print("  ✓ Added public_id column")
        except pymysql.err.OperationalError as e:
            if "Duplicate column name" in str(e):
                print("  - public_id column already exists")
            else:
                raise
        
        # 2. Add user_id to profile table
        print("Adding user_id to profile table...")
        try:
            cursor.execute("""
                ALTER TABLE profile 
                ADD COLUMN user_id INT,
                ADD FOREIGN KEY (user_id) REFERENCES users(id)
            """)
            conn.commit()
            print("  ✓ Added user_id column")
        except pymysql.err.OperationalError as e:
            if "Duplicate column name" in str(e):
                print("  - user_id column already exists")
            else:
                raise

        # 3. Add user_id to skills table
        print("Adding user_id to skills table...")
        try:
            cursor.execute("""
                ALTER TABLE skills 
                ADD COLUMN user_id INT,
                ADD FOREIGN KEY (user_id) REFERENCES users(id)
            """)
            conn.commit()
            print("  ✓ Added user_id column")
        except pymysql.err.OperationalError as e:
            if "Duplicate column name" in str(e):
                print("  - user_id column already exists")
            else:
                raise

        # 4. Add user_id to projects table
        print("Adding user_id to projects table...")
        try:
            cursor.execute("""
                ALTER TABLE projects 
                ADD COLUMN user_id INT,
                ADD FOREIGN KEY (user_id) REFERENCES users(id)
            """)
            conn.commit()
            print("  ✓ Added user_id column")
        except pymysql.err.OperationalError as e:
            if "Duplicate column name" in str(e):
                print("  - user_id column already exists")
            else:
                raise

        # 5. Add user_id to learning_goals table
        print("Adding user_id to learning_goals table...")
        try:
            cursor.execute("""
                ALTER TABLE learning_goals 
                ADD COLUMN user_id INT,
                ADD FOREIGN KEY (user_id) REFERENCES users(id)
            """)
            conn.commit()
            print("  ✓ Added user_id column")
        except pymysql.err.OperationalError as e:
            if "Duplicate column name" in str(e):
                print("  - user_id column already exists")
            else:
                raise

        # 6. Add user_id to about_info table
        print("Adding user_id to about_info table...")
        try:
            cursor.execute("""
                ALTER TABLE about_info 
                ADD COLUMN user_id INT,
                ADD FOREIGN KEY (user_id) REFERENCES users(id)
            """)
            conn.commit()
            print("  ✓ Added user_id column")
        except pymysql.err.OperationalError as e:
            if "Duplicate column name" in str(e):
                print("  - user_id column already exists")
            else:
                raise

        # 7. Add user_id to quick_facts table
        print("Adding user_id to quick_facts table...")
        try:
            cursor.execute("""
                ALTER TABLE quick_facts 
                ADD COLUMN user_id INT,
                ADD FOREIGN KEY (user_id) REFERENCES users(id)
            """)
            conn.commit()
            print("  ✓ Added user_id column")
        except pymysql.err.OperationalError as e:
            if "Duplicate column name" in str(e):
                print("  - user_id column already exists")
            else:
                raise

        # 8. Add user_id to contact_info table
        print("Adding user_id to contact_info table...")
        try:
            cursor.execute("""
                ALTER TABLE contact_info 
                ADD COLUMN user_id INT,
                ADD FOREIGN KEY (user_id) REFERENCES users(id)
            """)
            conn.commit()
            print("  ✓ Added user_id column")
        except pymysql.err.OperationalError as e:
            if "Duplicate column name" in str(e):
                print("  - user_id column already exists")
            else:
                raise

        # 9. Add user_id to timeline_items table
        print("Adding user_id to timeline_items table...")
        try:
            cursor.execute("""
                ALTER TABLE timeline_items 
                ADD COLUMN user_id INT,
                ADD FOREIGN KEY (user_id) REFERENCES users(id)
            """)
            conn.commit()
            print("  ✓ Added user_id column")
        except pymysql.err.OperationalError as e:
            if "Duplicate column name" in str(e):
                print("  - user_id column already exists")
            else:
                raise

        print("\n✅ Migration completed successfully!")
        
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    migrate()
