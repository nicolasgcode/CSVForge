# Makefile
norm:
	python3 -m scripts.normalizator

proc:
	python3 -m scripts.processor

all: norm proc