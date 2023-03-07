# cq == Code Quality
cq:
	flake8 ./ && black ./ && isort ./ && mypy ./

reload:
	uvicorn app/main:app --reload

alem mig:
	alembic init migration

alem rev:
	alembic revision --autogenerate -m

alem upd:
	alembic upgrade

build:
	docker build .
up:
	docker-compose up -d
psa:
	docker-compose ps -a
upb:
	docker-compose up -d --build
docbuild:
	docker-compose build
down:
	docker-compose down
