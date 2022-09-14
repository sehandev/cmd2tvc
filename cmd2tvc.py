from captions import convert_captions
from optioner import Optioner, get_args_parser
from subtitles import convert_subtitles


if __name__ == "__main__":
    args_parser = get_args_parser()
    args = args_parser.parse_args()

    option = Optioner(args)

    if option.is_caption:
        convert_captions(option)
    if option.is_subtitle:
        convert_subtitles(option)
