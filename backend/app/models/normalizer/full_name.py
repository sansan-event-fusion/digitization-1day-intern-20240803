"""app.models.normalizer.name
氏名のノーマライズを行うクラスを提供するモジュール。
"""
import re

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

        # 氏名 + ()のものはかっこを削除
        full_name = full_name.split('(')[0]
        full_name = full_name.split('（')[0]
        


        titles = ['Mr.', 'Mrs.', 'Dr.']
        for title in titles:
            if title in full_name:
                full_name = full_name.replace(title, '')
                break
        jp = []
        en = []
        # 日本語と英語を区別する正規表現パターン
        japanese_pattern = re.compile(r'[\u3040-\u30FF\u4E00-\u9FFF]')
        
        for name in full_name.split():
            # 日本語の文字が含まれているかどうかをチェック
            if japanese_pattern.search(name):
                jp.append(name)
            else:
                en.append(name)
                
        if jp and en:
            full_name = ' '.join(jp)

        

        return full_name.strip()
