from sqlalchemy import create_engine, MetaData, Table, update, delete, select, bindparam

# 1. Connect to existing database and reflect table structure
engine = create_engine('sqlite:///database.db', echo=False)
metadata = MetaData()
students_table = Table('students', metadata, autoload_with=engine)


def print_table_data(connection, message):
    """Helper function to inspect current rows in the database"""
    print(f"\n--- {message} ---")
    results = connection.execute(select(students_table)).fetchall()
    if not results:
        print("Table is currently empty.")
    for row in results:
        print(f"ID: {row.id} | Name: {row.name} | Age: {row.age}")


with engine.connect() as conn:
    print_table_data(conn, "Initial Table State")

    # ----------------------------------------------------
    # Topic 1: Using UPDATE Expression (Single record update)
    # Target: Update 'Alice' (ID: 5) to change age to 23
    # ----------------------------------------------------
    update_single_stmt = (
        update(students_table)
        .where(students_table.c.name == 'Alice')
        .values(age=23)
    )
    conn.execute(update_single_stmt)
    conn.commit()
    print_table_data(conn, "After Single Row Update ('Alice' age set to 23)")

    # ----------------------------------------------------
    # Topic 2: Multiple Updates / Parameterized Batch Updates
    # Target: Update multiple records simultaneously using bindparam
    # ----------------------------------------------------
    batch_update_stmt = (
        update(students_table)
        .where(students_table.c.name == bindparam('b_name'))
        .values(age=bindparam('new_age'))
    )

    batch_data = [
        {'b_name': 'Bob', 'new_age': 26},
        {'b_name': 'Charlie', 'new_age': 21}
    ]

    conn.execute(batch_update_stmt, batch_data)
    conn.commit()
    print_table_data(conn, "After Batch Update ('Bob' -> 26, 'Charlie' -> 21)")

    # ----------------------------------------------------
    # Topic 3: Using DELETE Expression (Single / Conditional delete)
    # Target: Delete student where name is 'Charlie'
    # ----------------------------------------------------
    delete_single_stmt = (
        delete(students_table)
        .where(students_table.c.name == 'Charlie')
    )
    conn.execute(delete_single_stmt)
    conn.commit()
    print_table_data(conn, "After Single Row Deletion (Deleted 'Charlie')")

    # ----------------------------------------------------
    # Topic 4: Multiple Deletes / Clean-up Deletions
    # Target: Delete multiple records matching a condition (e.g., age >= 24)
    # ----------------------------------------------------
    delete_multiple_stmt = (
        delete(students_table)
        .where(students_table.c.age >= 24)
    )
    conn.execute(delete_multiple_stmt)
    conn.commit()
    print_table_data(conn, "After Multiple Deletions (Deleted all with Age >= 24)")