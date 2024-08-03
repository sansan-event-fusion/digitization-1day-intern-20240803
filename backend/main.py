import re


def to_address(text: str) -> str:
    address_regex = re.compile(
        r"(...??[都道府県])((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|那須塩原|東村山|武蔵村山|羽村|十日町|上越|富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|廿日市|下松|岩国|田川|大村)市|.+?郡(?:玉村|大町|.+?)[町村]|.+?市.+?区|.+?[市区町村])(.+)"
    )

    prefactures, city, block = re.findall(address_regex, text)[0]

    return prefactures, city, block


addresses = [
    "神奈川県横浜市⻄区三丁目五番地十一号",
    "福岡県福岡市東区九ー二三番地一号",
    "神奈川県川崎市幸区新川崎一丁目六番地五号 ウォーターゲートビル10階",
    "大阪府大阪市北区梅田3-3-10 (3-3-10 Umeda, Kita-ku, Osaka)",
]


for address in addresses:
    print(to_address(address))
