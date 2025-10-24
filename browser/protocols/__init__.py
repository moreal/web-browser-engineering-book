from .http.connection import HttpConnection
from .http.request import HttpRequest
from .https.connection import HttpsConnection

from browser.url import URL, ConcreteUrl, DataURL, FileURL, HttpURL, to_concrete


def create_connection(url: HttpURL) -> HttpConnection | HttpsConnection:
    match url.scheme:
        case "http":
            return HttpConnection(url.host, url.port)
        case "https":
            return HttpsConnection(url.host, url.port)


def http_handler(url: HttpURL) -> str:
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
        redirect_url = to_concrete(URL.parse(response.headers["location"]))
        return handle_url(redirect_url)
    else:
        return response.body


def file_handler(url: FileURL) -> str:
    assert url.path is not None

    with open(url.path, "r") as file:
        return file.read()


def data_handler(url: DataURL) -> str:
    data = url.get_data()
    if isinstance(data, bytes):
        raise ValueError("Binary data not supported yet.")

    return data


def handle_url(url: ConcreteUrl) -> str:
    match url:
        case HttpURL():
            return http_handler(url)
        case FileURL():
            return file_handler(url)
        case DataURL():
            return data_handler(url)
