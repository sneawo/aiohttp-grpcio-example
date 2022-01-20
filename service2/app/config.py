import os


class Config:
    DEBUG = bool(os.environ.get("DEBUG", False))
    PORT = int(os.environ.get("PORT", 8080))
    SERVICE1_CHANNEL = os.environ.get("SERVICE1_CHANNEL", "service1:50051")

    def __str__(self):
        return f"debug={self.DEBUG}, port={self.PORT}, service1_channel={self.SERVICE1_CHANNEL}"
