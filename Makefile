enumerate:
	uv run -m pybuster -t www.bbc.co.uk


format:
	uv run ruff format
	uv run ruff check --fix
	uv run ruff check --fix --select I


requirements:
	uv pip freeze > requirements.txt


build:
	docker compose build


up:
	docker compose up -w


down:
	docker compose down


server:
	uv run 
