run:
	venv/bin/python3 semantic_pdf/cli.py

init:
	python3 -m venv venv
	venv/bin/pip3 install --upgrade pip
	venv/bin/pip3 install -r requirements.txt

delete-venv:
	rm -rf venv

refresh-venv: delete-venv init