# 動作確認方法

0. `python` のバージョンは `^3.11` を使用します
   - `./pyproject.toml` でプロジェクトに設定しています
1. `poetry` をインストールします
   - `pip install poetry`
2. 依存関係をインストールして仮想環境を有効にします
   - `poetry install`
3. アプリケーションを起動します
   - `poetry run uvicorn app.main:app --reload`

# ディレクトリ構成
```shell
backend/
├── README.md
├── app
│   ├── main.py
│   ├── models
│   │   ├── entry.py # 名刺のデータ化項目に関するデータ
│   │   ├── inspector #インスペクターに関する処理
│   │   │   ├── base.py
│   │   │   ├── extra_inspector.py
│   │   │   ├── hands_on_inspector.py
│   │   │   ├── inspector.py
│   │   │   └── test_inspector.py
│   │   ├── normalizer #ノーマライザーに関する処理
│   │   │   ├── address.py
│   │   │   ├── common.py
│   │   │   ├── company_name.py
│   │   │   ├── email.py
│   │   │   ├── entries.py
│   │   │   ├── full_name.py
│   │   │   ├── position_name.py
│   │   │   ├── test_address.py
│   │   │   ├── test_company_name.py
│   │   │   ├── test_email.py
│   │   │   ├── test_full_name.py
│   │   │   └── test_position_name.py
│   │   └── virtual_card.py # データ化中の名刺に関するデータ
│   ├── repositories
│   │   ├── base.py
│   │   ├── correct.py
│   │   ├── delivered.py
│   │   ├── inspector.py
│   │   └── virtual_card.py
│   ├── router
│   │   ├── delivered.py
│   │   ├── inspector.py
│   │   ├── normalizer.py
│   │   └── virtual_card.py
│   └── schemas
│   　　   ├── entry.py
│   　　   └── virtual_card.py
├── poetry.lock
├── pyproject.toml
├── static
│   ├── correct　 #正解データ
│   ├── delivered #データ化済みの名刺データ
│   ├── images #名刺画像
│   ├── inspectors #インスペクターを通過した名刺データ
│   └── virtual_cards #OCRの結果データ
└── tools
    └── scoring # 採点ツール
```
