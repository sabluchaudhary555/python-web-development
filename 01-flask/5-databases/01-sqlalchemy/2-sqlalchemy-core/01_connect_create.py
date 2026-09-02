from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

# 1. Database engine banayen
engine = create_engine('sqlite:///database.db', echo=True)

# 2. MetaData object banayen
metadata = MetaData()

# 3. Table ka structure define karein
students_table = Table(
    'students', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('age', Integer)
)

# 4. Database aur table create karein
metadata.create_all(engine)

print("\n🚀 Database aur Table successfully ban gaye hain!")