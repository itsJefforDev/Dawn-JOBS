import os
from PyPDF2 import PdfReader
from sqlalchemy.orm import Session
from app.models.cv import CV

UPLOAD_FOLDER = "uploads"


def extract_text_from_pdf(file_path: str):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


def save_cv(db: Session, user_id: int, file):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = f"{UPLOAD_FOLDER}/{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    extracted_text = extract_text_from_pdf(file_path)

    cv = CV(
        user_id=user_id,
        file_name=file.filename,
        file_path=file_path,
        extracted_text=extracted_text
    )

    db.add(cv)
    db.commit()
    db.refresh(cv)

    return cv


def get_cv(db: Session, user_id: int):
    return db.query(CV).filter(CV.user_id == user_id).first()


def delete_cv(db: Session, user_id: int):
    cv = get_cv(db, user_id)

    if not cv:
        return None

    if os.path.exists(cv.file_path):
        os.remove(cv.file_path)

    db.delete(cv)
    db.commit()

    return {"message": "CV deleted successfully"}