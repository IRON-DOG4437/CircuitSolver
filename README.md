# ⚡ SPICE Circuit Simulator

A Python-based circuit solver that computes **node voltages** and **branch currents** from a given text-based circuit file, similar to a basic SPICE simulator.

## 🚀 Features

- Parses circuit descriptions in a simple netlist format
- Calculates node voltages and branch currents using numerical techniques
- Supports basic circuit elements (resistors, voltage sources, etc.)
- Designed for educational and prototyping purposes

## 🧠 How It Works

The simulator reads a text file containing circuit specifications (similar to SPICE format), builds the matrix equations based on Kirchhoff’s laws, and solves them using `NumPy`.

## 🛠️ Getting Started

### Prerequisites

- Python 3.x
- NumPy

```bash
pip install numpy
```

## Usage
```bash
python evalSpice.py <circuit_file.txt>
```

## 📄 File Structure
evalSpice.py – Core script that implements the circuit solver logic
README.pdf – Original documentation submitted with the project (optional)

## 📚 Sample Circuit File Format
```arduino
* Simple resistive circuit
V1 N1 0 5
R1 N1 N2 10k
R2 N2 0 5k
.end
```

## 👨‍💻 Author
Vatsal Patwari



