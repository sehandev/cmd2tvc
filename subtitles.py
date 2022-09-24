from pathlib import Path
import re
from typing import List

import pysrt
from tqdm import tqdm

from info.cmd_info import CMDSubtitleLine
from optioner import Optioner
from info.tvc_info import TVCSubtitle, TVCSubtitleLine
from utils import export_json, save_jsonl

PREPROCESS_FLAG = "preprocessed"
TIMELINE_REGEX = r"\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+"


def find_cmd_srt_paths(videos_dir: Path) -> List[Path]:
    srt_path_list = list(videos_dir.glob(f"**/*[!{PREPROCESS_FLAG}].srt"))
    return srt_path_list


def is_timeline(line: str) -> bool:
    if re.match(TIMELINE_REGEX, line):
        return True
    return False


def preprocess_srt(line: str) -> str:
    line = line.strip()
    return line


def make_preprocessed_srt(srt_path: Path) -> Path:
    preprocessed_srt_path = srt_path.with_suffix(f".{PREPROCESS_FLAG}.srt")

    if preprocessed_srt_path.exists():
        return preprocessed_srt_path

    preprocessed_line_list: List[str] = []
    with open(srt_path, "r") as srt_file:
        for line in srt_file:
            line = preprocess_srt(line)
            if line != "":
                if is_timeline(line):
                    preprocessed_line_list[-1] = f"\n{preprocessed_line_list[-1]}"
                preprocessed_line_list.append(line)

    with open(preprocessed_srt_path, "w") as srt_file:
        for line in preprocessed_line_list:
            srt_file.write(line + "\n")

    return preprocessed_srt_path


def read_srt(srt_path: Path) -> List[pysrt.SubRipItem]:
    preprocessed_srt_path = make_preprocessed_srt(srt_path)
    line_list = list(pysrt.open(preprocessed_srt_path))
    return line_list


def convert_subtitle_line(subtitle: pysrt.SubRipItem) -> TVCSubtitleLine:
    # Make a CMD line
    cmd_line = CMDSubtitleLine(
        text=subtitle.text,
        start=subtitle.start.ordinal,
        end=subtitle.end.ordinal,
    )

    # Make a TVC line with the CMD line
    tvc_line = TVCSubtitleLine(
        text=cmd_line.text,
        start=cmd_line.start,
        end=cmd_line.end,
    )

    return tvc_line


def convert_subtitles(option: Optioner) -> None:
    srt_path_list = find_cmd_srt_paths(option.videos_dir)

    # Convert CMD to TVC
    tvc_json_list = []
    for srt_path in tqdm(srt_path_list):
        video_id = srt_path.stem.split(".")[0]

        srt_line_list = read_srt(srt_path)

        tvc_line_list: List[TVCSubtitleLine] = []
        for subtitle_line in srt_line_list:
            tvc_line = convert_subtitle_line(subtitle_line)
            if tvc_line.is_valid():
                tvc_line_list.append(tvc_line)

        tvc = TVCSubtitle(
            vid_name=video_id,
            sub=tvc_line_list,
        )

        tvc_json = export_json(tvc)
        tvc_json_list.append(tvc_json)

    # Save TVC subtitles jsonl
    save_jsonl(option.tvc_dir, "subtitles", tvc_json_list)
