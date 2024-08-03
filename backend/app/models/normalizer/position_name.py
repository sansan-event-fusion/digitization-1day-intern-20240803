"""app.models.normalizer.position_name
役職名のノーマライズを行うクラスを提供するモジュール。
"""


from app.models.normalizer.base import BaseNormalizer
from app.models.normalizer.rules import strip, nfkcNormalize, noPronounce

class PositionNameNormalizer(BaseNormalizer):
    RULES = [strip, nfkcNormalize, noPronounce]

