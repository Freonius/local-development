from os import environ
from json import loads
from contextlib import suppress
from typing import TYPE_CHECKING
from boto3 import client

if TYPE_CHECKING is True:
    from boto3_type_annotations.secretsmanager.client import Client


class SecretsManager:
    _client: "Client"

    def __init__(self) -> None:
        self._client: "Client" = client(
            "secretsmanager",
            aws_access_key_id=environ.get("AWS_ACCESS_KEY", None),
            aws_secret_access_key=environ.get("AWS_SECRET_ACCESS_KEY", None),
            region_name=environ.get("AWS_DEFAULT_REGION", None),
            endpoint_url=environ.get("AWS_ENDPOINT", None),
        )

    def get_secrets(self, name: str) -> None:
        res = self._client.get_secret_value(SecretId=name)
        secret = loads(res["SecretString"])
        if not isinstance(secret, dict):
            raise TypeError("secret was not a dictionary")
        for _key in (
            "host",
            "port",
            "user",
            "password",
            "name",
        ):
            if _key not in secret:
                raise KeyError(f"key {_key} was not in secret")
        environ[
            "DB_URI"
        ] = f'postgresql+psycopg2://{secret["user"]}:{secret["password"]}@{secret["host"]}:{secret["port"]}/{secret["name"]}'

    @property
    def client(self) -> "Client":
        return self._client

    def __del__(self) -> None:
        with suppress(Exception):
            self._client.close()
