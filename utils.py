import json
from pathlib import Path
from typing import List

from info.tvc_info import TVCCaption


def export_json(tvc: TVCCaption) -> str:
    tvc_dict = tvc.export_dictionary()
    json_string = json.dumps(tvc_dict, default=str)
    return json_string


def save_jsonl(output_dir: Path, file_name: str, json_string_list: List[str]) -> None:
    with open(output_dir / f"{file_name}.jsonl", "w") as jsonl_file:
        for json_string in json_string_list:
            jsonl_file.write(json_string + "\n")
