"""app.modules.normalizer.company_name
会社名のノーマライズを行うクラスを提供するモジュール。
"""
from functools import reduce
from app.models.normalizer.base import BaseNormalizer
from app.models.normalizer.rules import strip, nfkcNormalize, expandHoujinkakuAbb, noFollowingAlphaNum

class CompanyNameNormalizer(BaseNormalizer):
    """CompanyNameNormalizer
    会社名のノーマライズを行う。
    """
    RULES = [strip, nfkcNormalize, expandHoujinkakuAbb, noFollowingAlphaNum]
