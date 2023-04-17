import numpy as np
from scipy.sparse.linalg import spsolve
from scipy.sparse import csr_matrix


# The parse_input_file function takes in a file path and returns the following:
# young_mod: Young's modulus
# nu: Poisson's ratio
# nodes: a list of lists, where each sublist contains the node number, x coordinate, and y coordinate
# elements: a list of lists, where each sublist contains the element number, node 1, node 2, node 3, node 4,
# and thickness
# loads: a list of lists, where each sublist contains the element number, node 1, node 2, and force
def parse_input_file(input_file_path):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    n_dof, n_node, _, n_elem, n_force, n_load = map(int, lines[0].strip().split(','))
    young_mod, nu = map(float, lines[1].strip().split(','))

    nodes = []
    for line in lines[2:2 + n_node]:
        nodes.append(list(map(float, line.strip().split(','))))

    elements = []
    for line in lines[2 + n_node:2 + n_node + n_elem]:
        elements.append(list(map(float, line.strip().split(','))))

    loads = []
    for line in lines[2 + n_node + n_elem:]:
        loads.append(list(map(float, line.strip().split(','))))

    return young_mod, nu, nodes, elements, loads


# The element_stiffness_matrix function takes in the Young's modulus, area, and length of an element and returns
# the element stiffness matrix
def element_stiffness_matrix(young_mod, area, length):
    k = young_mod * area / length
    return np.array([[k, -k], [-k, k]])


# The element_force_vector function takes in the force and length of an element and returns the element force vector
def element_force_vector(force, length):
    return np.array([force * length / 2, force * length / 2])


# The calculate_areas_thickness function takes in a list of elements and returns a list of areas
def calculate_areas_thickness(elements):
    areas = []
    for element in elements:
        _, _, _, _, _, thickness = element
        area = thickness
        areas.append(area)
    return areas


# The construct_global_matrices function takes in the Young's modulus, Poisson's ratio, nodes, elements, and loads
# and returns the global stiffness matrix and global force vector
def construct_global_matrices(young_mod, nodes, elements, loads):
    num_elements = len(elements)
    areas = calculate_areas_thickness(elements)

    K = np.zeros((num_elements + 1, num_elements + 1))
    F = np.zeros(num_elements + 1)

    load_dict = {load[0]: load[2] for load in loads}

    for element, area in zip(elements, areas):
        _, node1, node2, _, _, _ = element
        x1, y1 = nodes[int(node1) - 1][1:3]
        x2, y2 = nodes[int(node2) - 1][1:3]
        length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        element_index = elements.index(element)
        force = load_dict.get(element_index + 1, 0)
        k_local = element_stiffness_matrix(young_mod, area, length)
        f_local = element_force_vector(force, length)

        K[element_index:element_index + 2, element_index:element_index + 2] += k_local
        F[element_index:element_index + 2] += f_local

    return K, F


# The apply_boundary_conditions function takes in the global stiffness matrix, global force vector, and nodes and
# returns the reduced global stiffness matrix and reduced global force vector
def apply_boundary_conditions(global_stiffness_matrix, global_force_vector, nodes):
    K, F = global_stiffness_matrix.copy(), global_force_vector.copy()
    num_elements = len(nodes) - 1

    K_reduced = K[1:num_elements, 1:num_elements]
    F_reduced = F[1:num_elements]

    return K_reduced, F_reduced


# The solve_reduced_system function takes in the reduced global stiffness matrix and reduced global force vector
# and returns the displacements
def calculate_stresses(displacements, young_mod, nodes, elements):
    num_elements = len(elements)
    stresses = []

    for element in elements:
        _, node1, node2, _, _, _ = element
        x1, y1 = nodes[int(node1) - 1][1:3]
        x2, y2 = nodes[int(node2) - 1][1:3]
        length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        element_index = elements.index(element)
        if element_index < num_elements - 1:
            d = displacements[element_index + 1] - displacements[element_index]
            stress_x = young_mod * d / length
            stress_y = 0  # Average normal stress in y direction
            shear_stress = 0  # Shear stress
            stresses.append((stress_x, stress_y, shear_stress))

    return stresses


# The output_results function takes in the displacements and stresses and prints them to the console
def output_results(displacements, stresses):
    print("Displacements: \t   x\t\t\ty")
    for i, (displacement_x, displacement_y) in enumerate(displacements, 1):
        print(f"Node {i:4}: {displacement_x:12.6f} {displacement_y:12.6f}")
    print("\nStresses:\t\t   Stress_x\t\t  Stress_y  Shear stress")
    for i, (stress_x, stress_y, shear_stress) in enumerate(stresses, 1):
        print(f"Element {i:4}: {stress_x:12.6f} | {stress_y:12.6f} | {shear_stress:12.6f}")


# The map_reduced_displacements_to_full function takes in the displacements and nodes and returns the full displacements
def map_reduced_displacements_to_full(displacements, nodes):
    num_nodes = len(nodes)
    full_displacements = np.zeros((num_nodes - 1) * 2)

    reduced_index = 0
    for i in range(1, num_nodes):
        if nodes[i][3] != 0:
            full_displacements[2 * (i - 1)] = displacements[reduced_index]
            full_displacements[2 * (i - 1) + 1] = displacements[reduced_index + 1]
            reduced_index += 2

    return full_displacements


# The main function takes in the input file path and prints the displacements and stresses
def main():
    input_file = input("Enter the file path: ")
    young_mod, nu, nodes, elements, loads = parse_input_file(input_file)
    global_stiffness_matrix, global_force_vector = construct_global_matrices(young_mod, nodes, elements, loads)
    reduced_stiffness_matrix, reduced_force_vector = apply_boundary_conditions(global_stiffness_matrix,
                                                                               global_force_vector, nodes)
    reduced_displacements = spsolve(csr_matrix(reduced_stiffness_matrix), reduced_force_vector)
    displacements = map_reduced_displacements_to_full(reduced_displacements, nodes)

    num_nodes = len(nodes)
    displacements_x_y = np.zeros((num_nodes, 2))
    displacement_index = 0
    for i in range(1, num_nodes):
        if nodes[i][3] == 0:
            displacements_x_y[i, 0] = displacements[displacement_index]
            displacements_x_y[i, 1] = displacements[displacement_index + 1]
            displacement_index += 2

    stresses = calculate_stresses(displacements, young_mod, nodes, elements)
    output_results(displacements_x_y, stresses)


# The main function is called when the program is run
if __name__ == "__main__":
    main()
