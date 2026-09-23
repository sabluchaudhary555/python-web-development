from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine("sqlite:///orm_database.db", echo=False)
Base = declarative_base()

# ----------------------------------------------------
# 1. Models with 1-to-Many Relationship
# ----------------------------------------------------
class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    # Relationship does not create a column in the DB table
    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Author(id={self.id}, name='{self.name}')>"


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    pages = Column(Integer)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    author = relationship("Author", back_populates="books")

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', pages={self.pages})>"


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def run_relations_and_joins():
    with Session() as session:
        session.query(Book).delete()
        session.query(Author).delete()
        session.commit()

        # ----------------------------------------------------
        # 2. Populating Graph Data (Relationship append)
        # ----------------------------------------------------
        author1 = Author(name="Robert C. Martin")
        author1.books.append(Book(title="Clean Code", pages=464))
        author1.books.append(Book(title="Clean Architecture", pages=432))

        author2 = Author(name="Martin Fowler")
        author2.books.append(Book(title="Refactoring", pages=448))

        session.add_all([author1, author2])
        session.commit()

        # ----------------------------------------------------
        # 3. Explicit Joins
        # ----------------------------------------------------
        print("--- 1. Querying with JOIN ---")
        joined_results = (
            session.query(Book.title, Author.name)
            .join(Author, Book.author_id == Author.id)
            .filter(Author.name == "Robert C. Martin")
            .all()
        )
        for title, author_name in joined_results:
            print(f"Book: '{title}' | Written by: {author_name}")

        # ----------------------------------------------------
        # 4. Ordering, Limiting, Pagination, and Count
        # ----------------------------------------------------
        print("\n--- 2. Ordering & Pagination ---")
        # Order descending by pages and limit
        paged_books = (
            session.query(Book)
            .order_by(Book.pages.desc())
            .limit(2)
            .offset(0)
            .all()
        )
        for b in paged_books:
            print(f"Top Book: {b.title} ({b.pages} pages)")

        total_books = session.query(Book).count()
        print(f"\nTotal Books count: {total_books}")

if __name__ == "__main__":
    run_relations_and_joins()