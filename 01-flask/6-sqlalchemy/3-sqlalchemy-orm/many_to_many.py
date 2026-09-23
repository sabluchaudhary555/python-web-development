from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine("sqlite:///orm_m2m_database.db", echo=False)
Base = declarative_base()

# ----------------------------------------------------
# 1. Association Table (Pure Table, No Model Class Needed)
# ----------------------------------------------------
student_course_association = Table(
    "student_courses",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True),
)

# ----------------------------------------------------
# 2. Models with Many-to-Many Relationship via secondary
# ----------------------------------------------------
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    # secondary points directly to the association table
    courses = relationship(
        "Course",
        secondary=student_course_association,
        back_populates="students"
    )

    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.name}')>"


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)

    students = relationship(
        "Student",
        secondary=student_course_association,
        back_populates="courses"
    )

    def __repr__(self):
        return f"<Course(id={self.id}, title='{self.title}')>"


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def run_many_to_many():
    with Session() as session:
        # Reset tables for clean run
        session.query(Student).delete()
        session.query(Course).delete()
        session.commit()

        # Create Entities
        s1 = Student(name="John Doe")
        s2 = Student(name="Jane Smith")

        c1 = Course(title="Python & Database Engineering")
        c2 = Course(title="System Design Basics")

        # Bidirectional graph linking
        s1.courses.append(c1)
        s1.courses.append(c2)
        s2.courses.append(c1)  # c1 has both John and Jane

        session.add_all([s1, s2])
        session.commit()

        # Querying through the Many-to-Many graph
        print("--- Student to Courses ---")
        student = session.query(Student).filter_by(name="John Doe").first()
        for course in student.courses:
            print(f"Student: {student.name} -> Enrolled in: {course.title}")

        print("\n--- Course to Students ---")
        course = session.query(Course).filter_by(title="Python & Database Engineering").first()
        for stud in course.students:
            print(f"Course: {course.title} -> Student: {stud.name}")

if __name__ == "__main__":
    run_many_to_many()