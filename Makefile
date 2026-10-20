.PHONY: all export sync

all: export sync

export:
	python3 scripts/export_svg.py

sync:
	python3 scripts/sync_to_quarto.py
