from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(
    title="AI Foundry API",
    description="API utilizzata per il laboratorio Docker",
    version="1.0.0"
)

endpoint = "https://uf2-foundry.services.ai.azure.com/openai/v1"
deployment_name = "gpt-5.4-nano"


class AskRequest(BaseModel):
    text: str
    foundry_key: str


@app.get("/")
def healthcheck():
    return {
        "status": "running",
        "service": "foundry-ai-api"
    }


@app.post("/ask")
def ask(request: AskRequest):

    client = OpenAI(
        base_url=endpoint,
        api_key=request.foundry_key
    )

    completion = client.chat.completions.create(
        model=deployment_name,
        messages=[{"role": "user", "content": request.text}],
    )

    # The chat completion content is available at completion.choices[0].message.content
    return {
        "input": request.text,
        "response": completion.choices[0].message.content
    }
    