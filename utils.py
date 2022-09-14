import json
from tvc_info import TVCCaption


def export_json(tvc: TVCCaption) -> str:
    tvc_dict = tvc.export_dictionary()
    json_string = json.dumps(tvc_dict, default=str)
    return json_string
