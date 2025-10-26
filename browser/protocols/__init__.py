import re
import os
import dataclasses

from .http.connection import HttpConnection
from .http.request import HttpRequest
from .https.connection import HttpsConnection

from browser.url import Url, ConcreteUrl, DataUrl, FileUrl, HttpUrl, to_concrete


def create_connection(url: HttpUrl) -> HttpConnection | HttpsConnection:
    match url.scheme:
        case "http":
            return HttpConnection(url.host, url.port)
        case "https":
            return HttpsConnection(url.host, url.port)


def http_handler(url: HttpUrl) -> str:
    assert url.scheme == "http" or url.scheme == "https"
    assert url.host is not None

    connection = create_connection(url)
    request = HttpRequest(
        method="GET",
        path=url.path or "/",
        headers={
            "Host": url.host,
        },
        version="1.1",
    )
    response = connection.send(request)

    if 300 <= response.status_code < 400:
        location_header_value = response.headers["location"]
        if re.match(r"^[^:/]+://", location_header_value):
            redirect_url = Url.parse(location_header_value)
        else:
            next_path = os.path.join(url.path, location_header_value)
            redirect_url = dataclasses.replace(url, path=next_path)

        redirect_url = to_concrete(redirect_url)
        return handle_url(redirect_url)
    else:
        return response.body


def file_handler(url: FileUrl) -> str:
    assert url.path is not None

    with open(url.path, "r") as file:
        return file.read()


def data_handler(url: DataUrl) -> str:
    data = url.get_data()
    if isinstance(data, bytes):
        raise ValueError("Binary data not supported yet.")

    return data


def handle_url(url: ConcreteUrl) -> str:
    match url:
        case HttpUrl():
            return http_handler(url)
        case FileUrl():
            return file_handler(url)
        case DataUrl():
            return data_handler(url)
