# MedAI Clerk 🏥🤖

An AI-powered medical documentation assistant for healthcare professionals.  
Built for the **OpenAI OSS Hackathon 2025**.

---

## 🌟 What it does
MedAI Clerk helps clinicians turn **unstructured patient notes** into:
- **Structured SOAP notes**
- **Suggested ICD-10 codes** with justifications

This reduces paperwork burden and speeds up clinical workflows.

---

## 🚀 Features
- Dual-mode **LLM backend**:
  - `LLM_MODE=api`: Uses OpenAI API (`gpt-4o-mini` by default)
  - `LLM_MODE=oss`: Runs **GPT-OSS** locally via Hugging Face (20B open-weight model)
  - `LLM_MODE=oss` + `OSS_QUANT=4bit|8bit`: Runs GPT-OSS quantized on GPU (smaller + faster)
- Frontend: Next.js dashboard for doctors
- Backend: FastAPI with endpoints for SOAP and ICD code generation
- Dockerized full stack (frontend + backend)

---

## 📂 Project Structure
```
MedAIClerk-Backend/     # FastAPI backend + LLM provider
medai-clerk-frontend/   # Next.js frontend
docker-compose.yml
README.md
```

---

## 🛠️ Setup

### 1. Clone repo
```bash
git clone <https://github.com/annezeal2306/MedAIClerk.git>
cd MedAIClerk
```

### 2. Environment variables
Create `.env` beside `docker-compose.yml`:

#### API mode (default)
```env
OPENAI_API_KEY=sk-...yourkey...
LLM_MODE=api
```

#### OSS mode (local GPT-OSS)
```env
LLM_MODE=oss
OSS_MODEL_ID=openai/gpt-oss-20b
OSS_DEVICE=cpu        # or "cuda" for GPU
OSS_MAX_NEW_TOKENS=512
OSS_TEMPERATURE=0.2
```

#### Quantized OSS (GPU only)
```env
LLM_MODE=oss
OSS_DEVICE=cuda
OSS_QUANT=4bit
OSS_MODEL_ID=openai/gpt-oss-20b
```

### 3. Model download (for OSS)
Download GPT-OSS weights from Hugging Face:
```bash
git lfs install
git clone https://huggingface.co/openai/gpt-oss-20b models/gpt-oss-20b
```

Mount cache in `docker-compose.yml`:
```yaml
volumes:
  - ./models:/root/.cache/huggingface
```

### 4. Run
```bash
docker compose up -d --build
```

- Frontend → http://localhost:3000  
- Backend → http://localhost:8000  

---

## 🧪 API Endpoints

### Generate SOAP note
```bash
curl -X POST http://localhost:8000/api/generate-soap-note       -H "Content-Type: application/json"       -d '{"notes":"Patient reports chest pain for 2 days, worse on exertion."}'
```

### Suggest ICD codes
```bash
curl -X POST http://localhost:8000/api/suggest-icd-codes       -H "Content-Type: application/json"       -d '{"soap_note":"Subjective: ... Objective: ... Assessment: ... Plan: ..."}'
```

---

## 🏆 Hackathon Checklist

✅ Backend supports **OSS GPT-OSS** (20B)  
✅ Quantization (4bit/8bit) support for GPUs  
✅ API fallback with OpenAI GPT-4o-mini  
✅ Frontend for user-friendly doctor dashboard  
✅ Dockerized full stack  
✅ Clear README for judges  

---

## 📹 Demo
(Add screenshots or link to demo video here)

---

## 📜 License
Apache 2.0 — aligns with GPT-OSS license.
