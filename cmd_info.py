class CMDCaption:
    def __init__(
        self,
        description,
        duration,
        imdbid,
        videoid,
        duration_type="int",
    ) -> None:
        self.description = description
        self.duration = self.astype_duration(duration, duration_type)
        self.imdbid = imdbid
        self.videoid = videoid

    @staticmethod
    def astype_duration(duration, type="int"):
        if type == "int":
            return int(duration)

        print("No type change - duration")
        return duration

    def __str__(self) -> str:
        string_list = [
            f"[ Video ID : {self.videoid} ]",
            f"IMDB ID : {self.imdbid}",
            f"Duration : {self.duration}",
            f"Description : {self.description}",
        ]
        return "\n".join(string_list)


class CMDSubtitleLine:
    def __init__(
        self,
        text: str,
        start: int,
        end: int,
    ) -> None:
        self.text = self.preprocess_text(text)
        self.start = self.change_to_second_format(start)
        self.end = self.change_to_second_format(end)

    @staticmethod
    def preprocess_text(text: str) -> str:
        text = text.strip()
        return text

    @staticmethod
    def change_to_second_format(milliseconds: int) -> float:
        seconds = milliseconds / 1000
        return seconds
