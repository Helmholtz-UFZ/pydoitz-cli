import pydoitz
from pydoitz.client import IDoitClient


class Application:

    def __init__(self, *args, **kwargs):
        self.api = IDoitClient(*args, **kwargs)
        self.category_config = None
        self.category_opts = {}
        self.verbose = 0
