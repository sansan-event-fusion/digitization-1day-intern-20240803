"""app.models.normalizer.name
氏名のノーマライズを行うクラスを提供するモジュール。
"""
import unicodedata

class FullNameNormalizer:
    """FullNameNormalizer
    氏名のノーマライズを行う。
    """

    def normalize(self, full_name: str):
        """normalize
        氏名をノーマライズする。
        Args:
                text (str): ノーマライズ対象の氏名。
        Returns:
                str: ノーマライズ後の氏名。
        Example:
                >>> NameNormalizer().normalize(" 田中　太郎 ")
                "田中　太郎"
        """
        
        #full_name = unicodedata.normalize('NFKC', full_name)
        full_name = full_name.replace("(Dr.)", "").replace("(Mr.)", "").replace("Dr.", "").replace("Mr.", "")
        return full_name.strip()
