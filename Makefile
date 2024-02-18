all: install import

install: .venv/bin/run-massless

import: var source_files extracted_files

test:
	tox -q

.venv/bin/run-massless: .venv/bin/python pyproject.toml
	uv pip install -r requirements.txt

.venv/bin/python:
	uv venv



var:
	mkdir -p var

source_files: var/hackdiet_db.csv var/export.xml

extracted_files: var/workouts.txt var/rings.txt var/alcohol.txt


var/hackdiet_db.csv: ~/Downloads/hackdiet_db.csv
	cp /Users/Reinout/Downloads/hackdiet_db.csv var

var/export.xml: ~/Downloads/apple_health_export/export.xml
	cp ~/Downloads/apple_health_export/export.xml var


var/workouts.txt: var/export.xml
	grep '<Workout\ ' var/export.xml > var/workouts.txt

var/rings.txt: var/export.xml
	grep '<ActivitySummary\ ' var/export.xml > var/rings.txt

var/alcohol.txt: var/export.xml
	grep NumberOfAlcoholicBeverages var/export.xml > var/alcohol.txt
