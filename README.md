# EvoSDXL demo

## Installation

```sh
git submodule update --init
```

Python環境をインストールしてから次を実行する。

```sh
# モデルをダウンロードするために、自分のAPI KEYを記入する必要がある
huggingface-cli login

# パッケージをインストール
python init.py [--preinstall_model]
```

## Usage

```sh 
python main.py [optional subcommands]
```