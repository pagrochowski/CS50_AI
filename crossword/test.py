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

    print(crossword.variables)

    print(crossword.words)

    for var in crossword.variables:
        assignment[var] = None

    print("Assignment: ", assignment)

    variable = creator.select_unassigned_variable(assignment)

    print("Variable: ", variable)

    #values = 
    creator.order_domain_values(variable, assignment)

    #print(values)

    
    #assignment = creator.solve()
    """
    
    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)
    """




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