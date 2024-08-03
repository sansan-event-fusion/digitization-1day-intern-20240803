"""app.models.normalizer.address
住所のノーマライズを行うクラスを提供するモジュール。
"""

from app.models.normalizer.base import BaseNormalizer
from app.models.normalizer.rules import strip, nfkcNormalize, noFollowingAlpha, noPrefix

class AddressNormalizer(BaseNormalizer):
    RULES = [strip, nfkcNormalize, noFollowingAlpha, noPrefix]
