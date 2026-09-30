from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DocumentMetadata:
    title: str
    university: str | None = None
    course: str | None = None
    semester: int | None = None
    subject: str | None = None
    unit: int | None = None
    document_type: str = "notes"
    source: str = "admin_upload"

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "university": self.university,
            "course": self.course,
            "semester": self.semester,
            "subject": self.subject,
            "unit": self.unit,
            "document_type": self.document_type,
            "source": self.source,
        }
