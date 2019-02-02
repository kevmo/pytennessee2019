"""
    Code for interacting with the popular DNS sinkhole
"""

import asyncio
import sys

from operator import itemgetter
from typing import List
from collections import Counter

import requests
from whispers import _LOGGER
from .exceptions import SinkholeException

HOLE_TIMEOUT = 60  # Arbitrary timeout setting


class SinkholeQueryData:
    """
    Appdaemon container uses Python3.6 so copying code from connection for demo purposes.
    """

    def __init__(self, **kwargs):
        """
        Fetch data from sinkhole API
        """

        self.tls = kwargs["tls"]
        self.verify_tls = kwargs["verify_tls"]
        self.schema = kwargs["schema"]
        self.host = kwargs["host"]
        self.path = "admin"
        self.data = None
        self.auth = kwargs["auth"]
        if self.tls:
            self.schema = "https"
            self.base = (
                f"{self.schema}://{self.host}/{self.path}/api.php?auth={self.auth}"
            )
        else:
            self.base = (
                f"{self.schema}://{self.host}/{self.path}/api.php?auth={self.auth}"
            )

    def order_data(self) -> List:
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
            url = self.base + "&getAllQueries"
            _LOGGER.debug("Connecting to server at %s", url)
            response = requests.get(url, verify=self.verify_tls)
            self.data = response.json()
        except Exception as error:
            _LOGGER.error("Could not get data from sinkhole server: %s", error)
            raise SinkholeException

        _LOGGER.debug("Found data %s", self.data)
        desired = Counter([x[2] for x in self.data["data"] if x[4] == "2"])
        return sorted(desired.items(), key=itemgetter(1), reverse=True)
