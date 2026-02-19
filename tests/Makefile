# Variables
CC = gcc
CFLAGS = -shared -fPIC
TARGET_LIB = src/c_logic/libfirmware.so
SRC_C = src/c_logic/firmware.c

# Build the shared library
build:
	$(CC) $(CFLAGS) -o $(TARGET_LIB) $(SRC_C)

# Run the Pytest suite
test: build
	pytest tests/ -v

# Clean up build artifacts
clean:
	rm -f $(TARGET_LIB)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache