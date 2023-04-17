Template 

2,4,2,1,0,1      # n_dof, n_node, ETYPE, n_elem, n_force, n_load
30.0e6,0.25      # E, nu
1,0,0,1,1        # Each of the following (beginning with 1, 2, 3, 4 in that order) are nodes
2,1,0,0,1        # Each node element consists of (node#, x, y, constrained/unconstrained in x,constrained/unconstrained in y)
3,1,1,0,0        # another node element
4,0,1,0,0        # the final node element in this example
1,1,2,3,4,1.0    # elements (elem #, 1st node, 2nd node, 3rd node, 4th node, thickness)
1,3,-8000.0      # loads(elem #, edge #, surface load intensity)
