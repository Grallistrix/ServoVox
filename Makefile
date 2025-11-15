VENV_NAME = venv
PYTHON = python3
REQ = requirements.txt

.PHONY: all venv install clean

prepare: venv install

# Create Venv
venv:
	$(PYTHON) -m venv $(VENV_NAME)

# Install requirements
install: venv
	. $(VENV_NAME)/bin/activate && \
	pip install --upgrade pip setuptools wheel && \
	pip install -r $(REQ) --break-system-packages 
	curl https://ollama.com/install.sh | sh
	sudo apt install -y libasound2-dev


serve:
	ollama serve
#	ollama pull llama3.1:8b

# Test GPU detection
test:
	. $(VENV_NAME)/bin/activate && \
	$(PYTHON) torch_test.py

# Remove venv
clean:
	rm -rf $(VENV_NAME)
