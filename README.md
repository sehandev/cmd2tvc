# CMD to TVC
Convert CMD(Condensed Movies Dataset) to TVC(TV show Caption) dataset


## TODO
- [x]  Video Features (v0.3.0)
- [x]  Subtitles (v0.2.0)
- [x]  Captions (v0.1.0)

# How to

## Install dependencies

```bash
$ poetry install
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
