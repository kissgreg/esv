# Variables
CC = gcc
CFLAGS = -shared -fPIC
TARGET_LIB = src/libfirmware.so
SRC_C = src/firmware.c

build:
	$(CC) $(CFLAGS) -o $(TARGET_LIB) $(SRC_C)

# All-in-one test command with coverage and html report
test: build
	PYTHONPATH=. pytest tests/ -v --cov=src --cov-report=term-missing --html=report.html --self-contained-html

clean:
	rm -f $(TARGET_LIB) report.html
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache