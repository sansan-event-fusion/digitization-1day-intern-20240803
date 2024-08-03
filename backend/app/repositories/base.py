from pydantic import BaseModel
from typing import Any, Generic, List, TypeVar
import json
import os


T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T]):
    def __init__(self, path: str):
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def __read_json_file(self, file_path: str) -> Any | None:
        try:
            with open(file_path, "r", encoding="utf-8_sig") as file:
                content = json.load(file)
                return content
        except FileNotFoundError:
            print(f"File {file_path} not found")
            return None
        except json.JSONDecodeError:
            print(f"File {file_path} is not a valid JSON file")
            return None

    def get(self, id) -> Any | None:
        file_path = os.path.join(self.path, f"{id}.json")
        return self.__read_json_file(file_path)

    def get_all(self) -> List[Any]:
        result = []
        for file in os.listdir(self.path):
            if not file.endswith(".json"):
                continue
            file_path = os.path.join(self.path, file)
            model = self.__read_json_file(file_path)
            if model:
                result.append(model)
        return result

    def save(self, id: str, model: T) -> None:
        file_name = os.path.join(self.path, f"{id}.json")
        with open(file_name, "w") as file:
            file.write(model.json())

    def delete(self, id) -> None:
        os.remove(os.path.join(self.path, f"{id}.json"))

    def delete_all(self) -> None:
        for file in os.listdir(self.path):
            os.remove(os.path.join(self.path, file))
