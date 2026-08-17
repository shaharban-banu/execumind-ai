from typing import List
from fastapi import APIRouter, UploadFile, File,Depends
import shutil
from pathlib import Path
from rag.services.index_service import IndexService
from rag.services.knowledge_service import KnowledgeService
from app.auth.dependencies import get_current_user

knowledge_service = KnowledgeService()


index_service = IndexService()


router = APIRouter(
    prefix="/knowledge",
    tags=["Knowledge"]
)


@router.post("/upload")
async def upload_documents(
    files: List[UploadFile] = File(...),
    user=Depends(get_current_user)
):
    
    UPLOAD_DIR = Path(f"data/users/{user.id}/uploads")
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
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
def generate_index(user=Depends(get_current_user)):
    return index_service.build_index(user.id)

@router.get("/documents")
def get_documents(user=Depends(get_current_user)):
    return knowledge_service.list_documents(user.id)