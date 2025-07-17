import sqlite3
import os
from typing import List, Optional
from models import Practitioner, Product, ProductCategory

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


class ProductDatabase:
    @staticmethod
    def _get_connection():
        """Get database connection"""
        return sqlite3.connect(DATABASE_PATH)
    
    @staticmethod
    def initialize_database():
        """Initialize the products database with tables and sample data"""
        conn = ProductDatabase._get_connection()
        cursor = conn.cursor()
        
        # Create products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                price REAL NOT NULL,
                original_price REAL,
                rating REAL NOT NULL,
                reviews INTEGER NOT NULL,
                image TEXT NOT NULL,
                category TEXT NOT NULL,
                in_stock BOOLEAN NOT NULL DEFAULT 1
            )
        ''')
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM products")
        if cursor.fetchone()[0] == 0:
            # Insert sample data
            sample_data = [
                ("Organic Turmeric Powder", "Premium quality organic turmeric powder with high curcumin content", 24.99, 29.99, 4.8, 156, "https://images.pexels.com/photos/4198015/pexels-photo-4198015.jpeg?auto=compress&cs=tinysrgb&w=400", "Herbs & Spices", True),
                ("Ashwagandha Capsules", "Natural stress relief and energy support supplement", 39.99, None, 4.9, 203, "https://images.pexels.com/photos/3683074/pexels-photo-3683074.jpeg?auto=compress&cs=tinysrgb&w=400", "Supplements", True),
                ("Herbal Tea Blend", "Calming blend of chamomile, lavender, and holy basil", 18.99, 22.99, 4.7, 89, "https://images.pexels.com/photos/1417945/pexels-photo-1417945.jpeg?auto=compress&cs=tinysrgb&w=400", "Teas", True),
                ("Neem Oil", "Pure cold-pressed neem oil for skin and hair care", 16.99, None, 4.6, 124, "https://images.pexels.com/photos/4041392/pexels-photo-4041392.jpeg?auto=compress&cs=tinysrgb&w=400", "Oils", False),
                ("Triphala Powder", "Traditional Ayurvedic digestive support formula", 21.99, 26.99, 4.8, 167, "https://images.pexels.com/photos/4198015/pexels-photo-4198015.jpeg?auto=compress&cs=tinysrgb&w=400", "Herbs & Spices", True),
                ("Meditation Cushion", "Comfortable organic cotton meditation cushion", 45.99, None, 4.9, 78, "https://images.pexels.com/photos/3822622/pexels-photo-3822622.jpeg?auto=compress&cs=tinysrgb&w=400", "Accessories", True),
                ("Brahmi Capsules", "Memory and cognitive support supplement", 32.99, 37.99, 4.7, 142, "https://images.pexels.com/photos/3683074/pexels-photo-3683074.jpeg?auto=compress&cs=tinysrgb&w=400", "Supplements", True),
                ("Ginger Tea", "Warming digestive tea blend with organic ginger", 14.99, None, 4.5, 95, "https://images.pexels.com/photos/1417945/pexels-photo-1417945.jpeg?auto=compress&cs=tinysrgb&w=400", "Teas", True),
                ("Sesame Oil", "Cold-pressed sesame oil for massage and cooking", 19.99, 24.99, 4.6, 88, "https://images.pexels.com/photos/4041392/pexels-photo-4041392.jpeg?auto=compress&cs=tinysrgb&w=400", "Oils", True),
                ("Yoga Mat", "Non-slip eco-friendly yoga mat", 59.99, None, 4.8, 234, "https://images.pexels.com/photos/3822622/pexels-photo-3822622.jpeg?auto=compress&cs=tinysrgb&w=400", "Accessories", True)
            ]
            
            cursor.executemany('''
                INSERT INTO products (name, description, price, original_price, rating, reviews, image, category, in_stock)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', sample_data)
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_all_products() -> List[Product]:
        """Get all products from database"""
        conn = ProductDatabase._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, description, price, original_price, rating, reviews, image, category, in_stock
            FROM products
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            Product(
                id=row[0],
                name=row[1],
                description=row[2],
                price=row[3],
                originalPrice=row[4],
                rating=row[5],
                reviews=row[6],
                image=row[7],
                category=row[8],
                inStock=bool(row[9])
            )
            for row in rows
        ]
    
    @staticmethod
    def get_product_by_id(product_id: int) -> Optional[Product]:
        """Get a specific product by ID"""
        conn = ProductDatabase._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, description, price, original_price, rating, reviews, image, category, in_stock
            FROM products
            WHERE id = ?
        ''', (product_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Product(
                id=row[0],
                name=row[1],
                description=row[2],
                price=row[3],
                originalPrice=row[4],
                rating=row[5],
                reviews=row[6],
                image=row[7],
                category=row[8],
                inStock=bool(row[9])
            )
        return None
    
    @staticmethod
    def search_products(category: Optional[str] = None, query: Optional[str] = None, in_stock_only: bool = False) -> List[Product]:
        """Search products by category, name, or description"""
        conn = ProductDatabase._get_connection()
        cursor = conn.cursor()
        
        sql_query = '''
            SELECT id, name, description, price, original_price, rating, reviews, image, category, in_stock
            FROM products
            WHERE 1=1
        '''
        params = []
        
        if category:
            sql_query += " AND category LIKE ?"
            params.append(f"%{category}%")
        
        if query:
            sql_query += " AND (name LIKE ? OR description LIKE ?)"
            params.extend([f"%{query}%", f"%{query}%"])
        
        if in_stock_only:
            sql_query += " AND in_stock = 1"
        
        cursor.execute(sql_query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [
            Product(
                id=row[0],
                name=row[1],
                description=row[2],
                price=row[3],
                originalPrice=row[4],
                rating=row[5],
                reviews=row[6],
                image=row[7],
                category=row[8],
                inStock=bool(row[9])
            )
            for row in rows
        ]
    
    @staticmethod
    def get_categories() -> List[ProductCategory]:
        """Get all product categories with counts"""
        conn = ProductDatabase._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT category, COUNT(*) as count
            FROM products
            GROUP BY category
            ORDER BY category
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            ProductCategory(name=row[0], count=row[1])
            for row in rows
        ]