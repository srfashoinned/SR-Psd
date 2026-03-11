"""
Test script to verify database connection and query
"""

import pyodbc
import config

def test_connection():
    """Test database connection and run a simple query"""
    try:
        conn_str = (
            f"DRIVER={config.SQL_SERVER['driver']};"
            f"SERVER={config.SQL_SERVER['server']};"
            f"DATABASE={config.SQL_SERVER['database']};"
        )
        
        if 'trusted_connection' in config.SQL_SERVER:
            conn_str += f"Trusted_Connection={config.SQL_SERVER['trusted_connection']};"
        else:
            conn_str += f"UID={config.SQL_SERVER['username']};PWD={config.SQL_SERVER['password']};"
        
        print("🔌 Connecting to database...")
        conn = pyodbc.connect(conn_str)
        print("✅ Connected successfully!")
        
        # Test simple query
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 5 Name, Alias FROM Master1 WHERE MasterType = 6")
        
        rows = cursor.fetchall()
        print(f"\n📊 Found {len(rows)} sample items:")
        for row in rows:
            print(f"  - {row.Name} (Barcode: {row.Alias})")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_connection()