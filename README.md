# Environment

### install pipx[https://github.com/pypa/pipx]

```commandline
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

### install python3-venv

```commandline
sudo apt install python3.12-venv
```

### install poetry[https://python-poetry.org/docs/#enable-tab-completion-for-bash-fish-or-zsh]

```commandline
pipx install poetry
```

### configure python environment

```commandline
poetry env use 3.12
```

### install neo4j[https://neo4j.com/docs/operations-manual/current/installation/linux/]


### Configuration
At `database/session.py` change `AUTH = ("rene", "00000000")` to your neo4j username and password.

### Install python dependencies

```commandline
poetry install
```

### Build Equipment Knowledge Graph
Turn neo4j database on and run `poetry run build-equipment-kg`, or `build_equipment_kg.py`

### Run Project
Run `poetry run dev`, the server would be running on `localhost:8000`. You could read the swagger api docs are at `localhost:8000/docs`.

# Caveat
1. user cannot name 'admin'
2. there is no data verification
3. user's customized node cannot have properties named with 'creator' or 'gid'
4. edges can only have one type at a time(but there could be multiple edges with different types between two nodes)
5. chatbot only support first 20 equipments for now.

