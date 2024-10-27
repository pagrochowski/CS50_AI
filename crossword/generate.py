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
        print("Revising ", x, " and ", y)

        print("Domains before revision: \n", self.domains[x], " and \n", self.domains[y])

        # Assign value to x if there is a possible value for y
        revised = False
        for x_value in self.domains[x]:
            for y_value in self.domains[y]:
                if x_value != y_value:
                    assignment = {}
                    print("x_value: ", x_value, " and y_value: ", y_value)
                    assignment[x] = x_value
                    assignment[y] = y_value
                    print("Assignment: ", assignment)
                    if self.consistent(assignment):
                        print("Consistent: ", x_value, " and ", y_value)
                        
                    else:
                        print("Inconsistent: ", x_value, " and ", y_value)
                        revised = True
                    
        

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in assignment:
            if assignment[var] is None:
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
            if assignment[var] not in unique_vars:
                unique_vars.add(assignment[var])
            else:
                return False
            
        # Check if all words fit in the crossword puzzle
        for var in assignment:
            if len(assignment[var]) != var.length:
                return False
            
        # Check the overlaps between neighboring variables
        for var in assignment:
            # Get neighbors
            neighbors = self.crossword.neighbors(var)
            for neighbor in neighbors:
                # Check if there is an overlap
                if self.crossword.overlaps[var, neighbor]:
                    # Check if the values of the overlapping variables are the same and if neighbor has value assigned (is in assignment)
                    if neighbor in assignment and (var, neighbor) in self.crossword.overlaps:
                        print("Overlapping variables: ", var, " and ", neighbor)
                        if assignment[var][self.crossword.overlaps[var, neighbor][0]] != assignment[neighbor][self.crossword.overlaps[var, neighbor][1]]:
                            return False
        

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, 
        """
        
        values = []

        for value in self.domains[var]:
            values.append(value)

        print(values)

        return values
       
        """
        in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        for var in assignment:
            if assignment[var] is None:
                return var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        raise NotImplementedError


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
