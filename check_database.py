import sqlite3
import os

def check_database():
    """Check the SQLite database structure and export it for MySQL conversion"""
    
    if not os.path.exists('employees.db'):
        print("Error: employees.db file not found!")
        return
    
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('employees.db')
        cursor = conn.cursor()
        
        print("=== SQLite Database Analysis ===")
        print(f"Database file: employees.db")
        print(f"File size: {os.path.getsize('employees.db')} bytes")
        print()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            print("No tables found in the database.")
            return
        
        print(f"Found {len(tables)} table(s):")
        print("-" * 50)
        
        # Analyze each table
        for table in tables:
            table_name = table[0]
            print(f"\nTable: {table_name}")
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            print("Columns:")
            for col in columns:
                col_id, name, data_type, not_null, default_val, primary_key = col
                pk_str = " PRIMARY KEY" if primary_key else ""
                not_null_str = " NOT NULL" if not_null else ""
                default_str = f" DEFAULT {default_val}" if default_val else ""
                print(f"  - {name}: {data_type}{not_null_str}{default_str}{pk_str}")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = cursor.fetchone()[0]
            print(f"Row count: {row_count}")
            
            # Show sample data (first 3 rows)
            if row_count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                sample_data = cursor.fetchall()
                print("Sample data:")
                for i, row in enumerate(sample_data, 1):
                    print(f"  Row {i}: {row}")
        
        # Export schema and data for MySQL conversion
        print("\n" + "=" * 60)
        print("Exporting database for MySQL conversion...")
        
        # Get all SQL statements
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table'")
        table_schemas = cursor.fetchall()
        
        with open('employees_mysql_export.sql', 'w', encoding='utf-8') as f:
            f.write("-- MySQL Database Export from SQLite\n")
            f.write("-- Generated automatically\n\n")
            
            # Write table creation statements
            for schema in table_schemas:
                if schema[0]:  # schema[0] contains the CREATE TABLE statement
                    sql = schema[0]
                    # Convert SQLite syntax to MySQL syntax
                    sql = sql.replace('AUTOINCREMENT', 'AUTO_INCREMENT')
                    sql = sql.replace('INTEGER PRIMARY KEY', 'INT AUTO_INCREMENT PRIMARY KEY')
                    sql = sql.replace('WITHOUT ROWID', '')
                    # Replace double quotes with backticks for identifiers
                    import re
                    sql = re.sub(r'"([^"]+)"', r'`\1`', sql)
                    f.write(sql + ";\n\n")
            
            # Export data
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                
                if rows:
                    # Get column names
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = cursor.fetchall()
                    column_names = [col[1] for col in columns]
                    
                    f.write(f"-- Data for table `{table_name}`\n")
                    f.write(f"INSERT INTO `{table_name}` (`{'`, `'.join(column_names)}`) VALUES\n")
                    
                    for i, row in enumerate(rows):
                        # Convert row data to MySQL format
                        formatted_row = []
                        for value in row:
                            if value is None:
                                formatted_row.append('NULL')
                            elif isinstance(value, str):
                                # Escape single quotes and wrap in quotes
                                escaped_value = value.replace("'", "''")
                                formatted_row.append(f"'{escaped_value}'")
                            else:
                                formatted_row.append(str(value))
                        
                        row_str = f"({', '.join(formatted_row)})"
                        if i < len(rows) - 1:
                            row_str += ","
                        f.write(f"{row_str}\n")
                    
                    f.write(";\n\n")
        
        print("✓ Database exported to 'employees_mysql_export.sql'")
        print("✓ This file is ready for import into MySQL")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_database() 