PYTHON ?= python3
DAY ?=
DIAGRAMS ?= allow

.PHONY: day-check day-gate tests metrics require-day

require-day:
	@test -n "$(DAY)" || { echo "DAY is required (1-180)"; exit 2; }

day-check: require-day
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -B scripts/day_run.py check --day $(DAY) --diagrams $(DIAGRAMS)

day-gate: require-day
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -B scripts/day_run.py gate --day $(DAY)

tests:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest discover -s tests

metrics:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -B scripts/site_metrics.py
