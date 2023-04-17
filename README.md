# urban-guacamole
This Python program performs a structural analysis on a given structure, calculating displacements and stresses at nodes and elements. The program takes an input file containing structure properties, such as material properties, nodes, elements, and loads, and computes the results using a finite element method.

## Features

- Parses an input file containing structure properties
- Constructs global stiffness and force matrices
-Applies boundary conditions
- Solves for displacements and stresses
- Outputs results in an easy-to-read format

## Usage

### Input file format

The input file should be formatted as follows:

- First line: Number of degrees of freedom, number of nodes, number of boundary conditions, number of elements, number of forces, number of loads (separated by commas)
- Second line: Material properties (E and nu, separated by a comma)
- Next lines: Node information (node number, x-coordinate, y-coordinate, boundary condition)
- Following lines: Element information (element number, node 1, node 2, material number, cross-sectional area, thickness)
- Final lines: Load information (load number, node number, force)

For a detailed input, check the ```README.txt``` file 

## Running the program

To run the program, simply execute it in a Python environment. You will be prompted to enter the file path of your input file. The program will then perform the structural analysis and output the calculated displacements and stresses.

```
python structural_analysis.py
```
Example:
```
Enter the file path: BM1.txt
Displacements: 	   x	        y
Node    1:     0.000000     0.000000
Node    2:     0.000500     0.000000
Node    3:     0.001000     0.000000
...

Stresses:	 Stress_x	 Stress_y   Shear stress
Element    1:    -0.001000 |     0.000000 |     0.000000
Element    2:     0.000500 |     0.000000 |     0.000000
Element    3:     0.001000 |     0.000000 |     0.000000
...

```
