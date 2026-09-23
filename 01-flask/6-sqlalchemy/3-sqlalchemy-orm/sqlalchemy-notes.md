# SQLAlchemy ORM

## Module 1: Introduction to SQLAlchemy ORM

SQLAlchemy is a Python SQL toolkit and Object Relational Mapper (ORM) that lets you interact with relational databases using Python classes and objects instead of writing raw SQL. It has two main layers: the **Core** (expression language, closer to SQL) and the **ORM** (maps Python classes to database tables). These notes focus on the ORM layer, which is what most application developers use day to day.

- SQLAlchemy ORM maps a Python class to a database table, where each class attribute becomes a column and each instance becomes a row.
- It supports multiple database backends (SQLite, MySQL, PostgreSQL, etc.) through the same Python API, so switching databases mostly means changing the connection string.
- The ORM tracks changes to objects in memory and translates them into SQL statements (INSERT, UPDATE, DELETE) when you commit a session.
- Edge case: SQLAlchemy does not auto-detect schema changes on existing tables (no built-in migrations) — tools like **Alembic** are used for schema migrations in real projects.
- Edge case: mixing raw SQL and ORM queries in the same session is allowed, but careless mixing can cause the session's identity map to go out of sync with the database.

### Installation

```bash
pip install sqlalchemy
```

---

## Module 2: Engine — The Starting Point

The **Engine** is the core interface to the database. It manages a pool of database connections and knows how to speak the specific SQL dialect of the backend you're using (SQLite, MySQL, PostgreSQL, etc.). You create an engine once per database and reuse it throughout the application.

- The engine is created using `create_engine()` with a **connection URL** in the format `dialect+driver://username:password@host:port/database`.
- For SQLite, the URL is simpler since there's no server — it just points to a file (or `:memory:` for an in-memory database).
- The engine does not connect to the database immediately; it connects lazily on first use (unless `echo=True` triggers early logging).
- `echo=True` prints every SQL statement SQLAlchemy generates — extremely useful for debugging and learning.
- Edge case: creating multiple engines to the same database wastes connections; the engine is meant to be a singleton per database in an application.

### Syntax

```python
from sqlalchemy import create_engine

engine = create_engine("sqlite:///example.db", echo=True)
```

- `create_engine()` — builds the Engine object; this is the function that actually sets up the connection pool and dialect.
- `"sqlite:///example.db"` — the connection URL; tells SQLAlchemy which database type and file/server to connect to.
- `echo=True` — turns on logging of every generated SQL statement, useful while learning or debugging.

### Example

```python
from sqlalchemy import create_engine

engine = create_engine("sqlite:///app.db", echo=False)
print(engine.url)
# Output: sqlite:///app.db
```

---

## Module 3: Declarative Base & Models

The **Declarative Base** is a base class that SQLAlchemy uses to keep track of all model classes and their mapped tables. Every ORM model class inherits from this base. Each model class then defines columns as class attributes using `Column()` (or `Mapped`/`mapped_column()` in SQLAlchemy 2.0 style).

- `declarative_base()` (1.x style) or `DeclarativeBase` (2.0 style) creates the registry that links Python classes to database tables.
- The `__tablename__` attribute is mandatory — it tells SQLAlchemy which table name to use in the database.
- Every model needs at least one `primary_key=True` column, since the ORM uses primary keys as object identity.
- Edge case: forgetting `__tablename__` raises an `InvalidRequestError` at class definition time, not at query time.
- Edge case: two models cannot share the same class name within the same declarative base registry, or SQLAlchemy raises a mapper configuration error.

### Syntax

```python
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class ModelName(Base):
    __tablename__ = "table_name"
    id = Column(Integer, primary_key=True)
```

- `declarative_base()` — creates the base class that all your model classes must inherit from.
- `class ModelName(Base)` — defines a model by inheriting from `Base`; this is what gets mapped to a table.
- `__tablename__` — the actual table name to use in the database; required on every model.
- `id = Column(Integer, primary_key=True)` — defines a column named `id` of integer type and marks it as the table's primary key.

### Example

```python
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100), unique=True)

print(User.__tablename__)
# Output: users
```

---

## Module 4: Common Column Types & Constraints

SQLAlchemy provides Python-level types that map to SQL column types under the hood. Choosing the right type ensures correct validation and storage on the database side.

- `Integer`, `String(length)`, `Float`, `Boolean`, `DateTime`, `Text`, `Numeric` are the most commonly used column types.
- Constraints are passed as keyword arguments to `Column()`: `primary_key=True`, `nullable=False`, `unique=True`, `default=value`, `index=True`.
- `default` sets a Python-side default applied on insert if no value is given; `server_default` sets a database-side default instead.
- Edge case: `nullable=False` is only enforced by the database engine at insert time — SQLAlchemy itself won't stop you from building an object with a missing required field in memory.
- Edge case: `String` without a length works fine on SQLite (which ignores length) but will error or truncate silently on strict engines like MySQL.

### Syntax

```python
Column(TypeName, primary_key=False, nullable=True, unique=False, default=None, index=False)
```

- `TypeName` — the data type of the column, e.g. `Integer`, `String(50)`, `Boolean`, `DateTime`.
- `primary_key` — if `True`, marks this column as the table's primary key.
- `nullable` — if `False`, the database will reject rows that don't provide a value for this column.
- `unique` — if `True`, no two rows can have the same value in this column.
- `default` — a Python-side value (or callable) automatically used if none is given when creating a row.
- `index` — if `True`, creates a database index on this column for faster lookups.

### Example

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    in_stock = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

p = Product(name="Notebook")
print(p.in_stock)
# Output: True
```

---

## Module 5: Creating Tables

Once models are defined, the actual tables must be created in the database. SQLAlchemy generates the `CREATE TABLE` statements automatically based on the model definitions.

- `Base.metadata.create_all(engine)` creates all tables registered under that declarative base, if they don't already exist.
- It is **idempotent** — running it again does not recreate or overwrite existing tables.
- It does **not** alter existing tables if you change a model's columns later; that requires a migration tool like Alembic.
- Edge case: if two models reference each other via foreign keys, SQLAlchemy figures out the correct creation order automatically.

### Syntax

```python
Base.metadata.create_all(engine)
```

- `Base.metadata` — the collection of all table definitions registered under this declarative base.
- `.create_all(engine)` — generates and runs the `CREATE TABLE` statements for any tables that don't already exist, using the given engine's connection.

### Example

```python
Base.metadata.create_all(engine)
# Output: (creates users, products tables in app.db if not present)
```

---

## Module 6: Session — Talking to the Database

The **Session** is the ORM's workspace for all database operations — it stages changes, tracks object identity, and commits transactions. While the Engine handles raw connections, the Session handles the object-to-row bookkeeping.

- `sessionmaker(bind=engine)` creates a Session **factory**; you call it (`Session()`) to get an actual session instance.
- A session tracks three states of objects: pending (added, not committed), persistent (saved and tracked), and detached (no longer associated with a session).
- `session.add(obj)` stages an object for insertion; nothing hits the database until `session.commit()`.
- `session.commit()` flushes all pending changes and commits the transaction; `session.rollback()` discards uncommitted changes.
- Edge case: forgetting to close a session can leak connections in long-running applications — using a context manager (`with Session() as session:`) avoids this.
- Edge case: after `commit()`, object attributes are expired by default and will trigger a fresh SELECT the next time they're accessed (unless `expire_on_commit=False`).

### Syntax

```python
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()
```

- `sessionmaker(bind=engine)` — creates a reusable Session **factory** tied to a specific engine; you configure this once.
- `Session()` — calling the factory produces an actual session instance you use to run queries and commit changes.

### Example

```python
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

new_user = User(name="Alice", email="alice@example.com")
session.add(new_user)
session.commit()
print(new_user.id)
# Output: 1
```

---

## Module 7: CRUD — Create (Insert)

Inserting data means creating a model instance in Python and staging it with the session.

- A single object: `session.add(obj)`.
- Multiple objects at once: `session.add_all([obj1, obj2, ...])`, which is more efficient than calling `add()` in a loop.
- The primary key is usually auto-assigned by the database (autoincrement) and only available on the Python object **after** `commit()` or `flush()`.
- Edge case: `session.flush()` sends pending SQL to the database without committing the transaction — useful when you need a generated ID before deciding whether to commit.

### Syntax

```python
session.add(instance)
session.add_all([instance1, instance2])
session.commit()
```

- `session.add(instance)` — stages a single object to be inserted; doesn't touch the database yet.
- `session.add_all([...])` — stages multiple objects at once, in one go instead of looping `add()`.
- `session.commit()` — actually sends the staged INSERT statements to the database and finalizes the transaction.

### Example

```python
u1 = User(name="Bob", email="bob@example.com")
u2 = User(name="Carol", email="carol@example.com")
session.add_all([u1, u2])
session.commit()
print(u1.id, u2.id)
# Output: 2 3
```

---

## Module 8: CRUD — Read (Querying)

Reading data is done through `session.query()` (1.x style) or `session.execute(select(...))` (2.0 style). Both let you filter, sort, and limit results.

- `session.query(Model).all()` returns every row as a list of model instances.
- `.filter_by(column=value)` filters using keyword arguments (works only on the queried model's own columns).
- `.filter(Model.column == value)` filters using explicit column expressions and supports more complex conditions (`>`, `<`, `!=`, `.like()`, `.in_()`).
- `.first()` returns the first matching row or `None`; `.one()` raises an error if there isn't exactly one match; `.get(pk)` (or `session.get(Model, pk)` in 2.0) fetches by primary key directly.
- Edge case: `.filter_by()` cannot filter across joined tables using dotted syntax — for joins, `.filter()` with explicit column references is required.
- Edge case: `.first()` silently returns `None` on no match, which can hide bugs if not checked explicitly before using the result.

### Syntax

```python
session.query(Model).filter(Model.column == value).all()
session.query(Model).filter_by(column=value).first()
session.get(Model, primary_key)
```

- `session.query(Model)` — starts a query against the given model's table.
- `.filter(Model.column == value)` — filters using an explicit column expression; supports operators like `>`, `<`, `.like()`.
- `.filter_by(column=value)` — a shorthand filter using keyword arguments, only for the model's own columns.
- `.all()` — executes the query and returns every matching row as a list.
- `.first()` — executes the query and returns just the first matching row, or `None` if nothing matches.
- `session.get(Model, primary_key)` — fetches a single row directly by its primary key value, no filtering needed.

### Example

```python
all_users = session.query(User).all()
print(len(all_users))
# Output: 3

bob = session.query(User).filter_by(name="Bob").first()
print(bob.email)
# Output: bob@example.com

fetched = session.get(User, 1)
print(fetched.name)
# Output: Alice
```

---

## Module 9: CRUD — Update

Updating a row is as simple as modifying the attribute of a fetched object and committing — no explicit UPDATE statement is written by hand.

- Fetch the object, change its attribute(s), then call `session.commit()` — SQLAlchemy detects the change via its unit-of-work tracking and issues an UPDATE.
- Bulk updates without loading objects into memory: `session.query(Model).filter(...).update({Model.column: new_value})`.
- Edge case: bulk `.update()` bypasses Python-side model logic (like `@validates` decorators or default callables) since it issues SQL directly.

### Syntax

```python
obj.column = new_value
session.commit()
```

- `obj.column = new_value` — simply reassigns the attribute on an already-fetched, session-tracked object; SQLAlchemy notices this change automatically.
- `session.commit()` — turns the detected change into an UPDATE statement and saves it to the database.

### Example

```python
user = session.query(User).filter_by(name="Bob").first()
user.email = "bobby@example.com"
session.commit()

updated = session.get(User, user.id)
print(updated.email)
# Output: bobby@example.com
```

---

## Module 10: CRUD — Delete

Deleting removes a tracked object from both the session and the underlying table.

- `session.delete(obj)` stages an object for deletion; it's only removed from the database after `session.commit()`.
- Bulk delete without loading objects: `session.query(Model).filter(...).delete()`.
- Edge case: deleting a parent row that has related child rows (via foreign key) can raise an `IntegrityError` unless a cascade rule (like `cascade="all, delete"`) is defined on the relationship.

### Syntax

```python
session.delete(obj)
session.commit()
```

- `session.delete(obj)` — marks a session-tracked object for deletion; still not removed from the database yet.
- `session.commit()` — executes the DELETE statement and finalizes the removal.

### Example

```python
carol = session.query(User).filter_by(name="Carol").first()
session.delete(carol)
session.commit()

remaining = session.query(User).count()
print(remaining)
# Output: 2
```

---

## Module 11: Relationships — ForeignKey and relationship()

Real applications have related tables — SQLAlchemy models this using `ForeignKey` (at the database level) combined with `relationship()` (at the Python object level), so related rows can be accessed as Python attributes instead of manual joins.

- `ForeignKey("table.column")` on a `Column` creates the actual database-level constraint linking two tables.
- `relationship("OtherModel")` on the model creates a Python-level attribute that lazily loads related objects — it does not create a database column itself.
- `backref="name"` (or the more explicit `back_populates`) creates the reverse-direction attribute automatically, so a parent can access its children and vice versa.
- One-to-many is the default shape of `relationship()`; many-to-many requires an extra **association table** passed via the `secondary` argument.
- Edge case: without `back_populates`/`backref`, the two sides of a relationship exist independently and won't stay in sync in memory until you re-query.
- Edge case: accessing a lazy-loaded relationship attribute outside an active session raises a `DetachedInstanceError`.

### Syntax

```python
class Parent(Base):
    __tablename__ = "parents"
    id = Column(Integer, primary_key=True)
    children = relationship("Child", back_populates="parent")

class Child(Base):
    __tablename__ = "children"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("parents.id"))
    parent = relationship("Parent", back_populates="children")
```

- `ForeignKey("parents.id")` — a database-level constraint on `parent_id`, linking each child row to a specific parent row.
- `relationship("Child", back_populates="parent")` — a Python-only attribute that lets you access a parent's related children as a list, without writing a join manually.
- `back_populates="parent"` / `back_populates="children"` — links both sides of the relationship together so updating one side (e.g. appending a child) is reflected on the other side in memory too.

### Example

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    books = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")

Base.metadata.create_all(engine)

a = Author(name="John")
a.books.append(Book(title="Learning ORM"))
session.add(a)
session.commit()

fetched_author = session.query(Author).filter_by(name="John").first()
print(fetched_author.books[0].title)
# Output: Learning ORM
```

---

## Module 12: Ordering, Limiting, and Joins

Beyond basic filtering, SQLAlchemy supports sorting, pagination, and explicit joins for querying across related tables.

- `.order_by(Model.column)` sorts ascending; `.order_by(Model.column.desc())` sorts descending.
- `.limit(n)` restricts the number of rows returned; `.offset(n)` skips the first `n` rows — together they implement pagination.
- `.join(OtherModel)` performs an SQL JOIN based on the relationship or foreign key already defined between models.
- `.count()` returns the number of matching rows without loading them all into memory as objects.
- Edge case: chaining `.limit()` before `.order_by()` still works because SQLAlchemy builds the full query lazily and only finalizes SQL when the query is executed (`.all()`, `.first()`, etc.).

### Syntax

```python
session.query(Model).order_by(Model.column.desc()).limit(n).offset(m).all()
session.query(Model).join(OtherModel).filter(...).all()
```

- `.order_by(Model.column.desc())` — sorts the results by the given column; `.desc()` reverses it to descending order (leave it off for ascending).
- `.limit(n)` — caps the number of rows returned to `n`.
- `.offset(m)` — skips the first `m` rows before returning results, used together with `.limit()` for pagination.
- `.join(OtherModel)` — performs an SQL JOIN with another model's table, based on the relationship/foreign key already defined between them.

### Example

```python
recent_books = (
    session.query(Book)
    .order_by(Book.id.desc())
    .limit(5)
    .all()
)
print(len(recent_books))
# Output: 1

joined = (
    session.query(Book)
    .join(Author)
    .filter(Author.name == "John")
    .all()
)
print(joined[0].title)
# Output: Learning ORM
```

---

## Cheat Sheet

| Concept | Syntax | Key Point |
|---|---|---|
| Create engine | `create_engine("sqlite:///app.db", echo=True)` | Entry point managing the connection pool |
| Declarative base | `Base = declarative_base()` | Registry linking Python classes to tables |
| Define model | `class M(Base): __tablename__ = "t"; id = Column(Integer, primary_key=True)` | `__tablename__` is mandatory |
| Column with constraint | `Column(String(50), nullable=False, unique=True)` | Constraints enforced by the DB engine |
| Create tables | `Base.metadata.create_all(engine)` | Idempotent, does not alter existing tables |
| Create session | `Session = sessionmaker(bind=engine); session = Session()` | Session tracks pending/persistent/detached states |
| Insert (single) | `session.add(obj); session.commit()` | PK only populated after commit/flush |
| Insert (bulk) | `session.add_all([obj1, obj2])` | More efficient than looped `add()` |
| Read all | `session.query(Model).all()` | Returns list of model instances |
| Read filtered | `session.query(Model).filter(Model.col == val).first()` | `.filter()` supports complex expressions |
| Read by PK | `session.get(Model, pk)` | Direct primary-key lookup |
| Update | `obj.col = new_val; session.commit()` | Unit-of-work auto-detects attribute changes |
| Delete | `session.delete(obj); session.commit()` | Cascade rules needed for related child rows |
| Relationship (1-to-many) | `relationship("Child", back_populates="parent")` | Python-level only, no DB column created |
| Foreign key | `Column(Integer, ForeignKey("parents.id"))` | Actual DB-level constraint |
| Order results | `.order_by(Model.col.desc())` | Ascending by default |
| Paginate | `.limit(n).offset(m)` | Combine for page-by-page fetching |
| Join | `.join(OtherModel).filter(...)` | Uses defined FK/relationship |
| Count | `.count()` | Avoids loading full objects into memory |