from pathlib import Path

class KnowledgeService:

    UPLOAD_DIR = Path("rag/docs/uploads")

    def list_documents(self):

        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

        documents = []

        for file in self.UPLOAD_DIR.iterdir():

            if file.is_file():

                documents.append({
                    "name": file.name,
                    "size": round(file.stat().st_size / 1024 / 1024, 2),
                    "uploaded_at": file.stat().st_mtime
                })

        return documents