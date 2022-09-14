import json
from pathlib import Path
from typing import List

import pandas as pd
from tqdm import tqdm

from cmd_info import CMDInfo
from optioner import Optioner, get_args_parser
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
    with open(tvc_dir / "captions.jsonl", "w") as jsonl_file:
        for json_string in json_string_list:
            jsonl_file.write(json_string + "\n")


def convert_caption(option: Optioner) -> None:
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
    args_parser = get_args_parser()
    args = args_parser.parse_args()

    option = Optioner(args)

    if option.is_caption:
        convert_caption(option)
