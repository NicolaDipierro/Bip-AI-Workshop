from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI(
    title="Fake AI Prediction API",
    description="API utilizzata per il laboratorio Docker",
    version="1.0.0"
)


class PredictionRequest(BaseModel):
    text: str


@app.get("/")
def healthcheck():
    return {
        "status": "running",
        "service": "fake-ai-api"
    }


@app.post("/predict")
def predict(request: PredictionRequest):

    sentiment = random.choice([
        "Positive",
        "Negative",
        "Neutral"
    ])

    confidence = round(random.uniform(0.75, 0.99), 2)

    return {
        "input": request.text,
        "prediction": sentiment,
        "confidence": confidence
    }