# SQLAlchemy — Introduction & Installation

## 1. What is SQLAlchemy?

SQLAlchemy is a Python library used to interact with relational databases using Python code. It provides tools for executing SQL queries, managing database connections, and working with database records through Python objects instead of writing raw SQL directly.

**Key Characteristics**
- Supports popular databases such as MySQL, PostgreSQL, SQLite, and MongoDB.
- Allows developers to write database operations using Python instead of raw SQL for many common tasks.
- Provides an Object Relational Mapping (ORM) system that maps database tables to Python classes.
- Can be used with both ORM-based and SQL-based (Core) approaches, depending on project requirements.

## 2. Installation

**Prerequisites**
- Python already installed
- pip or Conda (depending on preference)

**Method 1 — Using pip (Standard Python Installation)**
```
pip install sqlalchemy
```

**Method 2 — Using Conda (Anaconda Distribution)**
```
conda install -c anaconda sqlalchemy
```
- Type `y` when prompted to confirm.
- Best practice — install inside a dedicated conda environment rather than the base environment:
```
conda create -n my-env
conda activate my-env
```
- If using conda-forge as the preferred channel:
```
conda config --env --add channels conda-forge
```

**Method 3 — Verifying Installation**

Using Python (works regardless of pip/conda method):
```python
import sqlalchemy
print(sqlalchemy.__version__)
```
Output: `2.0.45`

Using pip directly (Command Prompt):
```
python -m pip show sqlalchemy
```
This displays installed package details (version, location, dependencies), confirming the installation.

Using Conda (Anaconda PowerShell Prompt):
```
conda list sqlalchemy
```
This lists the installed SQLAlchemy package and its version from the active conda environment.

## 3. Connecting to a Database

Before performing any database operations, a connection must be established using `create_engine()`.

**Syntax**
```python
import sqlalchemy as db
engine = db.create_engine(
    "dialect+driver://username:password@host:port/database_name"
)
```

**Connecting to SQLite**

SQLite stores data in a local file and does not require a separate database server — commonly used for learning, testing, and small applications.
```python
import sqlalchemy as db
engine = db.create_engine("sqlite:///students.db")
```
Explanation: This creates a connection to the SQLite database file `students.db`. If the file does not exist, SQLite will create it automatically.

**Connecting to MySQL**

MySQL is a relational database management system used in web and enterprise applications.
```python
import sqlalchemy as db

engine = db.create_engine(
    "mysql+pymysql://root:password@localhost:3306/company"
)
```
Explanation: This connects to a MySQL database named `company` running on the local machine. Here, `root` is the username, `password` is the database password, and `3306` is the default MySQL port.

**Connecting to PostgreSQL**

PostgreSQL is an open-source relational database known for its reliability and powerful features.
```python
import sqlalchemy as db

engine = db.create_engine(
    "postgresql://username:password@localhost:5432/company"
)
```
Explanation: This connects to a PostgreSQL database named `company`. Replace `username` and `password` with actual database credentials — `5432` is the default PostgreSQL port.

## 4. Querying Data with SQLAlchemy

SQLAlchemy allows queries to be built using Python expressions instead of writing raw SQL statements — making queries easier to integrate with Python applications while still providing functionality similar to SQL.

**Example 1 — Filtering Records**

Suppose a table named `books` contains information about different books. The following query retrieves only records whose category is "Programming".

Equivalent SQL:
```sql
SELECT *
FROM books
WHERE category = 'Programming';
```

SQLAlchemy Query:
```python
db.select(books).where(
    books.c.category == "Programming"
)
```

Explanation:
- `db.select(books)` creates a query that selects records from the `books` table.
- `books.c.category` accesses the `category` column of the table.
- `.where()` filters the records and returns only those where the category is "Programming".

**Example 2 — Multiple Conditions**

Suppose the `books` table also needs to be filtered by publish year. The following query retrieves books in the "Programming" category published after 2020.

Equivalent SQL:
```sql
SELECT *
FROM books
WHERE category = 'Programming'
AND publish_year > 2020;
```

SQLAlchemy Query:
```python
db.select(books).where(
    db.and_(
        books.c.category == "Programming",
        books.c.publish_year > 2020
    )
)
```

Explanation:
- `db.and_()` combines multiple filtering conditions into a single query.
- `books.c.category == "Programming"` selects books from the Programming category.
- `books.c.publish_year > 2020` selects books published after 2020.
- A record is returned only if both conditions are satisfied.

## 5. SQL vs SQLAlchemy

Both SQL and SQLAlchemy are used to interact with databases, but they differ in how queries are written and executed. SQL uses database-specific query statements, whereas SQLAlchemy provides Python-based tools for performing the same operations.

| SQL | SQLAlchemy |
|---|---|
| Queries are written as SQL statements. | Queries are built using Python expressions. |
| Requires direct SQL syntax knowledge. | Uses Python objects and methods. |
| Database tables are referenced directly. | Tables and columns are represented as Python objects. |
| Suitable for raw database operations. | Suitable for both ORM and SQL-based development. |

## Notes

- SQLAlchemy's connection string format follows the pattern `dialect+driver://username:password@host:port/database_name` — the dialect identifies the database type (sqlite, mysql, postgresql), and driver specifies which underlying library handles the actual connection (e.g. `pymysql` for MySQL).
- For MySQL connections, an additional driver package (like `pymysql`) usually needs to be installed separately via `pip install pymysql` — SQLAlchemy itself doesn't bundle database-specific drivers.
- SQLite connection strings use three slashes for a relative path (`sqlite:///students.db`) — a fourth slash would indicate an absolute file path instead.
- Default ports are standard but can vary in real deployments: MySQL commonly uses 3306, PostgreSQL commonly uses 5432 — always confirm the actual port configured on the target server.
- `db.and_()` combines conditions with logical AND; a corresponding `db.or_()` exists for OR-based filtering, following the same pattern.
- SQLAlchemy can be used two ways: SQLAlchemy Core (the query-building style shown above, working directly with table objects) or the ORM (mapping tables to Python classes) — both are part of the same library, chosen based on project needs.