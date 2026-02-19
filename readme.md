# Embedded System Verification Framework (ESV-Framework)

## Project Overview
This repository demonstrates a modern, scalable approach to testing embedded software by bridging high-level test orchestration (Python/Pytest) with low-level logic (C). 

It models a **Hardware Abstraction Layer (HAL)** to verify firmware behavior without requiring physical hardware in the initial CI phase.

## Key Features
- **Hybrid Integration:** C-based logic compiled as a shared library, accessed via `ctypes`.
- **Advanced Orchestration:** Pytest fixtures for lifecycle management and parameterized testing for edge-case coverage.
- **CI/CD Ready:** Integrated GitHub Actions pipeline for automated Build & Test cycles.
- **Universal Design:** Architecture-agnostic approach applicable to ARM, RISC-V, or x86 environments.

## Architecture
1. **src/firmware.c**: Simulated embedded logic (registers, buffers).
2. **src/bridge.py**: Python wrapper implementing the HAL pattern.
3. **tests/**: Test suite covering functional logic and boundary conditions.

## How to Run
1. Build the library: `make build`
2. Run tests: `pytest`