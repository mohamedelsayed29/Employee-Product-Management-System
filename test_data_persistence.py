#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify data persistence in the مصراوي سات application
"""

import sqlite3
import os

def test_data_persistence():
    """Test if data is properly saved and can be retrieved"""
    
    print("=" * 50)
    print("Testing Data Persistence")
    print("=" * 50)
    
    # Check if database file exists
    if not os.path.exists("employees.db"):
        print("✗ Database file 'employees.db' not found!")
        return False
    
    print(f"✓ Database file found: {os.path.getsize('employees.db')} bytes")
    
    try:
        # Connect to database
        conn = sqlite3.connect("employees.db")
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"\nFound {len(tables)} table(s):")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Check data in each table
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"\n{table_name}: {count} record(s)")
            
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                sample_data = cursor.fetchall()
                print("  Sample data:")
                for i, row in enumerate(sample_data, 1):
                    print(f"    Row {i}: {row}")
        
        conn.close()
        print("\n✓ Data persistence test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n✗ Error testing data persistence: {e}")
        return False

def add_test_data():
    """Add some test data to verify persistence"""
    
    print("\n" + "=" * 50)
    print("Adding Test Data")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect("employees.db")
        cursor = conn.cursor()
        
        # Add test employee
        cursor.execute("INSERT INTO employees (name, email, department) VALUES (?, ?, ?)", 
                      ("Test Employee", "test@example.com", "Test Department"))
        
        # Add test category
        cursor.execute("INSERT INTO categories (name) VALUES (?)", ("Test Category",))
        
        # Add test product
        cursor.execute("INSERT INTO products (name, category, price, quantity) VALUES (?, ?, ?, ?)", 
                      ("Test Product", "Test Category", 99.99, 10))
        
        conn.commit()
        conn.close()
        
        print("✓ Test data added successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Error adding test data: {e}")
        return False

def main():
    """Main test function"""
    
    print("مصراوي سات - Data Persistence Test")
    print("This script tests if your data is properly saved and can be retrieved.")
    print()
    
    # Test current data
    if test_data_persistence():
        print("\nYour data persistence is working correctly!")
    else:
        print("\nThere might be an issue with data persistence.")
    
    # Ask if user wants to add test data
    response = input("\nWould you like to add some test data? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        if add_test_data():
            print("\nNow run the main application and check if the test data appears.")
            print("Then close the application and run this test again to verify persistence.")
        else:
            print("\nFailed to add test data.")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main() 