from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

# 1. Create database engine
engine = create_engine('sqlite:///database.db', echo=True)

# 2. Initialize MetaData object
metadata = MetaData()

# 3. Define the table structure
students_table = Table(
    'students', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('age', Integer)
)

# 4. Create the database and tables
metadata.create_all(engine)

print("\n🚀 Database and Table created successfully!")