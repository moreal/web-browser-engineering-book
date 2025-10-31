from browser.cache import MemoryCache
from browser.connection_factory import ConnectionFactory
from browser.content_fetcher import ContentFetcher
from browser.handler_factory import HandlerFactory


GlobalMemoryCache = MemoryCache()
GlobalConnectionFactory = ConnectionFactory()
GlobalHandlerFactory = HandlerFactory()
GlobalContentFetcher = ContentFetcher()
