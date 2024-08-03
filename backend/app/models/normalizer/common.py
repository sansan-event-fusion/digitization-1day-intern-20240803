import unicodedata
import re

class CommonNormalizer:
    def normalize(self, data: str):
        # この場合は、最初のブロックだけresultとして残す
        # ABC あいうえお -> ABC
        result = data
        if re.search(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9faf\uF900-\uFAFF]', data) and re.search(r'[A-Za-z]', data):
            if not any(exception in data for exception in ["CFO", "Manager", "F"]):
                try:
                    result = data.split()[0]
                    print(result)
                except:
                    pass
        result = unicodedata.normalize("NFKC", result).strip()
        return result
