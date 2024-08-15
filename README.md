# EvoSDXL demo

## Installation

```sh
pip install -r requirements.txt
```

モデルをダウンロードするために、[ここ](https://huggingface.co/stabilityai/japanese-stable-diffusion-xl)へアクセス許可を申請しないとならない。
その後、自分のAPIキーをPython環境に挿入する。

```sh
python -m huggingface-cli login
```

## Usage

```sh 
python main.py [optional subcommands]
```