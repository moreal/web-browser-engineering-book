from dataclasses import dataclass
from typing import overload
from browser.connection_factory import ConnectionFactory, GlobalConnectionFactory
from browser.protocols.data.handler import DataUrlHandler
from browser.protocols.file.handler import FileUrlHandler
from browser.protocols.http.handler import HttpHandler
from browser.url import ConcreteUrl, DataUrl, FileUrl, HttpFamilyUrl


@dataclass(frozen=True)
class HandlerFactory:
    connection_factory: ConnectionFactory = GlobalConnectionFactory

    @overload
    def get(self, url: HttpFamilyUrl) -> HttpHandler: ...
    @overload
    def get(self, url: FileUrl) -> FileUrlHandler: ...
    @overload
    def get(self, url: DataUrl) -> DataUrlHandler: ...
    def get(self, url: ConcreteUrl) -> HttpHandler | FileUrlHandler | DataUrlHandler:
        match url:
            case HttpFamilyUrl():
                return HttpHandler(self.connection_factory)
            case FileUrl():
                return FileUrlHandler()
            case DataUrl():
                return DataUrlHandler()


GlobalHandlerFactory = HandlerFactory()
