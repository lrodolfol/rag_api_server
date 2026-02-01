db-init:
	docker exec -i rag_postgres psql -U postgres -d ragweb < dump.sql
# Makefile para rag_api_server

.PHONY: help venv install run lint format test clean infra-start infra-stop

infra-start:
	docker compose -f infra/infra.yaml up -d
infra-stop:
	docker compose -f infra/infra.yaml down

help:
	@echo "Comandos disponíveis:"
	@echo "  venv     - Cria ambiente virtual Python (./venv)"
	@echo "  install  - Instala dependências no venv"
	@echo "  run      - Executa a aplicação Flask"
	@echo "  lint     - Roda flake8 para análise de código"
	@echo "  format   - Roda black para formatar o código"
	@echo "  test     - Executa testes (se houver)"
	@echo "  clean    - Remove arquivos temporários e venv"

venv:
	python3 -m venv venv

install: venv
	. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

run:
	. venv/bin/activate && python app.py

lint:
	. venv/bin/activate && flake8 .

format:
	. venv/bin/activate && black .

test:
	@echo "Adicione seus testes aqui."

clean:
	rm -rf venv __pycache__ .pytest_cache .mypy_cache
