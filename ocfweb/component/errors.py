from requests import models


class ResponseException(Exception):

    def __init__(self, response: models.Response) -> None:
        self.response = response
