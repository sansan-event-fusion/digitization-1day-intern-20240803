import unicodedata


class CommonNormalizer:
    def normalize(self, data: str):
        return unicodedata.normalize("NFKC", data).strip()
