from typing import List
from fastapi import APIRouter, UploadFile, File
import shutil
from pathlib import Path
from rag.services.index_service import IndexService
from rag.services.knowledge_service import KnowledgeService

knowledge_service = KnowledgeService()


index_service = IndexService()


router = APIRouter(
    prefix="/knowledge",
    tags=["Knowledge"]
)

UPLOAD_DIR = Path("rag/docs/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload")
async def upload_documents(
    files: List[UploadFile] = File(...)
):
    uploaded = []

    for file in files:
        destination = UPLOAD_DIR / file.filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        uploaded.append(file.filename)

    return {
        "success": True,
        "uploaded": uploaded
    }

@router.post("/index")
def generate_index():
    return index_service.build_index()

@router.get("/documents")
def get_documents():
    return knowledge_service.list_documents()