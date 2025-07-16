import sqlite3
import os
from typing import List, Optional
from models import Practitioner

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "practitioners.db")

class PractitionerDatabase:
    @staticmethod
    def _get_connection():
        """Get database connection"""
        return sqlite3.connect(DATABASE_PATH)
    
    @staticmethod
    def initialize_database():
        """Initialize the database with tables and sample data"""
        conn = PractitionerDatabase._get_connection()
        cursor = conn.cursor()
        
        # Create practitioners table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS practitioners (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                specialty TEXT NOT NULL,
                rating REAL NOT NULL,
                experience TEXT NOT NULL,
                location TEXT NOT NULL,
                next_available TEXT NOT NULL,
                image TEXT NOT NULL
            )
        ''')
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM practitioners")
        if cursor.fetchone()[0] == 0:
            # Insert sample data
            sample_data = [
                ("Dr. Priya Sharma", "Ayurvedic Medicine", 4.9, "15 years", "Downtown Wellness Center", "Today 2:00 PM", "https://images.pexels.com/photos/5452293/pexels-photo-5452293.jpeg?auto=compress&cs=tinysrgb&w=400"),
                ("Dr. Rajesh Patel", "Panchakarma Therapy", 4.8, "12 years", "Holistic Health Hub", "Tomorrow 10:00 AM", "https://images.pexels.com/photos/5452201/pexels-photo-5452201.jpeg?auto=compress&cs=tinysrgb&w=400"),
                ("Dr. Maya Joshi", "Herbal Medicine", 4.7, "18 years", "Natural Healing Center", "Today 4:30 PM", "https://images.pexels.com/photos/5452274/pexels-photo-5452274.jpeg?auto=compress&cs=tinysrgb&w=400"),
                ("Dr. Anand Kumar", "Pulse Diagnosis", 4.6, "20 years", "Traditional Healing Center", "Tomorrow 3:00 PM", "https://images.pexels.com/photos/5452268/pexels-photo-5452268.jpeg?auto=compress&cs=tinysrgb&w=400"),
                ("Dr. Kavitha Nair", "Yoga Therapy", 4.8, "10 years", "Mind-Body Wellness Studio", "Today 6:00 PM", "https://images.pexels.com/photos/5452275/pexels-photo-5452275.jpeg?auto=compress&cs=tinysrgb&w=400")
            ]
            
            cursor.executemany('''
                INSERT INTO practitioners (name, specialty, rating, experience, location, next_available, image)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', sample_data)
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_all_practitioners() -> List[Practitioner]:
        """Get all practitioners from database"""
        conn = PractitionerDatabase._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, specialty, rating, experience, location, next_available, image
            FROM practitioners
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            Practitioner(
                id=row[0],
                name=row[1],
                specialty=row[2],
                rating=row[3],
                experience=row[4],
                location=row[5],
                nextAvailable=row[6],
                image=row[7]
            )
            for row in rows
        ]
    
    @staticmethod
    def get_practitioner_by_id(practitioner_id: int) -> Optional[Practitioner]:
        """Get a specific practitioner by ID"""
        conn = PractitionerDatabase._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, specialty, rating, experience, location, next_available, image
            FROM practitioners
            WHERE id = ?
        ''', (practitioner_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Practitioner(
                id=row[0],
                name=row[1],
                specialty=row[2],
                rating=row[3],
                experience=row[4],
                location=row[5],
                nextAvailable=row[6],
                image=row[7]
            )
        return None
    
    @staticmethod
    def search_practitioners(specialty: Optional[str] = None, location: Optional[str] = None) -> List[Practitioner]:
        """Search practitioners by specialty and/or location"""
        conn = PractitionerDatabase._get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT id, name, specialty, rating, experience, location, next_available, image
            FROM practitioners
            WHERE 1=1
        '''
        params = []
        
        if specialty:
            query += " AND specialty LIKE ?"
            params.append(f"%{specialty}%")
        
        if location:
            query += " AND location LIKE ?"
            params.append(f"%{location}%")
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [
            Practitioner(
                id=row[0],
                name=row[1],
                specialty=row[2],
                rating=row[3],
                experience=row[4],
                location=row[5],
                nextAvailable=row[6],
                image=row[7]
            )
            for row in rows
        ]