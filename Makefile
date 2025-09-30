run:
	uv run -m pybuster -t bbc.co.uk


format:
	uv run ruff format
	uv run ruff check --fix
	uv run ruff check --fix --select I


requirements:
	uv pip freeze > requirements.txt
