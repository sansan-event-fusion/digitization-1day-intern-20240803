KANJI_NUMBERS_MAP = {
    "〇": 0,
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
    "百": 100,
    "千": 1000,
}


class KanjiNumberConverter:
    @staticmethod
    def kanji_to_arabic(text: str) -> str:
        """漢数字をアラビア数字に変換する

        Args:
            text (str): 変換対象のテキスト

        Returns:
            str: アラビア数字に変換されたテキスト
        """

        def convert_kanji_to_arabic_segment(kanji_segment: str) -> str:
            """漢数字のセグメントをアラビア数字に変換する

            Args:
                kanji_segment (str): 漢数字のセグメント

            Returns:
                str: アラビア数字に変換されたセグメント
            """
            num = 0
            tmp = 0
            for char in kanji_segment:
                if char in KANJI_NUMBERS_MAP:
                    val = KANJI_NUMBERS_MAP[char]
                    if val in [10, 100, 1000]:
                        if tmp == 0:
                            tmp = 1  # 十、百、千の前に数がない場合は1とみなす
                        num += tmp * val
                        tmp = 0
                    else:
                        tmp = tmp * 10 + val  # 単位の前の数字を更新
            num += tmp
            return str(num)

        kanji_numerals = "".join(KANJI_NUMBERS_MAP.keys())
        segments = []

        # 漢数字のグループを一時的に保持するバッファ
        # バッファに溜まった段階で変換を行う
        buffer = []

        for char in text:
            if char in kanji_numerals:
                buffer.append(char)
            else:
                if buffer:
                    segments.append(convert_kanji_to_arabic_segment("".join(buffer)))
                    buffer = []
                segments.append(char)

        if buffer:
            segments.append(convert_kanji_to_arabic_segment("".join(buffer)))

        return "".join(segments)
