from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from engine_model_setup import Base, User, Product  # Reusing models

engine = create_engine("sqlite:///orm_database.db", echo=False)
Session = sessionmaker(bind=engine)

def run_crud():
    with Session() as session:
        # Reset tables for clean demonstration
        session.query(Product).delete()
        session.query(User).delete()
        session.commit()

        # ----------------------------------------------------
        # 1. CREATE (Insert Single & Bulk)
        # ----------------------------------------------------
        u1 = User(name="Alice", email="alice@example.com")
        session.add(u1)  # Single insert
        session.commit()

        # Bulk insert
        u2 = User(name="Bob", email="bob@example.com")
        u3 = User(name="Carol", email="carol@example.com")
        p1 = Product(name="Mechanical Keyboard", price=79.99)
        p2 = Product(name="Wireless Mouse", price=29.99)
        session.add_all([u2, u3, p1, p2])
        session.commit()
        print("--- 1. CREATE Finished ---")

        # ----------------------------------------------------
        # 2. READ (all, filter_by, filter, get)
        # ----------------------------------------------------
        print("\n--- 2. READ Operations ---")
        # Read All
        all_users = session.query(User).all()
        print(f"Total Users: {len(all_users)}")

        # Exact match via filter_by
        bob = session.query(User).filter_by(name="Bob").first()
        print(f"Found via filter_by: {bob}")

        # Expression match via filter
        cheap_products = session.query(Product).filter(Product.price < 50.0).all()
        print(f"Products under $50: {cheap_products}")

        # Direct Primary Key lookup (Session.get)
        user_by_pk = session.get(User, u1.id)
        print(f"Fetched by PK ({u1.id}): {user_by_pk}")

        # ----------------------------------------------------
        # 3. UPDATE (Object-tracking & Bulk)
        # ----------------------------------------------------
        print("\n--- 3. UPDATE Operations ---")
        # In-place modification tracked automatically by identity map
        bob.email = "bobby_work@example.com"
        session.commit()
        print(f"Updated Bob's email: {session.get(User, bob.id).email}")

        # Direct Bulk UPDATE without object hydration
        session.query(Product).filter(Product.name == "Wireless Mouse").update(
            {Product.price: 24.99}
        )
        session.commit()

        # ----------------------------------------------------
        # 4. DELETE (Individual & Bulk)
        # ----------------------------------------------------
        print("\n--- 4. DELETE Operations ---")
        # Individual object delete
        carol = session.query(User).filter_by(name="Carol").first()
        session.delete(carol)
        session.commit()

        # Bulk query delete
        deleted_count = session.query(Product).filter(Product.price > 100.0).delete()
        session.commit()

        remaining_users = session.query(User).count()
        print(f"Remaining Users after deletions: {remaining_users}")

if __name__ == "__main__":
    run_crud()