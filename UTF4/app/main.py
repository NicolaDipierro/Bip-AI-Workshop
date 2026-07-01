import os
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from transformers import pipeline

# Inizializzazione di OpenTelemetry per Azure Application Insights (Modulo 4)
# Se la stringa di connessione è presente, traccia automaticamente le richieste
if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
    from azure.monitor.opentelemetry import configure_azure_monitor
    configure_azure_monitor()

app = FastAPI(
    title="Cloud-Native Azure AI Service",
    description="Microservizio AI di esempio per il Workshop Azure",
    version="1.0"
)

# Caricamento del modello di Sentiment Analysis (Leggero: ~260MB)
print("Loading AI Model (DistilBERT)...")
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
print("Model loaded successfully!")

class InferenceRequest(BaseModel):
    text: str

@app.get("/")
def health_check():
    """Endpoint di controllo integrità per Azure Container Apps."""
    return {"status": "healthy", "model": "distilbert-base-uncased", "timestamp": time.time()}

@app.post("/predict")
def predict(request: InferenceRequest):
    """Endpoint standard per l'inferenza (Modulo 1 & 2)."""
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    start_time = time.time()
    
    # Esecuzione dell'inferenza AI
    result = classifier(request.text)[0]
    
    latency = time.time() - start_time
    
    return {
        "text": request.text,
        "label": result["label"],
        "confidence": round(result["score"], 4),
        "inference_latency_seconds": round(latency, 4)
    }

@app.post("/predict/stream")
def predict_stream(request: InferenceRequest):
    """Endpoint in streaming (Server-Sent Events) (Modulo 2)."""
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    def token_generator():
        # Eseguiamo prima l'inferenza
        result = classifier(request.text)[0]
        response_text = f"Analysis complete. Label: {result['label']} (Confidence: {result['score']:.2f}). "
        
        # Simuliamo lo streaming dei token (parola per parola) generati dall'AI
        for word in response_text.split():
            yield f"data: {word} \n\n"
            time.sleep(0.15) # Delay per simulare la generazione in tempo reale

    return StreamingResponse(token_generator(), media_type="text/event-stream")