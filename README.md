# Pybuster

Website directory enumeration tool writte in Python. Hobby project inspired by [Gobuster](https://github.com/OJ/gobuster).

![alt text](https://github.com/Nyquist01/pybuster/blob/main/images/table_.png)

# Usage


## Requirements.txt

1. Create a virtual environment:

```
python -m venv .venv
```

2. Activate it:

```
source .venv/bin/activate
```

3. Install the dependencies:

```
pip install -r requirements.txt
```

4. Run the program:

```
python -m pybuster -t google.com
```

## UV

Also supports [uv](https://docs.astral.sh/uv/). Just run using:

```
uv run -m pybuster -t google.com
```
