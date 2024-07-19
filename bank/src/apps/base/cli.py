import betterlogging
import ssl
from typing import Literal, Optional, Any, Mapping
import xml.etree.ElementTree as ET

from aiohttp import ClientSession, TCPConnector


class APIClient:
    def __init__(self, base_url) -> None:
        self._base_url = base_url
        self._session: ClientSession | None = None
        self.log = betterlogging.getLogger(self.__class__.__name__)

    async def _get_session(self) -> ClientSession:
        """Get aiohttp session with cache."""
        if self._session is None:
            ssl_context = ssl.SSLContext()
            connector = TCPConnector(ssl_context=ssl_context)
            self._session = ClientSession(
                base_url=self._base_url,
                connector=connector,
            )

        return self._session

    async def __aenter__(self):
        self._session = await self._get_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()
        self._session = None

    async def _make_request(
            self,
            method: Literal["GET"],
            url: str,
            params: Optional[Mapping[str, Any]] = None,
    ) -> ET.Element:
        """
        :param method: Method for request GET or POST
        :param params: Query params for request
        :param url: would be added to base url string
        """

        async with self._session.request(
                method, url, params=params
        ) as response:
            try:
                text = await response.text()
                result = ET.fromstring(text)
            except Exception as e:
                self.log.exception(e)
                self.log.info(f"{await response.text()}")
                raise e

        return result
