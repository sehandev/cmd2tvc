# CMD to TVC
Convert CMD(Condensed Movies Dataset) to TVC(TV show Caption) dataset


## TODO
- [ ]  Video Features
- [x]  Subtitles (v0.2.0)
- [x]  Captions (v0.1.0)

# How to

## Install dependencies

`poetry install`

## Caption & subtitle conversion

`poetry run python cmd2tvc.py --is_caption --is_subtitle`

If you want to convert only a type, then use codes below.

### Only caption conversion

`poetry run python cmd2tvc.py --is_caption`

### Only subtitle conversion

`poetry run python cmd2tvc.py --is_subtitle`
