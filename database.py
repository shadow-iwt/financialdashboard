import sqlite3
import hashlib
from pathlib import Path

DATABASE_PATH = "finance_app.db"

def init_db():
    """Initialize the database with required tables"""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create user-specific data directories
        Path("user_data").mkdir(exist_ok=True)
        
        conn.commit()

def hash_password(password: str) -> str:
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username: str, password: str) -> bool:
    """Create a new user account."""
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                (username, hash_password(password))
            )
            conn.commit()
            
            # Create user-specific data directory
            user_dir = Path("user_data") / username
            user_dir.mkdir(exist_ok=True)
            
            # Initialize user's data files
            for file in ["transactions.csv", "clients.csv", "recurring.csv"]:
                if not (user_dir / file).exists():
                    (user_dir / file).touch()
                    
        return True
    except sqlite3.IntegrityError:
        return False

def verify_user(username: str, password: str) -> bool:
    """Verify user credentials."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT password_hash FROM users WHERE username = ?',
            (username,)
        )
        result = cursor.fetchone()
        
        if result is None:
            return False
            
        stored_hash = result[0]
        return stored_hash == hash_password(password)

def get_user_data_path(username: str, filename: str) -> str:
    """Get the path to a user's data file."""
    return str(Path("user_data") / username / filename)

# Initialize the database when this module is imported
init_db()
