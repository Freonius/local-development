from os import environ
from contextlib import suppress
from json import dumps
from fastapi import FastAPI
from uvicorn import run
from .schema import BasicResponse
from .utils import SecretsManager

if __debug__:
    # Let's set the local environment
    environ["AWS_ENDPOINT"] = "http://localhost:4566"
    environ["AWS_ACCESS_KEY"] = "localhost"
    environ["AWS_SECRET_ACCESS_KEY"] = "localhost"
    environ["AWS_DEFAULT_REGION"] = "eu-west-1"

sec_man: SecretsManager = SecretsManager()

if __debug__:
    with suppress(Exception):
        # It will throw an exception if the secret is already set
        # ...so we will suppress it
        sec_man.client.create_secret(
            Name="mySecret",
            SecretString=dumps(
                {
                    "host": "localhost",
                    "port": "5432",
                    "user": "localdev",
                    "password": "robinhood",
                    "name": "localdev",
                }
            ),
        )

sec_man.get_secrets("mySecret")

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
