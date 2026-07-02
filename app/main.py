from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from app.extractor import extract_text
from app.parser import parse_resume

import tempfile
import os

app = FastAPI(title="Resume Parser API")


@app.get("/")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/parse-resume")
async def parse_resume_endpoint(file: UploadFile = File(...)) -> JSONResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    suffix = file.filename.lower().split(".")[-1]
    if suffix not in {"pdf", "docx"}:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")

    contents = await file.read()
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmpf:
            tmpf.write(contents)
            tmp = tmpf.name

        raw_text = extract_text(tmp)
        parsed = parse_resume(raw_text)
        return JSONResponse(content=parsed)
    except Exception as exc:  # pragma: no cover - defensive path
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    finally:
        try:
            if tmp and os.path.exists(tmp):
                os.unlink(tmp)
        except Exception:
            pass
