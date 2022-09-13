import argparse
import json
from tqdm import tqdm

import pandas as pd

from cmd_info import CMDInfo
from optioner import Optioner
from tvc_info import TVCDescription, TVCInfo


def main(option: Optioner) -> None:
    description_df = pd.read_csv(option.descriptions_path)
    duration_df = pd.read_csv(option.durations_path)
    merge_df = pd.merge(description_df, duration_df, on="videoid")

    # Convert CMD to TVC
    json_string_list = []
    for idx, row in tqdm(merge_df.iterrows(), total=len(merge_df)):
        # Make CMD
        cmd = CMDInfo(
            description=row.description,
            duration=row.duration,
            imdbid=row.imdbid,
            videoid=row.videoid,
        )

        # Make TVC with CMD
        description = TVCDescription(
            desc=cmd.description,
            desc_id=cmd.videoid,
            from_retrieval=False,
            type="v",
        )
        tvc = TVCInfo(
            clip_id=idx,
            descs=[description],
            duration=cmd.duration,
            ts=[0],
            vid_name=cmd.videoid,
        )

        # Export to json
        tvc_dict = tvc.export_dictionary()
        json_string = json.dumps(tvc_dict, default=str)
        json_string_list.append(json_string)

    # Save TVC jsonl
    with open(option.tvc_dir / "cmd.jsonl", "w") as jsonl_file:
        for json_string in json_string_list:
            jsonl_file.write(json_string + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert CMD to TVC.")
    parser.add_argument("--project_dir", help="Project directory path")
    parser.add_argument("--cmd_dir", default="./test", help="CMD directory path")
    parser.add_argument("--tvc_dir", default="./tvc", help="TVC directory path")
    args = parser.parse_args()
    option = Optioner(args)
    main(option)
