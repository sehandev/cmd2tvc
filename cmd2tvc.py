import argparse
import json
from pathlib import Path
from typing import List

import pandas as pd
from tqdm import tqdm

from cmd_info import CMDInfo
from optioner import Optioner
from tvc_info import TVCDescription, TVCInfo


def load_cmd(descriptions_path: Path, durations_path: Path):
    description_df = pd.read_csv(descriptions_path)
    duration_df = pd.read_csv(durations_path)
    merge_df = pd.merge(description_df, duration_df, on="videoid")
    return merge_df


def convert_cmd_to_tvc(clip_id: int, cmd_row: pd.Series) -> TVCInfo:
    # Make CMD
    cmd = CMDInfo(
        description=cmd_row.description,
        duration=cmd_row.duration,
        imdbid=cmd_row.imdbid,
        videoid=cmd_row.videoid,
    )

    # Make TVC with CMD
    description = TVCDescription(
        desc=cmd.description,
        desc_id=cmd.videoid,
        from_retrieval=False,
        type="v",
    )
    tvc = TVCInfo(
        clip_id=clip_id,
        descs=[description],
        duration=cmd.duration,
        ts=[0],
        vid_name=cmd.videoid,
    )
    return tvc


def export_json(tvc: TVCInfo) -> str:
    tvc_dict = tvc.export_dictionary()
    json_string = json.dumps(tvc_dict, default=str)
    return json_string


def save_tvc_jsonl(tvc_dir: Path, json_string_list: List[str]):
    with open(tvc_dir / "cmd.jsonl", "w") as jsonl_file:
        for json_string in json_string_list:
            jsonl_file.write(json_string + "\n")


def main(option: Optioner) -> None:
    cmd_df = load_cmd(option.descriptions_path, option.durations_path)

    # Convert CMD to TVC
    tvc_json_list = []
    for idx, row in tqdm(cmd_df.iterrows(), total=len(cmd_df)):
        tvc = convert_cmd_to_tvc(idx, row)
        tvc_json = export_json(tvc)
        tvc_json_list.append(tvc_json)

    # Save TVC jsonl
    save_tvc_jsonl(option.tvc_dir, tvc_json_list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert CMD to TVC.")
    parser.add_argument("--project_dir", help="Project directory path")
    parser.add_argument("--cmd_dir", default="./test", help="CMD directory path")
    parser.add_argument("--tvc_dir", default="./tvc", help="TVC directory path")
    args = parser.parse_args()

    option = Optioner(args)
    main(option)
