from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.models import Course, Document, Semester, Subject, Unit, University, User
from app.services.auth_service import authenticate_user, register_user


def test_database_models_create_tables() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)

    with engine.begin() as connection:
        tables = [
            "users",
            "universities",
            "courses",
            "semesters",
            "subjects",
            "units",
            "documents",
        ]
        for table_name in tables:
            row = connection.execute(
                text("SELECT name FROM sqlite_master WHERE type = 'table' AND name = :table_name"),
                {"table_name": table_name},
            ).fetchone()
            assert row is not None, f"Missing table: {table_name}"


def test_database_model_relationships_can_be_instantiated() -> None:
    university = University(name="AKTU")
    course = Course(name="B.Tech CSE", university=university)
    semester = Semester(number=6, course=course)
    subject = Subject(name="DBMS", semester=semester)
    unit = Unit(number=3, title="Normalization", subject=subject)
    document = Document(
        title="DBMS Unit 3 Notes",
        file_name="dbms-unit-3.pdf",
        document_type="notes",
        source="admin_upload",
        university=university,
        course=course,
        semester=semester,
        subject=subject,
        unit=unit,
    )
    user = User(email="student@example.com", full_name="Sample Student", password_hash="hashed")

    assert university.name == "AKTU"
    assert course.name == "B.Tech CSE"
    assert semester.number == 6
    assert subject.name == "DBMS"
    assert unit.number == 3
    assert document.title == "DBMS Unit 3 Notes"
    assert user.email == "student@example.com"


def test_user_registration_and_authentication_persist_in_db() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    db = Session()

    try:
        result = register_user("user@example.com", "Pass123!", "User One", db=db)
        assert result["email"] == "user@example.com"
        assert authenticate_user("user@example.com", "Pass123!", db=db) is not None
        assert authenticate_user("user@example.com", "wrong-password", db=db) is None
    finally:
        db.close()
