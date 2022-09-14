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
        self.cmd_dir: Path = self.project_dir / args.cmd_dir
        self.metadata_dir: Path = self.cmd_dir / "metadata"
        self.descriptions_path: Path = self.metadata_dir / "descriptions.csv"
        self.durations_path: Path = self.metadata_dir / "durations.csv"
        self.videos_dir: Path = self.cmd_dir / "videos"
        self.tvc_dir: Path = self.project_dir / args.tvc_dir
        self.is_caption: bool = args.is_caption
        self.is_subtitle: bool = args.is_subtitle

        self.set_message_dict()
        self.validate_flags()
        self.mkdir()

    def set_message_dict(self) -> None:
        self.message_dict = {
            "flag_warning": "[WARN] Please check your options. You must turn on --is_caption or --is_subtitle"
        }

    def validate_flags(self) -> None:
        if self.is_caption is False and self.is_subtitle is False:
            print(self.message_dict["flag_warning"])

    def mkdir(self) -> None:
        self.tvc_dir.mkdir(parents=True, exist_ok=True)
