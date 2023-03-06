# cq == Code Quality
cq:
	flake8 ./ && black ./ && isort ./ && mypy ./

reload:
	uvicorn main:app --reload

alem mig:
	alembic init migration

alem rev:
	alembic revision --autogenerate -m

alem upd:
	alembic upgrade
