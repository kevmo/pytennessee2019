import logging
from os import getenv

_LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=getenv("LOG_LEVEL", default="INFO"))
