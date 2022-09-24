from pathlib import Path
from typing import List

import ffmpeg
from tqdm import tqdm

from optioner import Optioner


def get_video_path_list(
    videos_dir: Path,
    extension: str = "mkv",
) -> List[Path]:
    return list(videos_dir.glob(f"**/*.{extension}"))


def remove_converted_mkv(
    mkv_path_list: List[Path],
    mp4_path_list: List[Path],
) -> List[Path]:
    converted_video_id_list = [mp4_path.stem for mp4_path in mp4_path_list]
    not_converted_mkv_path_list = []
    for mkv_path in mkv_path_list:
        if not mkv_path.stem in converted_video_id_list:
            not_converted_mkv_path_list.append(mkv_path)
    return not_converted_mkv_path_list


def convert_mkv_to_mp4(
    mkv_path_list: List[Path],
    mp4_dir: Path,
) -> None:
    for mkv_path in tqdm(mkv_path_list):
        video_id = mkv_path.stem
        converted_mp4_path = mp4_dir / f"{video_id}.mp4"
        (
            ffmpeg.input(mkv_path.as_posix())
            .output(
                filename=converted_mp4_path.as_posix(),
                vcodec="copy",
            )
            .run(quiet=True)
        )


def convert_features(option: Optioner) -> None:
    print("\n-- Start feature converseion --\n")

    mkv_path_list = get_video_path_list(option.videos_dir, extension="mkv")
    mp4_path_list = get_video_path_list(option.videos_dir, extension="mp4")
    mkv_path_list = remove_converted_mkv(mkv_path_list, mp4_path_list)

    convert_mkv_to_mp4(mkv_path_list, option.mp4_dir)
    mp4_path_list = get_video_path_list(option.videos_dir, extension="mp4")
