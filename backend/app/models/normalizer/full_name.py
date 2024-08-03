"""app.models.normalizer.name
氏名のノーマライズを行うクラスを提供するモジュール。
"""

from app.models.normalizer.base import BaseNormalizer
from app.models.normalizer.rules import strip, nfkcNormalize, noFollowingAlphaNum, noHonorificTitle

class FullNameNormalizer(BaseNormalizer):
    """FullNameNormalizer
    氏名のノーマライズを行う。
    """

    RULES = [strip, nfkcNormalize, noFollowingAlphaNum, noHonorificTitle]
