## Installation

#### Install pyenv

`Dependencies:`

```
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl
```

`Install pyenv:`

```
curl https://pyenv.run | bash
```

`~/.bashrc:`

```
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```


`Setup up env:`

```
pyenv install -v 3.6.0
```

`Install poetry (package-manager):`

https://python-poetry.org/docs/#installation

For dev: 

```
pip install poetry
```

`Install packages (Inside project directory):` 

```
pyenv use 3.6.0
poetry install
```

`Source into virtual env (poetry):`

```
poetry env info
# this will generate the path to the environement
source /path/generated/above/bin/activate
```

`Run:`

```
python parse.py
```
