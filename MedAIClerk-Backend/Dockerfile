FROM pytorch/pytorch:2.3.0-cpu

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1         PORT=8000         LLM_MODE=api         OPENAI_MODEL=gpt-4o-mini         OSS_MODEL_ID=openai/gpt-oss-20b         OSS_DEVICE=cpu         OSS_MAX_NEW_TOKENS=512         OSS_TEMPERATURE=0.2

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
