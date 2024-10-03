run:
	uvicorn api:app --host 0.0.0.0 --port 8080 --reload

install:
	uv install

reinstall: 
	make clean
	rm -rf .venv
	make install

lint:
	uv run ruff format

clean: 
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
	rm -rf .pytest_cache

revision:
	alembic revision --autogenerate -m $(name)

make migrate:
	alembic upgrade head