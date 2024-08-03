"""app.models.normalizer.email
メールアドレスのノーマライズを行うクラスを提供するモジュール。
"""

from app.models.normalizer.base import BaseNormalizer
from app.models.normalizer.rules import strip, nfkcNormalize, commonEmail, noPrefix

class EmailNormalizer(BaseNormalizer):
    RULES = [strip, nfkcNormalize, commonEmail, noPrefix]


