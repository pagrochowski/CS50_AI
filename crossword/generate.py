import sys

from crossword import *
from crossword import Variable, Crossword


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        # Collect words to be removed for each variable
        words_to_remove = {}

        # Loop through each variable in the copy
        for var in self.domains:
            # Loop through each word in variable's domain
            for word in self.domains[var]:
                # If the length of the word does not match the length of the variable
                if len(word) != var.length:
                    # Add the word to the dictionary of words to be removed from the variable's domain
                    if var in words_to_remove:
                        words_to_remove[var].append(word)
                    else:
                        words_to_remove[var] = [word]

        # Remove the collected words for removal from the domain
        for var in words_to_remove:
            for word in words_to_remove[var]:
                if word in self.domains[var]:
                    self.domains[var].remove(word)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.

        Iterate through each value in self.domains[x].
        Check if there is a corresponding value in self.domains[y] that satisfies the constraints.
        If no such value exists, remove the value from self.domains[x] and set revised to True.
        """
        
        # Initiate revised flag
        revised = False

        # Initiate empty set for removal
        removals = set()

        # Assign value to x if there is a possible value for y that satisfies the constraints
        for x_value in self.domains[x]:

            # Initiate satisfied variable flag
            satisfied = False

            # Loop through each value in self.domains[y]
            for y_value in self.domains[y]:
                # Exclude same values
                if x_value != y_value:
                    # Create an assignment of x and y
                    assignment = {}
                    assignment[x] = x_value
                    assignment[y] = y_value

                    # Check if assignment is consistent
                    if self.consistent(assignment):

                        # Yes it is consistent, set satisfied to True
                        satisfied = True

            # If there is no value in self.domains[y] that satisfies the constraints, remove the value from self.domains[x]
            if not satisfied:
                removals.add(x_value)
                revised = True
        
        # Remove values from self.domains[x] that do not satisfy the constraints
        for removal in removals:
            self.domains[x].remove(removal)

        return revised
                    
        
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.

        Initialize the Queue: If arcs is None, you need to initialize the queue 
        with all arcs in the problem. Otherwise, use the provided arcs.

        Process the Queue: While the queue is not empty, remove an arc from the 
        queue and make the variables arc consistent.

        Revise Domains: For each arc, revise the domain of the first variable. 
        If the domain of a variable is revised, add all neighboring arcs back to the queue.

        Check for Empty Domains: If any domain becomes empty, return False. 
        If the queue is processed without empty domains, return True.
        """
        
        # Initialise arc queue
        if arcs is None:
            arcs = []
            # Add all arcs in the problem
            for var1 in self.crossword.variables:
                for var2 in self.crossword.neighbors(var1):
                    if var1 != var2:
                        arcs.append((var1, var2))

        #else:
            #print("Arcs provided: ", arcs)


        #print("Number of arcs to process: ", len(arcs))
        #for arc in arcs:
            #print("Arc: ", arc)

        # Process queue
        while len(arcs) > 0:
            # Remove an arc from the queue
            arc = arcs.pop()
            var1 = arc[0]
            var2 = arc[1]
            #print("Arc popped: ", arc)
            # Make the variables arc consistent
            if self.revise(var1, var2):
                #print("Revised: ", var1, var2)
                # If the domain of a variable is revised, add all neighboring arcs back to the queue
                #print("Var1 neighbors: ", self.crossword.neighbors(var1))
                for var3 in self.crossword.neighbors(var1):
                    if var3 != var1 and var3 != var2:
                        #print("Adding new arcs: ")
                        #print((var3, var1))
                        #print((var3, var2))
                        arcs.append((var3, var1))
                        arcs.append((var3, var2))
            #else: 
                #print("Not revised: ", var1, var2)
       
        # Check for empty domains
        for var in self.crossword.variables:
            if len(self.domains[var]) == 0:
                #print("Domain ", var, " is empty")
                return False
        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.

        :( assignment_complete identifies incomplete assignment
        expected "False", not "True"
        """
        # Check if all variables have a value
        for var in assignment:
            if assignment[var] is None:
                return False
        
        # Check if all variables are present in the assignment
        for var in self.crossword.variables:
            if var not in assignment:
                return False

        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # Check if each variable has a unique value
        unique_vars = set()
        for var in assignment:
            #print(f"Checking variable {var} with value {assignment[var]}")
            if assignment[var] is not None:
                #print(f"Value is not None: {assignment[var]}")
                if assignment[var] not in unique_vars:
                    unique_vars.add(assignment[var])
                else:
                    #print("Variable ", var, " has a duplicate value: ", assignment[var])
                    return False
            
        
        # Check if all words fit in the crossword puzzle
        for var in assignment:
            if assignment[var] is not None:
                if len(assignment[var]) != var.length:
                    #print("Variable ", var, " has an incorrect length: ", assignment[var])
                    return False

        
        # Check the overlaps between neighboring variables
        for var in assignment:
            # Get neighbors for variables with value
            if assignment[var] is None:
                #print("Variable ", var, " has no value assigned")
                continue
            neighbors = self.crossword.neighbors(var)
            for neighbor in neighbors:
                # Check if there is an overlap
                if neighbor in assignment and assignment[neighbor] is None:
                    #print("Neighbor is None: ", neighbor)
                    continue
                #print("Checking overlap: ", var, " and ", neighbor)
                if self.crossword.overlaps[var, neighbor]:
                    # Check if the values of the overlapping variables are the same and if neighbor has value assigned (is in assignment)
                    if neighbor in assignment and (var, neighbor) in self.crossword.overlaps:
                        #print("Overlapping variables: ", var, " and ", neighbor)
                        if assignment[var][self.crossword.overlaps[var, neighbor][0]] != assignment[neighbor][self.crossword.overlaps[var, neighbor][1]]:
                            #print("Overlapping variables have different values: ", assignment[var], " and ", assignment[neighbor])
                            return False
           
        return True
        

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Initialise a list of values with scores 0
        value_scores = {value: 0 for value in self.domains[var]}

        # Store original assignment
        original_assignment = assignment.copy()

        print("Original assignment:")
        for each_var in original_assignment:
            print(each_var, original_assignment[each_var])

        # Test each value of the var's domain
        for value in self.domains[var]:
            for neighbor in self.crossword.neighbors(var):
                # Check if neighbor has value assigned
                if neighbor not in assignment:
                    # Check if there is an overlap
                    if self.crossword.overlaps[var, neighbor]:
                        # Test each value of the neighbor's domain
                        for neighbor_value in self.domains[neighbor]:
                            # Assign value to var
                            assignment[var] = value
                            # Assign value to neighbor
                            assignment[neighbor] = neighbor_value
                            # Check if assignment is consistent
                            if not self.consistent(assignment):
                                # Increment value_scores
                                value_scores[value] += 1

                            # Reset assignment
                            assignment = original_assignment.copy()
        
        # Return list of values with scores
        sorted_values = sorted(value_scores, key=value_scores.get)
        print("Value scores: ", value_scores)

        return sorted_values



    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Get a list of unassigned variables
        unassigned = [var for var in self.crossword.variables if var not in assignment]

        # Get the number of remaining values for each variable
        remaining_values = [len(self.domains[var]) for var in unassigned]

        # Get the degree of each variable
        degrees = [len(self.crossword.neighbors(var)) for var in unassigned]

        # Return the variable with the minimum number of remaining values
        # and the highest degree
        return min(unassigned, key=lambda var: (remaining_values[unassigned.index(var)], degrees[unassigned.index(var)]))


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.

        function Backtrack(assignment, csp):

        if assignment complete:
            return assignment

        var = Select-Unassigned-Var(assignment, csp)
        for value in Domain-Values(var, assignment, csp):
        if value consistent with assignment:
        add {var = value} to assignment
        result = Backtrack(assignment, csp)
        if result ≠ failure:
        return result
        remove {var = value} from assignment
        return failure
        """
        print("Assignment received in backtrack: ")
        for var in assignment:
            print(var, assignment[var])

        # Check if assignment is completed
        if self.assignment_complete(assignment):
            print("Assignment complete")
            return assignment
        else:
            print("Assignment not complete, continuing the loop")
            # Select an unassigned variable
            var = self.select_unassigned_variable(assignment)
            print("Selecting variable: ", var)
            # Order domain values and assign to variable
            for value in self.order_domain_values(var, assignment):
                print("Value: ", value)
                # Make variable assignment
                assignment[var] = value
                print("Assignment: ")
                for var in assignment:
                    print(var, assignment[var])
                # Call consistent
                if self.consistent(assignment):
                    print("Consistent")
                    # Call backtrack in case newly assigned variable is okay, keep going
                    result = self.backtrack(assignment)
                    if result is not None:
                        #print("Feeding result to backtrack")
                        return result
                print("Consistent failed, variable unassigned:", var)
                assignment[var] = None
            print("Returning None")
            return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
