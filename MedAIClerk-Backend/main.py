import os
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from llm_provider import LLM

load_dotenv()

app = FastAPI()
origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = LLM()

class PatientNotes(BaseModel):
    notes: str

class IcdBody(BaseModel):
    soap_note: Optional[str] = None
    notes: Optional[str] = None

@app.get("/health")
async def health():
    return {"status": "ok", "mode": os.getenv("LLM_MODE", "api")}

@app.post("/api/generate-soap-note")
async def generate_soap_note(patient_notes: PatientNotes):
    text = (patient_notes.notes or "").strip()
    if len(text) < 10:
        raise HTTPException(status_code=400, detail="Patient notes must be at least 10 characters long.")
    prompt = f"""
    You are an AI assistant designed to help medical professionals.
    Convert the following into a structured SOAP note with headings:
    Subjective, Objective, Assessment, Plan.

    Notes:
    {text}
    """.strip()
    try:
        content = llm.generate(prompt)
        return {"soap_note": content}
    except Exception as e:
        print("LLM error (SOAP):", repr(e))
        raise HTTPException(status_code=500, detail=f"LLM error: {e}")

@app.post("/api/suggest-icd-codes")
async def suggest_icd_codes(body: IcdBody):
    text = (body.soap_note or body.notes or "").strip()
    if len(text) < 10:
        raise HTTPException(status_code=400, detail="Provide a SOAP note or notes of at least 10 characters.")
    prompt = f"""
    Based on the following clinical text, identify the most relevant ICD-10 codes.
    For each code, provide a brief justification.

    Clinical Text:
    {text}

    ---
    Respond ONLY in this format:
    Code: <ICD-10 Code> - <Description>
    Justification: <reason>
    """.strip()
    try:
        content = llm.generate(prompt)
        return {"icd_codes": content}
    except Exception as e:
        print("LLM error (ICD):", repr(e))
        raise HTTPException(status_code=500, detail=f"LLM error: {e}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
