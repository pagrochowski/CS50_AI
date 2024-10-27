import sys

from crossword import *
from crossword import Variable, Crossword
from generate import CrosswordCreator

def main():
    # Check usage 

    # Parse command-line arguments
    structure = "data/structure0.txt"
    words = "data/words0.txt"
    output = "output.png"

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)

    assignment = {}

    assignment[Variable(0, 1, 'across', 3)] = "SIX"
    assignment[Variable(0, 1, 'down', 5)] = "SEVEN"
    assignment[Variable(4, 1, 'across', 4)] = "NINE"
    assignment[Variable(1, 4, 'down', 4)] = "FIVE"

    creator.enforce_node_consistency()

def test_enforce_node_consistency():

    # Parse command-line arguments
    structure = "data/structure0.txt"
    words = "data/words0.txt"

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)

    # Call enforce_node_consistency
    creator.enforce_node_consistency()

    # Assert that only correct words are in the domains
    assert creator.domains == {Variable(0, 1, 'down', 5): {'EIGHT', 'THREE', 'SEVEN'}, Variable(1, 4, 'down', 4): {'NINE', 'FOUR', 'FIVE'}, Variable(4, 1, 'across', 4): {'NINE', 'FOUR', 'FIVE'}, Variable(0, 1, 'across', 3): {'ONE', 'TEN', 'TWO', 'SIX'}}  


def test_consistent():

    # Parse command-line arguments
    structure = "data/structure0.txt"
    words = "data/words0.txt"

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)

    # Create an assignment
    assignment = {}

    for var in crossword.variables:
        assignment[var] = None

    # Assign values tovariables
    assignment[Variable(0, 1, 'across', 3)] = "SIX"
    assignment[Variable(0, 1, 'down', 5)] = "SEVEN"
    assignment[Variable(4, 1, 'across', 4)] = "NINE"
    assignment[Variable(1, 4, 'down', 4)] = "FIVE"

    # Call consistent
    consistent = creator.consistent(assignment)

    # Assert that there is a consistent assignment returned
    assert consistent == True

    # Testing unique constraint
    assignment[Variable(4, 1, 'across', 4)] = "FIVE"

    # Call consistent
    consistent = creator.consistent(assignment)

    assert consistent == False

    # Return to original assignment
    assignment[Variable(4, 1, 'across', 4)] = "NINE"

    # Testing length constraint
    assignment[Variable(0, 1, 'across', 3)] = "THREE"

    # Call consistent
    consistent = creator.consistent(assignment)

    assert consistent == False

    # Return to original assignment
    assignment[Variable(0, 1, 'across', 3)] = "SIX"

    # Testing overlaps
    assignment[Variable(0, 1, 'across', 3)] = "ONE"

    # Call consistent
    consistent = creator.consistent(assignment)

    assert consistent == False

    # Return to original assignment
    assignment[Variable(0, 1, 'across', 3)] = "SIX"


def test_assignment_complete():

    # Parse command-line arguments
    structure = "data/structure0.txt"
    words = "data/words0.txt"

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)

    # Create an assignment
    assignment = {}

    for var in crossword.variables:
        assignment[var] = None

    # Assign values to 3 out of 4 variables
    assignment[Variable(0, 1, 'across', 3)] = "SIX"
    assignment[Variable(0, 1, 'down', 5)] = "SEVEN"
    assignment[Variable(4, 1, 'across', 4)] = "NINE"

    # Call assignment_complete
    complete = creator.assignment_complete(assignment)

    # Assert that there is a complete assignment returned
    assert complete == False

    # Assign last value for completing assignment
    assignment[Variable(1, 4, 'down', 4)] = "FIVE"

    # Call assignment_complete
    complete = creator.assignment_complete(assignment)

    # Assert that there is a complete assignment returned
    assert complete == True

def test_order_domain_values():

    # Parse command-line arguments
    structure = "data/structure0.txt"
    words = "data/words0.txt"

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)

    # Create an assignment
    assignment = {}

    for var in crossword.variables:
        assignment[var] = None

    # Select an unassigned variable
    variable = creator.select_unassigned_variable(assignment)

    # Call order_domain_values
    domain_values = creator.order_domain_values(variable, assignment)

    # Assert that there is a list of domain values returned
    assert domain_values is not None


def test_select_unassigned_variable():

    # Parse command-line arguments
    structure = "data/structure0.txt"
    words = "data/words0.txt"

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)

    # Create an assignment
    assignment = {}

    for var in crossword.variables:
        assignment[var] = None

    # Select an unassigned variable
    variable = creator.select_unassigned_variable(assignment)

    # Assert that there is an unassigned variable returned
    assert variable is not None

    

if __name__ == "__main__":
    main()