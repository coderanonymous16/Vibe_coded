from __future__ import annotations

from app.ingestion.ingestion_pipeline import ingest_pdf


class IngestionWorker:
    def __init__(self):
        self.jobs: list[dict] = []

    def enqueue(self, file_path: str, metadata: dict, chunk_size: int = 500, overlap: int = 80) -> dict:
        job = {"file_path": file_path, "metadata": metadata, "status": "queued", "chunk_size": chunk_size, "overlap": overlap}
        self.jobs.append(job)
        return job

    def run_next(self) -> dict | None:
        if not self.jobs:
            return None
        job = self.jobs.pop(0)

        class Meta:
            def __init__(self, payload):
                self.payload = payload

            def to_dict(self):
                return self.payload

        chunks = ingest_pdf(job["file_path"], metadata=Meta(job["metadata"]), chunk_size=job["chunk_size"], overlap=job["overlap"])
        job["status"] = "completed"
        job["chunks"] = chunks
        return job
