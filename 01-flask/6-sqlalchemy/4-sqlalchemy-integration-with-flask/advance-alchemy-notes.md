# SQLAlchemy  Many-to-Many, Migrations & Flask Integration

## Module 13: Many-to-Many Relationships

A many-to-many relationship exists when multiple rows in one table can relate to multiple rows in another (e.g., students and courses). SQLAlchemy models this with a plain **association table** (no model class needed) passed to `relationship()` via the `secondary` argument.

- The association table only needs two foreign key columns (one to each side) — it usually doesn't need its own primary key or model class unless you want to store extra data on the relationship itself (like a timestamp).
- `relationship("OtherModel", secondary=association_table, back_populates="...")` is how both sides declare the link.
- If the association table needs extra columns (e.g., `enrolled_on`), it must be promoted to a full model class, and the relationship is then built using an **association object** pattern instead of a plain `secondary` table.
- Edge case: forgetting `back_populates` on both sides means appending to one side's collection won't be reflected on the other side until a fresh query.
- Edge case: a plain `secondary` table cannot hold extra data — trying to add columns to it silently ignores them from the ORM's perspective unless you switch to the association object pattern.

### Syntax

```python
from sqlalchemy import Table, Column, Integer, ForeignKey

association_table = Table(
    "association",
    Base.metadata,
    Column("left_id", Integer, ForeignKey("left.id")),
    Column("right_id", Integer, ForeignKey("right.id")),
)

class Left(Base):
    __tablename__ = "left"
    id = Column(Integer, primary_key=True)
    rights = relationship("Right", secondary=association_table, back_populates="lefts")
```

### Example

```python
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

student_course = Table(
    "student_course",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id")),
    Column("course_id", Integer, ForeignKey("courses.id")),
)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    courses = relationship("Course", secondary=student_course, back_populates="students")

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    students = relationship("Student", secondary=student_course, back_populates="courses")

Base.metadata.create_all(engine)

s = Student(name="John")
c = Course(title="Databases 101")
s.courses.append(c)
session.add(s)
session.commit()

print(s.courses[0].title)
# Output: Databases 101
print(c.students[0].name)
# Output: John
```

---

## Module 14: Alembic — Database Migrations

`create_all()` only creates tables that don't exist yet — it never alters existing tables when a model changes (a new column, a renamed field, a changed type). **Alembic** is SQLAlchemy's companion migration tool that tracks schema changes as versioned Python scripts, so a database can be upgraded or downgraded step by step.

- Alembic keeps a `alembic_version` table in the database to know which migration was last applied.
- `alembic init alembic` scaffolds a migrations folder with a config file (`alembic.ini`) and an `env.py` that needs to point to your models' metadata.
- `alembic revision --autogenerate -m "message"` compares your current models against the database and generates a migration script with the detected changes.
- `alembic upgrade head` applies all pending migrations up to the latest; `alembic downgrade -1` rolls back one step.
- Edge case: autogenerate does not reliably detect every kind of change (e.g., column renames look like a drop + add unless manually adjusted in the generated script).
- Edge case: `env.py` must import your models' `Base.metadata` correctly, or autogenerate will think every table needs to be created from scratch.

### Syntax

```bash
pip install alembic
alembic init alembic
alembic revision --autogenerate -m "add new column"
alembic upgrade head
```

### Example

```python
# In alembic/env.py, point Alembic to your models:
from myapp.models import Base
target_metadata = Base.metadata
```

```bash
# After adding a new column to a model:
alembic revision --autogenerate -m "add phone number to users"
alembic upgrade head
# Output: Running upgrade  -> a1b2c3d4, add phone number to users
```

---

## Module 15: SQLAlchemy Integration with Flask (Flask-SQLAlchemy)

**Flask-SQLAlchemy** is an extension that wraps plain SQLAlchemy to fit naturally into a Flask app's lifecycle — it manages the engine, session, and declarative base for you, tied to the Flask app context.

- Install with `pip install flask-sqlalchemy`.
- The database URL is set via the Flask config key `SQLALCHEMY_DATABASE_URI`, and the extension is initialized with `db = SQLAlchemy(app)`.
- Models inherit from `db.Model` instead of a manually created declarative base — Flask-SQLAlchemy provides this base internally.
- Columns and relationships use `db.Column`, `db.Integer`, `db.String`, `db.ForeignKey`, `db.relationship` — same concepts as plain SQLAlchemy, just namespaced under `db`.
- The session is automatically available as `db.session`, scoped to the request lifecycle, so you don't manually create a `sessionmaker`.
- `db.create_all()` (run inside an app context) creates all tables, same idea as plain `Base.metadata.create_all(engine)`.
- Edge case: `db.create_all()` must be called within `with app.app_context():` in newer Flask-SQLAlchemy versions, or it raises a `RuntimeError` about missing application context.
- Edge case: unlike a manually managed session, `db.session` is tied to the request — leftover uncommitted changes from a failed request can leak into the next one if not explicitly rolled back in error handlers.
- Edge case: using both a raw SQLAlchemy engine and Flask-SQLAlchemy's `db` object in the same app can create two separate connection pools to the same database, which usually indicates a project structure mistake.

### Syntax

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
db = SQLAlchemy(app)

class ModelName(db.Model):
    id = db.Column(db.Integer, primary_key=True)
```

### Example

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text)

with app.app_context():
    db.create_all()

    new_post = Post(title="Hello Flask", body="First post using Flask-SQLAlchemy.")
    db.session.add(new_post)
    db.session.commit()

    fetched = Post.query.filter_by(title="Hello Flask").first()
    print(fetched.body)
    # Output: First post using Flask-SQLAlchemy.
```

### Flask Route Example (Full CRUD Snippet)

```python
@app.route("/posts", methods=["GET"])
def list_posts():
    posts = Post.query.all()
    return {"posts": [p.title for p in posts]}
    # Output (JSON): {"posts": ["Hello Flask"]}

@app.route("/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = db.session.get(Post, post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
    return {"status": "deleted"}
    # Output (JSON): {"status": "deleted"}
```

---

## Cheat Sheet

| Concept | Syntax | Key Point |
|---|---|---|
| Association table (many-to-many) | `Table("assoc", Base.metadata, Column("a_id", ForeignKey("a.id")), Column("b_id", ForeignKey("b.id")))` | No model class needed unless extra columns required |
| Many-to-many relationship | `relationship("B", secondary=assoc, back_populates="a_list")` | Both sides need `back_populates` to stay in sync |
| Association object (extra data) | Promote association table to a full model with its own relationships | Needed when the link itself has attributes |
| Alembic init | `alembic init alembic` | Scaffolds migration folder + config |
| Point Alembic to models | `target_metadata = Base.metadata` in `env.py` | Required for autogenerate to detect changes |
| Generate migration | `alembic revision --autogenerate -m "message"` | Doesn't reliably detect renames |
| Apply migration | `alembic upgrade head` | Applies all pending migrations |
| Rollback migration | `alembic downgrade -1` | Steps back one revision |
| Flask-SQLAlchemy install | `pip install flask-sqlalchemy` | Wraps SQLAlchemy for Flask's app lifecycle |
| Configure DB URI | `app.config["SQLALCHEMY_DATABASE_URI"] = "..."` | Set before initializing `SQLAlchemy(app)` |
| Init extension | `db = SQLAlchemy(app)` | Provides `db.Model`, `db.session`, `db.Column`, etc. |
| Define model | `class M(db.Model): id = db.Column(db.Integer, primary_key=True)` | Inherits `db.Model` instead of manual declarative base |
| Create tables | `with app.app_context(): db.create_all()` | Must run inside an app context |
| Query shortcut | `Model.query.filter_by(...).first()` | Flask-SQLAlchemy's convenience query interface |
| Session in Flask | `db.session.add(obj); db.session.commit()` | Scoped automatically to the request lifecycle |