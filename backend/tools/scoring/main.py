from start import StartCommand
from test import TestCommand
import argparse
import requests
import time


def main(args):
    check_server_status()

    # データ化開始
    start_command = StartCommand()
    try:
        start_command.execute(args.id)
    except Exception as e:
        print("\u001b[31m" + "データ化開始に失敗しました" + "\u001b[0m")
        print(e)
        exit()

    # 2秒待機
    print("データ化中...")
    time.sleep(2)

    # テスト
    test_command = TestCommand()
    try:
        test_command.execute(args.id)
    except Exception as e:
        print(
            "\u001b[31m"
            + "テストに失敗しました。サーバーのログを確認し、エラーが出ていないか確認してください"
            + "\u001b[0m"
        )
        print(e)
        exit()


def check_server_status():
    url = "http://localhost:8000"

    try:
        response = requests.get(url)
        response.raise_for_status()
        print("\u001b[32m" + "サーバーは起動しています。" + "\u001b[0m")
    except requests.exceptions.RequestException:
        print(
            "\u001b[31m"
            + "サーバーは起動していません。サーバーのログを確認してください"
            + "\u001b[0m"
        )
        exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--id", type=int, help="テストケースのID", nargs="?", default=None
    )

    args = parser.parse_args()

    main(args)
