from fastapi import FastAPI
from uvicorn import run
from .schema import BasicResponse

app: FastAPI = FastAPI()


@app.get(
    "/message",
    description="Provides an hopeful message",
    response_model=BasicResponse,
)
async def message():
    """This function provides an helpful message"""
    return {
        "message": "Give me your tired, your poor, Your huddled masses yearning to breathe free",
    }


if __name__ == "__main__":
    run(app, host="0.0.0.0")
