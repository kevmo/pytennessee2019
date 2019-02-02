"""
    Code for interacting with the popular DNS sinkhole
"""

import asyncio
import sys

from operator import itemgetter
from typing import List
from collections import Counter
from dataclasses import dataclass

import aiohttp
import async_timeout

from whispers import _LOGGER
from .exceptions import SinkholeException

HOLE_TIMEOUT = 60  # Arbitrary timeout setting


@dataclass
class SinkholeQueryData:
    """
    Fetch data from sinkhole API
    """

    loop: None
    tls: bool = False
    verify_tls: bool = True
    schema: str = "http"
    host: str = "pi.hole"
    path: str = "admin"
    data: List = None
    auth: str = None

    def __post_init__(self) -> None:
        if self.tls:
            self.schema = "https"
            self.base = (
                f"{self.schema}://{self.host}/{self.path}/api.php?auth={self.auth}"
            )
        else:
            self.base = (
                f"{self.schema}://{self.host}/{self.path}/api.php?auth={self.auth}"
            )

    async def order_data(self) -> List:
        """
        Only care about hostname in response from API

        https://discourse.pi-hole.net/t/pi-hole-api/1863

        From FTL source code:
        ssend(*sock,"%i %s %s %s %i %i %i %lu\n",
          queries[i].timestamp,
          qtype,
          domain,
          client,
          queries[i].status,
          queries[i].dnssec,
          queries[i].reply,
          delay);
        """

        try:
            async with async_timeout.timeout(HOLE_TIMEOUT, loop=self.loop):
                url = self.base + "&getAllQueries"
                _LOGGER.debug("Connecting to server at %s", url)
                async with aiohttp.ClientSession() as session:
                    response = await session.get(url, verify_ssl=self.verify_tls)
                    _LOGGER.debug(
                        "Response from sinkhole server is %s", response.status
                    )
                    self.data = await response.json()
        except (asyncio.TimeoutError, aiohttp.ClientError) as error:
            _LOGGER.error("Could not get data from sinkhole server: %s", error)
            raise SinkholeException

        _LOGGER.debug("Found data %s", self.data)
        desired = Counter([x[2] for x in self.data["data"] if x[4] == "2"])
        return sorted(desired.items(), key=itemgetter(1), reverse=True)
