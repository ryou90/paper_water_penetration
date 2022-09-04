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

All the following commands must be executed in the command line.

### 1. Setup poetry
Execute the following command based on your OS.

For osx / linux / bashonwindows:
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - --preview
```

For Windows powershell:
```
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python - --preview
```

### 2. Setup dependencies
Execute the following command in the working directory.
```
poetry install
```

After install, close and reopen commandline to append poetry install path.

### 3. Run script
Goto the working directory.

```
poetry shell
cd ./src
python run.py
```

### 4. Run Notebook
Install VS Code.
Import project directory.
Click on the notebook.ipynb

OR

Open commandline.

```
jupyter notebook
```

[starting-the-notebook-server](https://docs.jupyter.org/en/latest/running.html#starting-the-notebook-server)

Search for your project directory.
Click on the notebook.ipynb

## Authors
Anne-Marie Kröher<br />
Luisa Schueller<br />
Peter Krutzke<br />

Coding support by Robert Unger


## License
This repository is released under the terms of the MIT license. Full details in LICENSE file.