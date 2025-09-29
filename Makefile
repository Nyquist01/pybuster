run:
	uv run main.py -t google.com


format:
	uv run ruff format
	uv run ruff check --fix
	uv run ruff check --fix --select I


requirements:
	uv pip freeze > requirements.txt
