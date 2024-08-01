PYTHON = ./venv/bin/python3
PIP = ./venv/bin/pip

setup: pip-install migrations loaddata runserver

pip-install:
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r requirements.txt

migrations:
	$(PYTHON) tree_menu/manage.py makemigrations
	$(PYTHON) tree_menu/manage.py migrate

loaddata:
	$(PYTHON) tree_menu/manage.py loaddata tree_menu/data/db.json

create-test-admin:
	$(PYTHON) tree_menu/manage.py createsuperuser

runserver:
	$(PYTHON) tree_menu/manage.py runserver
