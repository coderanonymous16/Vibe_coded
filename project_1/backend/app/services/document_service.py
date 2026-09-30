from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.models.academic import Course, Document, Semester, Subject, Unit, University


def seed_default_catalog(db: Session) -> list[dict]:
    if db.query(University).count() > 0:
        return []

    records = [
        {"university": "AKTU", "course": "B.Tech CSE", "semester": 6, "subject": "DBMS", "unit": 3, "title": "DBMS Unit 3 Notes", "file_name": "dbms-unit-3.pdf"},
        {"university": "AKTU", "course": "B.Tech CSE", "semester": 6, "subject": "OS", "unit": 2, "title": "Operating Systems Quick Revision", "file_name": "os-quick-revision.pdf"},
        {"university": "AKTU", "course": "B.Tech CSE", "semester": 5, "subject": "CN", "unit": 1, "title": "Computer Networks Notes", "file_name": "cn-unit-1.pdf"},
    ]

    for record in records:
        university = db.query(University).filter_by(name=record["university"]).first()
        if university is None:
            university = University(name=record["university"])
            db.add(university)
            db.flush()

        course = db.query(Course).filter_by(university_id=university.id, name=record["course"]).first()
        if course is None:
            course = Course(name=record["course"], university_id=university.id)
            db.add(course)
            db.flush()

        semester = db.query(Semester).filter_by(course_id=course.id, number=record["semester"]).first()
        if semester is None:
            semester = Semester(number=record["semester"], course_id=course.id)
            db.add(semester)
            db.flush()

        subject = db.query(Subject).filter_by(semester_id=semester.id, name=record["subject"]).first()
        if subject is None:
            subject = Subject(name=record["subject"], semester_id=semester.id)
            db.add(subject)
            db.flush()

        unit = db.query(Unit).filter_by(subject_id=subject.id, number=record["unit"]).first()
        if unit is None:
            unit = Unit(number=record["unit"], title=f"Unit {record['unit']}", subject_id=subject.id)
            db.add(unit)
            db.flush()

        document = db.query(Document).filter_by(title=record["title"]).first()
        if document is None:
            document = Document(
                title=record["title"],
                file_name=record["file_name"],
                document_type="notes",
                source="seed",
                university_id=university.id,
                course_id=course.id,
                semester_id=semester.id,
                subject_id=subject.id,
                unit_id=unit.id,
            )
            db.add(document)

    db.commit()
    return records


def get_documents(db: Session) -> list[dict]:
    documents = db.query(Document).order_by(Document.created_at.desc()).all()
    return [
        {
            "id": doc.id,
            "title": doc.title,
            "file_name": doc.file_name,
            "document_type": doc.document_type,
            "source": doc.source,
            "university": doc.university.name if doc.university else None,
            "course": doc.course.name if doc.course else None,
            "semester": doc.semester.number if doc.semester else None,
            "subject": doc.subject.name if doc.subject else None,
            "unit": doc.unit.number if doc.unit else None,
        }
        for doc in documents
    ]


def get_subjects(db: Session) -> list[dict]:
    subjects = db.query(Subject).order_by(Subject.name).all()
    return [
        {
            "id": subject.id,
            "name": subject.name,
            "semester": subject.semester.number if subject.semester else None,
            "course": subject.semester.course.name if subject.semester and subject.semester.course else None,
            "university": subject.semester.course.university.name if subject.semester and subject.semester.course and subject.semester.course.university else None,
        }
        for subject in subjects
    ]
