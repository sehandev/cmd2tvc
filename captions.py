from pathlib import Path

import pandas as pd
from tqdm import tqdm

from info.cmd_info import CMDCaption
from optioner import Optioner
from info.tvc_info import TVCCaption, TVCDescription
from utils import export_json, save_jsonl


def load_cmd_caption(descriptions_path: Path, durations_path: Path) -> pd.DataFrame:
    description_df = pd.read_csv(descriptions_path)
    duration_df = pd.read_csv(durations_path)
    merge_df = pd.merge(description_df, duration_df, on="videoid")
    return merge_df


def convert_caption(clip_id: int, cmd_row: pd.Series) -> TVCCaption:
    # Make CMD
    cmd = CMDCaption(
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
    tvc = TVCCaption(
        clip_id=clip_id,
        descs=[description],
        duration=cmd.duration,
        ts=[0],
        vid_name=cmd.videoid,
    )
    return tvc


def convert_captions(option: Optioner) -> None:
    cmd_df = load_cmd_caption(option.descriptions_path, option.durations_path)

    # Convert CMD to TVC
    tvc_json_list = []
    for idx, row in tqdm(cmd_df.iterrows(), total=len(cmd_df)):
        tvc = convert_caption(idx, row)
        tvc_json = export_json(tvc)
        tvc_json_list.append(tvc_json)

    # Save TVC captions jsonl
    save_jsonl(option.tvc_dir, "captions", tvc_json_list)
