"""
Export inventory from BusyWin SQL Server to JSON
"""

import pyodbc
import json
from datetime import datetime
import config

def get_db_connection():
    """Create database connection"""
    try:
        conn_str = (
            f"DRIVER={config.SQL_SERVER['driver']};"
            f"SERVER={config.SQL_SERVER['server']};"
            f"DATABASE={config.SQL_SERVER['database']};"
        )
        
        if 'trusted_connection' in config.SQL_SERVER:
            conn_str += f"Trusted_Connection={config.SQL_SERVER['trusted_connection']};"
        
        conn = pyodbc.connect(conn_str)
        print(f"✅ Connected to database: {config.SQL_SERVER['database']}")
        return conn
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None

def export_inventory():
    """Export inventory data to JSON"""
    conn = get_db_connection()
    if not conn:
        return False
    
    query = """
    SELECT
      I.Name AS ItemName,
      I.Alias AS ItemAlias,
      G.Name AS GroupName,
      ISNULL(I.D2, 0) AS Item_MRP,
      ISNULL(I.D3, 0) AS Item_Sale_Price,
      ISNULL(I.D4, 0) AS Item_Purchase_Price,
      COALESCE(NULLIF(I.D9, 0), OV.OpenValPerUnit, 0) AS Item_Wholesale_Price,
      ISNULL(SQ.Stock, 0) AS Stock
    FROM Master1 I
    LEFT JOIN Master1 G
      ON I.ParentGrp = G.Code AND G.MasterType = 5
    LEFT JOIN (
      SELECT T4.MasterCode1 AS ItemCode,
             SUM(T4.D1) AS OpenQty,
             SUM(T4.D2) AS OpenValue,
             CASE WHEN SUM(T4.D1) <> 0 THEN SUM(T4.D2) / SUM(T4.D1) ELSE 0 END AS OpenValPerUnit
      FROM Tran4 T4
      GROUP BY T4.MasterCode1
    ) OV
      ON OV.ItemCode = I.Code
    LEFT JOIN (
      SELECT T2.MasterCode1 AS ItemCode,
             SUM(CASE WHEN T2.TranType IN (0,1) THEN T2.Value1 ELSE -T2.Value1 END) AS Stock
      FROM Tran2 T2
      GROUP BY T2.MasterCode1
    ) SQ
      ON SQ.ItemCode = I.Code
    WHERE I.MasterType = 6
    ORDER BY I.Name
    """
    
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        
        # Get column names
        columns = [column[0] for column in cursor.description]
        
        # Fetch all rows
        rows = cursor.fetchall()
        
        # Convert to list of dictionaries
        items = []
        for row in rows:
            item = {}
            for i, col in enumerate(columns):
                value = row[i]
                if isinstance(value, (int, float)):
                    value = float(value)
                item[col] = value
            items.append(item)
        
        conn.close()
        
        # Add metadata
        output = {
            'last_updated': datetime.now().isoformat(),
            'total_items': len(items),
            'items': items
        }
        
        # Save to JSON file
        with open(config.JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Exported {len(items)} items to {config.JSON_FILE}")
        
        # Show sample
        if items:
            print(f"\n📊 Sample: {items[0].get('ItemName')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Export error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 SR Fashion - BusyWin Export Tool")
    print("=" * 40)
    export_inventory()