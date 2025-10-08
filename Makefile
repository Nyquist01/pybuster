enumerate:
	uv run --directory backend/ -m pybuster -t www.bbc.co.uk


format:
	uv run --directory backend/ ruff format
	uv run --directory backend/ ruff check --fix
	uv run --directory backend/ ruff check --fix --select I


requirements:
	uv pip --directory backend/ freeze > requirements.txt


build:
	docker compose build


build.nocache:
	docker compose build --no-cache


up:
	docker compose up -w


down:
	docker compose down

