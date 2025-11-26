"""
Database utilities for FIBRA Content Management System
Provides connection and CRUD operations for PostgreSQL database
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_connection():
    """Create and return a database connection"""
    try:
        conn = psycopg2.connect(
            os.getenv('DATABASE_URL'),
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        raise Exception(f"Error connecting to database: {str(e)}")

# ==================== COURSES ====================

def get_courses() -> List[Dict]:
    """Get all courses"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM courses ORDER BY id")
    courses = cur.fetchall()
    cur.close()
    conn.close()
    return courses

def create_course(title: str, image_src: str) -> int:
    """Create a new course"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO courses (title, image_src) VALUES (%s, %s) RETURNING id",
        (title, image_src)
    )
    course_id = cur.fetchone()['id']
    conn.commit()
    cur.close()
    conn.close()
    return course_id

def update_course(course_id: int, title: str, image_src: str):
    """Update an existing course"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE courses SET title = %s, image_src = %s WHERE id = %s",
        (title, image_src, course_id)
    )
    conn.commit()
    cur.close()
    conn.close()

def delete_course(course_id: int):
    """Delete a course"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM courses WHERE id = %s", (course_id,))
    conn.commit()
    cur.close()
    conn.close()

# ==================== UNITS ====================

def get_units(course_id: Optional[int] = None) -> List[Dict]:
    """Get all units or units for a specific course"""
    conn = get_db_connection()
    cur = conn.cursor()
    if course_id:
        cur.execute(
            "SELECT * FROM units WHERE course_id = %s ORDER BY \"order\"",
            (course_id,)
        )
    else:
        cur.execute("SELECT * FROM units ORDER BY course_id, \"order\"")
    units = cur.fetchall()
    cur.close()
    conn.close()
    return units

def create_unit(title: str, description: str, course_id: int, order: int) -> int:
    """Create a new unit"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO units (title, description, course_id, \"order\") VALUES (%s, %s, %s, %s) RETURNING id",
        (title, description, course_id, order)
    )
    unit_id = cur.fetchone()['id']
    conn.commit()
    cur.close()
    conn.close()
    return unit_id

def update_unit(unit_id: int, title: str, description: str, course_id: int, order: int):
    """Update an existing unit"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE units SET title = %s, description = %s, course_id = %s, \"order\" = %s WHERE id = %s",
        (title, description, course_id, order, unit_id)
    )
    conn.commit()
    cur.close()
    conn.close()

def delete_unit(unit_id: int):
    """Delete a unit"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM units WHERE id = %s", (unit_id,))
    conn.commit()
    cur.close()
    conn.close()

# ==================== LESSONS ====================

def get_lessons(unit_id: Optional[int] = None) -> List[Dict]:
    """Get all lessons or lessons for a specific unit"""
    conn = get_db_connection()
    cur = conn.cursor()
    if unit_id:
        cur.execute(
            "SELECT * FROM lessons WHERE unit_id = %s ORDER BY \"order\"",
            (unit_id,)
        )
    else:
        cur.execute("SELECT * FROM lessons ORDER BY unit_id, \"order\"")
    lessons = cur.fetchall()
    cur.close()
    conn.close()
    return lessons

def create_lesson(title: str, unit_id: int, order: int) -> int:
    """Create a new lesson"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO lessons (title, unit_id, \"order\") VALUES (%s, %s, %s) RETURNING id",
        (title, unit_id, order)
    )
    lesson_id = cur.fetchone()['id']
    conn.commit()
    cur.close()
    conn.close()
    return lesson_id

def update_lesson(lesson_id: int, title: str, unit_id: int, order: int):
    """Update an existing lesson"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE lessons SET title = %s, unit_id = %s, \"order\" = %s WHERE id = %s",
        (title, unit_id, order, lesson_id)
    )
    conn.commit()
    cur.close()
    conn.close()

def delete_lesson(lesson_id: int):
    """Delete a lesson"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM lessons WHERE id = %s", (lesson_id,))
    conn.commit()
    cur.close()
    conn.close()

# ==================== CHALLENGES ====================

def get_challenges(lesson_id: Optional[int] = None) -> List[Dict]:
    """Get all challenges or challenges for a specific lesson"""
    conn = get_db_connection()
    cur = conn.cursor()
    if lesson_id:
        cur.execute(
            "SELECT * FROM challenges WHERE lesson_id = %s ORDER BY \"order\"",
            (lesson_id,)
        )
    else:
        cur.execute("SELECT * FROM challenges ORDER BY lesson_id, \"order\"")
    challenges = cur.fetchall()
    cur.close()
    conn.close()
    return challenges

def create_challenge(lesson_id: int, type: str, question: str, order: int, audio_src: Optional[str] = None) -> int:
    """Create a new challenge"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO challenges (lesson_id, type, question, \"order\", audio_src) VALUES (%s, %s, %s, %s, %s) RETURNING id",
        (lesson_id, type, question, order, audio_src)
    )
    challenge_id = cur.fetchone()['id']
    conn.commit()
    cur.close()
    conn.close()
    return challenge_id

def update_challenge(challenge_id: int, lesson_id: int, type: str, question: str, order: int, audio_src: Optional[str] = None):
    """Update an existing challenge"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE challenges SET lesson_id = %s, type = %s, question = %s, \"order\" = %s, audio_src = %s WHERE id = %s",
        (lesson_id, type, question, order, audio_src, challenge_id)
    )
    conn.commit()
    cur.close()
    conn.close()

def delete_challenge(challenge_id: int):
    """Delete a challenge"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM challenges WHERE id = %s", (challenge_id,))
    conn.commit()
    cur.close()
    conn.close()

# ==================== CHALLENGE OPTIONS ====================

def get_challenge_options(challenge_id: Optional[int] = None) -> List[Dict]:
    """Get all challenge options or options for a specific challenge"""
    conn = get_db_connection()
    cur = conn.cursor()
    if challenge_id:
        cur.execute(
            "SELECT * FROM challenge_options WHERE challenge_id = %s ORDER BY id",
            (challenge_id,)
        )
    else:
        cur.execute("SELECT * FROM challenge_options ORDER BY challenge_id, id")
    options = cur.fetchall()
    cur.close()
    conn.close()
    return options

def create_challenge_option(challenge_id: int, text: str, correct: bool, image_src: Optional[str] = None, audio_src: Optional[str] = None) -> int:
    """Create a new challenge option"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO challenge_options (challenge_id, text, correct, image_src, audio_src) VALUES (%s, %s, %s, %s, %s) RETURNING id",
        (challenge_id, text, correct, image_src, audio_src)
    )
    option_id = cur.fetchone()['id']
    conn.commit()
    cur.close()
    conn.close()
    return option_id

def update_challenge_option(option_id: int, challenge_id: int, text: str, correct: bool, image_src: Optional[str] = None, audio_src: Optional[str] = None):
    """Update an existing challenge option"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE challenge_options SET challenge_id = %s, text = %s, correct = %s, image_src = %s, audio_src = %s WHERE id = %s",
        (challenge_id, text, correct, image_src, audio_src, option_id)
    )
    conn.commit()
    cur.close()
    conn.close()

def delete_challenge_option(option_id: int):
    """Delete a challenge option"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM challenge_options WHERE id = %s", (option_id,))
    conn.commit()
    cur.close()
    conn.close()
