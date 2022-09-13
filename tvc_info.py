import json
from typing import List


class TVCDescription:
    def __init__(
        self,
        desc: str,
        desc_id: str,
        from_retrieval: bool,
        type: str,
    ) -> None:
        self.desc = desc
        self.desc_id = desc_id
        self.from_retrieval = from_retrieval
        self.type = type
        self.validate()

    def validate(self) -> None:
        self.validate_type()

    def validate_type(self) -> None:
        type_set = {"t", "v", "vt"}
        if self.type not in type_set:
            raise ValueError(f"Description type must be one of [{', '.join(type_set)}]")

    def export_dictionary(self):
        return {
            "desc": self.desc,
            "desc_id": self.desc_id,
            "from_retrieval": self.from_retrieval,
            "type": self.type,
        }


class TVCInfo:
    def __init__(
        self,
        clip_id: int,
        descs: List[TVCDescription],
        duration: int,
        ts: List[int],
        vid_name: str,
    ) -> None:
        self.clip_id = clip_id
        self.descs = descs
        self.duration = duration
        self.ts = ts
        self.vid_name = vid_name
        self.validate()

    def validate(self) -> None:
        self.validate_descs()

    def validate_descs(self) -> None:
        if len(self.descs) == 0:
            raise ValueError("At least one description is needed")

    def export_dictionary(self):
        descs = [desc.export_dictionary() for desc in self.descs]
        return {
            "clip_id": self.clip_id,
            "descs": descs,
            "duration": self.duration,
            "ts": self.ts,
            "vid_name": self.vid_name,
        }

    def __str__(self) -> str:
        tvc_dict = self.export_dictionary()
        return json.dumps(tvc_dict, indent=4, default=str)
