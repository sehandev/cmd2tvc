# CMD to TVC
Convert CMD(Condensed Movies Dataset) to TVC(TV show Caption) dataset

Video Feature conversion is modified from opensource implementations made available by [HERO Video Feature Extractor](https://github.com/linjieli222/HERO_Video_Feature_Extractor).


## TODO
- [x]  Video Features (v0.3.0)
- [x]  Subtitles (v0.2.0)
- [x]  Captions (v0.1.0)

# How to

## Install dependencies

### Install python requirements with poetry

```bash
$ poetry install
```

### Install ffmpeg for feature conversion

```bash
$ sudo apt install ffmpeg
```

## Caption & Subtitle & Feature conversion

```bash
$ poetry run python cmd2tvc.py \
    --is_caption \
    --is_subtitle \
    --is_feature \
    --cmd_dir <path>/CMD/CondensedMovies/data/ \
```

If you want to convert only one type, then use codes below.

### Only caption conversion

```bash
$ poetry run python cmd2tvc.py --is_caption
```

### Only subtitle conversion

```bash
$ poetry run python cmd2tvc.py --is_subtitle
```

### Only feature conversion

```bash
$ poetry run python cmd2tvc.py --is_feature
```
