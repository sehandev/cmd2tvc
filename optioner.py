import argparse
from pathlib import Path


class Optioner:
    def __init__(
        self,
        args: argparse.Namespace,
    ) -> None:
        if args.project_dir is None:
            self.project_dir = Path(__file__).parent.resolve()
        else:
            self.project_dir = Path(args.project_dir).resolve()
        self.cmd_dir = self.project_dir / args.cmd_dir
        self.descriptions_path = self.cmd_dir / "descriptions.csv"
        self.durations_path = self.cmd_dir / "durations.csv"
        self.tvc_dir = self.project_dir / args.tvc_dir
        self.mkdir()

    def mkdir(self) -> None:
        self.tvc_dir.mkdir(parents=True, exist_ok=True)
