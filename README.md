# Paper-Water-Penetration
Code for measuring the penetration behavior of water through paper.

For visualization we use jupiter notebook.

## Setup
### Requirements
Python >=3.9<br>
Poetry

### Download
Download zip and extract files or simply use git clone.

### Install
This python repository use [poetry](https://python-poetry.org/) for dependency management and packaging.

All the following commands must be executed in the command line.

### 1. Setup poetry
Execute the following command based on your OS.

For osx / linux / bashonwindows:
```shell
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - --preview
```

For Windows powershell:
```shell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python - --preview
```


### 2. Setup dependencies
Execute the following command in the working directory.

```shell
poetry install # only once to install the project
# everytime you reopen the commandline and goto directory
poetry shell
```

After install, close and reopen commandline to append poetry install path.

----
## Usage
You can either use the jupyter notebook for visual code presentation or simply execute the batch process.

### 1. Variant: Run Notebook: 2 Subvariants

1. Variant<br />
- Install VS Code.<br />
- Import project directory.<br />
- Click on the notebook.ipynb and select our previously installed virtualenv in the top right corner (interpreters).


2. Variant<br />
- Open commandline after install process (see steps 1-2).
- Goto the working directory.

```shell
poetry shell
jupyter notebook
```

See also [starting the notebook server](https://docs.jupyter.org/en/latest/running.html#starting-the-notebook-server)

- Search for your project directory
- Click on the notebook.ipynb

### 2. Variant: Commandline usage
- Goto the working directory.
- Options can be changes in options.py

Enable project Virtualenv

```shell
poetry shell
```

### You can execute the following commands:

- Execute capturing and data image creation

```shell
poetry run script
```

- Same as above, but waits on pressed key before capturing

```shell
poetry run wait_script
```

- Execute capturing only

```shell
poetry run capture
```

- Same as above, but waits on pressed key before capturing

```shell
poetry run wait_capture
```

----

## Authors
Anne-Marie Kröher<br />
Luisa Schueller<br />
Peter Krutzke<br />
Ralph Mückstein<br />
Coding support by Robert Unger


## License
This repository is released under the terms of the MIT license. Full details in LICENSE file.