from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    insert,
    select,
    text,
    and_,
    or_
)

# 1. Database connection & reflection
engine = create_engine('sqlite:///database.db', echo=False)
metadata = MetaData()
students_table = Table('students', metadata, autoload_with=engine)

with engine.connect() as conn:

    # ----------------------------------------------------
    # Topic 1 & 2: SQL Expressions & Executing Expression (Insert Data)
    # ----------------------------------------------------
    insert_stmt = insert(students_table).values([
        {'name': 'Alice', 'age': 22},
        {'name': 'Bob', 'age': 24},
        {'name': 'Charlie', 'age': 19},
        {'name': 'David', 'age': 22}
    ])
    conn.execute(insert_stmt)
    conn.commit()
    print("--- 1. Data Inserted Successfully ---")

    # ----------------------------------------------------
    # Topic 3: Selecting Rows (Fetching all records)
    # ----------------------------------------------------
    select_all_stmt = select(students_table)
    result = conn.execute(select_all_stmt)
    print("\n--- 2. All Students (select) ---")
    for row in result:
        print(f"ID: {row.id} | Name: {row.name} | Age: {row.age}")

    # ----------------------------------------------------
    # Topic 4: Using Textual SQL (Raw SQL Queries)
    # ----------------------------------------------------
    text_stmt = text("SELECT name, age FROM students WHERE age >= :min_age")
    result_text = conn.execute(text_stmt, {"min_age": 22})
    print("\n--- 3. Textual SQL (Students with age >= 22) ---")
    for row in result_text:
        print(f"Name: {row.name} | Age: {row.age}")

    # ----------------------------------------------------
    # Topic 5: Using Conjunctions (and_, or_, where)
    # ----------------------------------------------------
    # Example: Students named 'Alice' OR (age > 20 AND age < 25)
    conjunction_stmt = select(students_table).where(
        or_(
            students_table.c.name == 'Alice',
            and_(
                students_table.c.age > 20,
                students_table.c.age < 25
            )
        )
    )
    result_conj = conn.execute(conjunction_stmt)
    print("\n--- 4. Filtered Rows Using Conjunctions (AND / OR) ---")
    for row in result_conj:
        print(f"ID: {row.id} | Name: {row.name} | Age: {row.age}")