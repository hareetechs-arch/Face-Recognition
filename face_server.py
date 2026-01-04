from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from deepface import DeepFace
import shutil
import uuid
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/verify-face")
async def verify_face(stored_image: UploadFile = File(...), live_image: UploadFile = File(...)):
    try:
        stored_path = f"{UPLOAD_DIR}/{uuid.uuid4()}_{stored_image.filename}"
        live_path = f"{UPLOAD_DIR}/{uuid.uuid4()}_{live_image.filename}"

        with open(stored_path, "wb") as buffer:
            shutil.copyfileobj(stored_image.file, buffer)
        with open(live_path, "wb") as buffer:
            shutil.copyfileobj(live_image.file, buffer)

        stored_image.file.close()
        live_image.file.close()

        result = DeepFace.verify(
            img1_path=stored_path,
            img2_path=live_path,
            model_name="ArcFace",
            detector_backend="retinaface",
            distance_metric="cosine",
            enforce_detection=False
        )

        os.remove(stored_path)
        os.remove(live_path)

        return {
            "success": result["verified"],
            "distance": result["distance"]
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})
