#!/usr/bin/env python3
"""
Debug script for SalonPro Manager.
Use this to test database operations.
"""

import sys
from pathlib import Path

# Ensure project root is on PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))


def main():
    print("SalonPro Manager - Debug Console")
    print("=" * 40)

    try:
        # Import database components
        from database import init_db, engine

        # Initialize database (creates tables)
        session = init_db()

        # Inspect database tables
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        print(f"\nTables in database: {len(tables)}")
        for table in tables:
            print(f"  - {table}")

        print("\n Database ready!")
        print("File: salonpro.db")

        session.close()

    except Exception as e:
        print("\n❌ Error occurred:")
        print(e)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
