# Pybuster

Website directory enumeration tool writte in Python. Hobby project inspired by [Gobuster](https://github.com/OJ/gobuster).

![alt text](https://github.com/Nyquist01/pybuster/blob/main/images/table.png)

# Usage


## Requirements.txt

1. Create a virtual environment

```
python -m venv .venv
```

2. Activate your virtual environment

```
source .venv/bin/activate
```

3. Install the dependencies in your virtual environment:

```
pip install -r requirements.txt
```

4. Run main.py against a target host:

```
python main.py -t <host/domain>
```

## UV

Also supports [uv](https://docs.astral.sh/uv/). Just run using:

```
uv run main.py -t <host/domain>
```
