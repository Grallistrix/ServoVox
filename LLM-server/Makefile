# Makefile dla Chatbot FastAPI z istniejącym venv
PYTHON := ../venv/bin/python
PIP := ../venv/bin/pip
UVICORN := ../venv/bin/uvicorn

SRC := main.py
PORT := 8000

.PHONY: all install run test clean

all: install run

# Instalacja zależności w istniejącym venv
install:
	$(PIP) install --upgrade pip

# Uruchomienie API
run:
	$(UVICORN) $(SRC:.py=):app --reload --host 0.0.0.0 --port $(PORT)


# Czyszczenie tymczasowych plików audio
clean:
	rm -f tts_*.wav 
	echo "Pliki tymczasowe audio usunięte"
