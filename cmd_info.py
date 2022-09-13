class CMDInfo:
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
