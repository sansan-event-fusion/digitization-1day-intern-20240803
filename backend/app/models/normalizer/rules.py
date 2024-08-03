import unicodedata
import re

def nfkcNormalize(v: str) -> str:
    return unicodedata.normalize("NFKC", v)

def expandHoujinkakuAbb(v: str) -> str:
    v = re.sub(r"^(\(有\)|（有）)|(\(有\)|（有）)$", "有限会社", v)
    v = re.sub(r"^(\(株\)|（株）)|(\(株\)|（株）)$", "株式会社", v)
    # v = re.sub(r"([^株])式会社$", r"\1", v)
    return v

def noPronounce(v: str) -> str:
    # 肩書き的なものが残っていたら飛ばす
    if ("manager" in v.lower()):
        return v
    v = re.sub(r"^([^a-zA-Z0-9-\/]+?)\s?[A-Za-z\/., ()-]*$", r"\1", v)
    return v

def noFollowingAlpha(v: str) -> str:
    v = re.sub(r"^([^a-zA-Z0-9-\/]+?)\s?[A-Za-z\/., ()-]*$", r"\1", v)
    return v

def noFollowingAlphaNum(v: str) -> str:
    v = re.sub(r"^([^a-zA-Z\/]+?)\s?[A-Za-z0-9\/., ()-]*$", r"\1", v)
    return v

def noHonorificTitle(v: str) -> str:
    v = re.sub(r"^(Dr\.|Mr\.)\s*", "", v)
    return v

def commonEmail(v: str) -> str:
    v = v.lower().replace(",", ".")
    return v

def noPrefix(v: str) -> str:
    v = re.sub(r"^(email|address): *", "", v, flags=re.IGNORECASE)
    return v

def strip(v: str) -> str:
    return v.strip()

