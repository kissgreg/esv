![Build Status](https://github.com/kissgreg/esv/actions/workflows/main.yml/badge.svg)

# Embedded System Verification Framework (ESV-Framework)

## Project Overview
This repository demonstrates a modern, scalable approach to testing embedded software by bridging high-level test orchestration (Python/Pytest) with low-level logic (C). 

It models a **Hardware Abstraction Layer (HAL)** to verify firmware behavior without requiring physical hardware in the initial CI phase.

## Key Features
- **Hybrid Integration:** C-based logic compiled as a shared library, accessed via `ctypes`.
- **Advanced Orchestration:** Pytest fixtures for lifecycle management and parameterized testing for edge-case coverage.
- **CI/CD Ready:** Integrated GitHub Actions pipeline for automated Build & Test cycles.
- **Universal Design:** Architecture-agnostic approach applicable to ARM, RISC-V, or x86 environments.

## Advanced Concept: Hardware Mocking & HIL Simulation
A key feature of this framework is the **Hardware Mocking Layer**. 

In embedded environments, physical hardware (sensors, actuators) is often unavailable or difficult to manipulate during early development. This project implements a **Dependency Injection** pattern using C function pointers:

1. **C Side:** The firmware defines a callback interface for a temperature sensor.
2. **Python Side:** Using `ctypes.CFUNCTYPE`, the test suite injects a Python function directly into the C logic.
3. **Verification:** We can simulate extreme conditions (e.g., 55°C overheat) from a Python test case and verify if the C firmware correctly triggers the safety alarm bits.

This demonstrates a **Software-in-the-Loop (SIL)** testing strategy, reducing dependency on physical prototypes and allowing for exhaustive edge-case verification.

## Architecture
1. **src/firmware.c**: Simulated embedded logic (registers, buffers).
2. **src/bridge.py**: Python wrapper implementing the HAL pattern.
3. **tests/**: Test suite covering functional logic and boundary conditions.

## How to Run
1. Build the library: `make build`
2. Run tests: `pytest`