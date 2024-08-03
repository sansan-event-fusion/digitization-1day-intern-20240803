"""app.modules.normalizer.company_name
会社名のノーマライズを行うクラスを提供するモジュール。
"""
from functools import reduce

class BaseNormalizer:
    """Base
    ノーマライズの仕組みを提供する
    """
    RULES = []

    def normalize(self, value: str):
        return reduce(lambda v, f: f(v), self.RULES, value)
