# Paper-Water-Penetration
Code for measuring the penetration behavior of water through paper.

For visualization we use jupiter notebook.

## Requirements
Python >=3.9<br>
Poetry

## Download
Download zip and extract files or simply use git clone.


## Install
This python repository use [poetry](https://python-poetry.org/) for dependency management and packaging.

### 1. Setup poetry
Execute the following command based on your OS.

For osx / linux / bashonwindows:
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

For Windows powershell:
```
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
```

### 2. Setup dependencies
Execute the following command.
```
poetry install
```

### 3. Run
Run the code by executing

```
python main.py
```

or

```
poetry run main.py
```

---

## Authors
Anne-Marie Kröher<br />
Luisa Schueller<br />
Peter Krutzke<br />

Coding support by Robert Unger


## License
This repository is released under the terms of the MIT license. Full details in LICENSE file.