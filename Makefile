# cq == Code Quality
cq:
	flake8 ./ && black ./ && isort ./ && mypy ./

reload:
	uvicorn app.main:app --reload

alemmig:
	alembic init migration

alemrev:
	alembic revision --autogenerate -m "Initial"

alemupd:
	alembic upgrade head

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
