import argparse
from pathlib import Path


def get_args_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert CMD to TVC.")
    parser.add_argument(
        "--project_dir",
        type=str,
        help="Project directory path",
    )
    parser.add_argument(
        "--cmd_dir",
        type=str,
        default="./test",
        help="CMD directory path",
    )
    parser.add_argument(
        "--tvc_dir",
        type=str,
        default="./tvc",
        help="TVC directory path",
    )
    parser.add_argument(
        "--is_caption",
        type=bool,
        default=False,
        action=argparse.BooleanOptionalAction,
        help="Do caption conversion or not",
    )
    parser.add_argument(
        "--is_subtitle",
        type=bool,
        default=False,
        action=argparse.BooleanOptionalAction,
        help="Do subtitle conversion or not",
    )
    parser.add_argument(
        "--is_feature",
        type=bool,
        default=False,
        action=argparse.BooleanOptionalAction,
        help="Do feature conversion or not",
    )
    return parser


class Optioner:
    def __init__(
        self,
        args: argparse.Namespace,
    ) -> None:
        if args.project_dir is None:
            self.project_dir: Path = Path(__file__).parent.resolve()
        else:
            self.project_dir: Path = Path(args.project_dir).resolve()
        self.cmd_dir: Path = Path(args.cmd_dir).resolve()
        self.metadata_dir: Path = self.cmd_dir / "metadata"
        self.descriptions_path: Path = self.metadata_dir / "descriptions.csv"
        self.durations_path: Path = self.metadata_dir / "durations.csv"
        self.videos_dir: Path = self.cmd_dir / "videos"
        self.tvc_dir: Path = self.project_dir / args.tvc_dir
        self.features_dir: Path = self.tvc_dir / "features"
        self.is_caption: bool = args.is_caption
        self.is_subtitle: bool = args.is_subtitle
        self.is_feature: bool = args.is_feature

        self.set_message_dict()
        if self.validate_flags():
            self.mkdir()

    def set_message_dict(self) -> None:
        self.message_dict = {
            "flag_warning": "[WARN] Please check your options. You must turn on --is_caption or --is_subtitle or --is_feature"
        }

    def validate_flags(self) -> bool:
        if not self.is_caption and not self.is_subtitle and not self.is_feature:
            print(self.message_dict["flag_warning"])
            return False
        return True

    def mkdir(self) -> None:
        self.tvc_dir.mkdir(parents=True, exist_ok=True)
        if self.is_feature:
            self.features_dir.mkdir(parents=True, exist_ok=True)
