# main.py

from fastapi import BackgroundTasks, FastAPI, File, UploadFile, status, HTTPException
from typing import Annotated
from rag import pdf_text_extractor, vector_service

app = FastAPI()


@app.post("/upload")
async def file_upload_controller(
    file: Annotated[UploadFile, File(description="A file read as UploadFile")],
    bg_text_processor: BackgroundTasks,
):
    ...  # Raise a HTTPException if data upload is not a PDF file
    try:
        filepath = await save_file(file)
        bg_text_processor.add_task(pdf_text_extractor, filepath)
        bg_text_processor.add_task(
            vector_service.store_file_content_in_db,
            filepath.replace("pdf", "txt"),
            512,
            "knowledgebase",
            768,
        )

    except Exception as e:
        raise HTTPException(
            detail=f"An error occurred while saving file - Error: {e}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return {"filename": file.filename, "message": "File uploaded successfully"}
