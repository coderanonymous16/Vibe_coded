from pathlib import Path

from reportlab.pdfgen import canvas

from app.ingestion.ingestion_pipeline import ingest_pdf
from app.ingestion.metadata import DocumentMetadata
from app.rag.pipeline import RagPipeline


def _make_test_pdf(path: Path, content: str) -> None:
    c = canvas.Canvas(str(path))
    c.setTitle("DBMS Notes")
    c.drawString(100, 750, content)
    c.save()


def test_ingest_pdf_creates_chunk_metadata() -> None:
    pdf_path = Path(__file__).with_name("sample.pdf")
    _make_test_pdf(pdf_path, "Normalization is the process of organizing data to reduce redundancy.")
    try:
        chunks = ingest_pdf(pdf_path, DocumentMetadata(title="DBMS Notes", university="AKTU", course="B.Tech CSE", semester=6, subject="DBMS", unit=3), chunk_size=80, overlap=20)
        assert chunks
        assert chunks[0]["page"] >= 1
        assert chunks[0]["metadata"]["subject"] == "DBMS"
        assert chunks[0]["metadata"]["unit"] == 3
    finally:
        pdf_path.unlink(missing_ok=True)


def test_rag_pipeline_answers_with_context() -> None:
    chunks = [
        {"chunk_id": "c1", "text": "Normalization is the process of organizing data to reduce redundancy.", "page": 3, "metadata": {"title": "DBMS Notes", "subject": "DBMS", "unit": 3}},
        {"chunk_id": "c2", "text": "2NF is a normal form where every non-key attribute is fully dependent on the primary key.", "page": 5, "metadata": {"title": "DBMS Notes", "subject": "DBMS", "unit": 3}},
    ]
    pipeline = RagPipeline(chunks)
    result = pipeline.answer("What is normalization?", language="Hinglish", filters={"subject": "DBMS"})
    assert result["answer"]
    assert result["citations"]
    assert result["retrieved_chunks"]
