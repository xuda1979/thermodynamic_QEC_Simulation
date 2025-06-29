# Thermodynamic QEC Simulation

This project provides a modular Python framework for exploring quantum error-correcting codes along with their thermodynamic costs. It is inspired by research on energy-aware fault-tolerant quantum computing.

## Features

- **Code modules** for defining surface codes and other QEC codes
- **Noise models** with extensible abstractions
- **Simulation backends** that can interface with tools such as Stim or Qiskit
- **Decoders** for translating syndromes into corrections
- **Energy accounting** utilities to track energy consumption during simulation

## Installation

```bash
pip install -r requirements.txt
```

## Running Tests

```bash
pytest
```

## References

- Bilokur *et al.*, *Thermodynamic limits on fault-tolerant quantum computation*
- Riverlane QEC Explorer and related open-source projects

