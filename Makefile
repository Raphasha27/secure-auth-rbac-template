.PHONY: install run test lint clean

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload --port 8000

test:
	pytest -v

lint:
	ruff check app/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
