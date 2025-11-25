# database.py - PostgreSQL database connection and query functions

import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database connection string from environment variable
# Format: postgresql://user:password@host:port/database
DATABASE_URL = os.getenv('DATABASE_URL')

def get_db_connection():
    """
    Creates and returns a connection to the PostgreSQL database.
    Uses psycopg2 library for database operations.
    """
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable not set. Please add it to your .env file.")
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except psycopg2.Error as e:
        raise Exception(f"Failed to connect to database: {str(e)}")


def insert_dog_questionnaire(breed_name: str, age_years: float, status_list: list) -> dict:
    """
    Inserts dog questionnaire response into questions_dog_initial3 table.
    
    Args:
        breed_name: AKC breed name
        age_years: Dog's age in years
        status_list: List of diet-related statuses (e.g., ['puppy', 'allergy'])
    
    Returns:
        Dictionary with success status and inserted record ID
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Convert status list to comma-separated string for storage
        status_string = ', '.join(status_list) if status_list else None
        
        # SQL INSERT query
        insert_query = """
            INSERT INTO questions_dog_initial3 
            (breed_name_AKC, age_years_preReg, status_dietRelat_preReg)
            VALUES (%s, %s, %s)
            RETURNING id_preRegister;
        """
        
        # Execute query with parameters (prevents SQL injection)
        cursor.execute(insert_query, (breed_name, age_years, status_string))
        
        # Fetch the returned ID of the newly inserted record
        record_id = cursor.fetchone()[0]
        
        # Commit transaction to save changes to database
        conn.commit()
        
        return {
            'success': True,
            'id': record_id,
            'message': f'Successfully saved dog questionnaire response (ID: {record_id})'
        }
        
    except psycopg2.Error as e:
        # Rollback transaction if error occurs
        if conn:
            conn.rollback()
        raise Exception(f"Database error: {str(e)}")
    finally:
        # Close cursor and connection
        if conn:
            cursor.close()
            conn.close()


def get_all_questionnaire_responses() -> list:
    """
    Retrieves all dog questionnaire responses from database.
    
    Returns:
        List of dictionaries containing all questionnaire records
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)  # RealDictCursor returns results as dictionaries
        
        select_query = "SELECT * FROM questions_dog_initial3 ORDER BY modified_preReg DESC;"
        cursor.execute(select_query)
        
        results = cursor.fetchall()
        return list(results)
        
    except psycopg2.Error as e:
        raise Exception(f"Database error: {str(e)}")
    finally:
        if conn:
            cursor.close()
            conn.close()


def get_questionnaire_response(record_id: int) -> dict:
    """
    Retrieves a specific questionnaire response by ID.
    
    Args:
        record_id: The id_preRegister value to retrieve
    
    Returns:
        Dictionary with the questionnaire record
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        select_query = "SELECT * FROM questions_dog_initial3 WHERE id_preRegister = %s;"
        cursor.execute(select_query, (record_id,))
        
        result = cursor.fetchone()
        return dict(result) if result else None
        
    except psycopg2.Error as e:
        raise Exception(f"Database error: {str(e)}")
    finally:
        if conn:
            cursor.close()
            conn.close()
