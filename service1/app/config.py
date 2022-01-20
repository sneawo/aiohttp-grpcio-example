import os


class Config:
    DEBUG = bool(os.environ.get("DEBUG", False))
    PORT = int(os.environ.get("PORT", 8080))

    def __str__(self):
        return f"debug={self.DEBUG}, port={self.PORT}"
