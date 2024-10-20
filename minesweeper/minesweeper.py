import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.

        Check if self.count is equal to the length of self.cells.
        If they are equal, all cells in self.cells are mines.
        """
        set_of_mines = set()

        # Number of cells equals mines 
        if self.count == len(self.cells):
            set_of_mines = self.cells
            

        return set_of_mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        set_of_safes = set()

        # Number of mines equals 0
        if self.count == 0:
            set_of_safes = self.cells

        return set_of_safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
        print("mark_mine(): ", cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
        
        print("mark_safe(): ", cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        def add_neighbors_as_sentence():
            # Add neighboring cells to knowledge as sentence
            neighbors = set()
            for i in range(cell[0] - 1, cell[0] + 2):
                for j in range(cell[1] - 1, cell[1] + 2):
                    if 0 <= i < self.height and 0 <= j < self.width:
                        if (i, j) != cell:
                            if (i, j) not in self.moves_made and (i, j) not in self.mines and (i, j) not in self.safes:
                                neighbors.add((i, j))

            new_sentence = Sentence(neighbors, count)
            if new_sentence not in self.knowledge:
                self.knowledge.append(new_sentence)

        def mark_cells_as_safe_or_mines():    
            knowledge_copy = copy.deepcopy(self.knowledge)
            for sentence in knowledge_copy:
                # # Mark safes
                if sentence.count == 0:
                    safes = sentence.known_safes()
                    print("adding known safes: ", safes)
                    print("Based on sentence: ", sentence)
                    for cell in safes:
                        self.mark_safe(cell)
                # Mark mines        
                elif len(sentence.cells) == sentence.count and sentence.count > 0:
                    mines = sentence.known_mines()
                    print("adding known mines: ", mines)
                    print("Based on sentence: ", sentence)
                    for cell in mines:
                        self.mark_mine(cell)
                    
        """ 
        Cross-Check All Sentences: Before marking a cell as a mine or safe, check other sentences 
        involving those cells to see if there's conflicting information. For instance, if multiple 
        sentences point to different outcomes for a specific cell, the AI should delay inference 
        until more information is available.

        Refine the Subset Check: You can enhance the subset inference logic by adding checks that 
        ensure inferred knowledge (e.g., (0, 0) being a mine) fits with all other existing sentences 
        in the knowledge base. This prevents conflicting deductions.
        """

        def infer_new_sentences():
            new_information = False
            knowledge_copy = copy.deepcopy(self.knowledge)
            for sentence in knowledge_copy:
                for other_sentence in knowledge_copy:
                    if sentence != other_sentence:
                        # Only infer if sentence has fewer cells and count <= other_sentence count
                        if sentence.cells.issubset(other_sentence.cells) and sentence.count <= other_sentence.count:
                            inferred_cells = other_sentence.cells - sentence.cells
                            inferred_count = other_sentence.count - sentence.count
                            # Only infer a new sentence if it is valid
                            # No empty sets
                            if len(inferred_cells) > 0:
                                # Non-negative counts
                                if inferred_count >= 0:
                                    # Count is less than or equal to number of cells
                                    if inferred_count <= len(inferred_cells):
                                        new_sentence = Sentence(inferred_cells, inferred_count)
                                        if new_sentence not in self.knowledge:
                                            self.knowledge.append(new_sentence)
                                            new_information = True
                                            print("adding new sentence: ", new_sentence)
            return new_information
                                

        def clear_knowledge():
            #print("clear_knowledge()")
            for sentence in self.knowledge:
                if len(sentence.cells) == 0:
                    #print("removing empty sentence")
                    self.knowledge.remove(sentence)


        # ------------------------------MAIN STEPS----------------------------------------------
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)
        print("-----------------------MOVE ", len(self.moves_made), " at ", cell, "-----------------------------------------")
        # 2) mark the cell as safe
        self.mark_safe(cell)
        
        # 3) add a new sentence to the AI's knowledge base
        add_neighbors_as_sentence()

        # 4) mark any additional cells as safe or as mines
        #    if it can be concluded based on the AI's knowledge base
        mark_cells_as_safe_or_mines()
                  
        # 5) add any new sentences to the AI's knowledge base
        # Loop marking cells and inferring new sentences until no new sentence is found
        new_information = True
        while new_information:
            new_information = False
            mark_cells_as_safe_or_mines()
            clear_knowledge()
            if infer_new_sentences():
                new_information = True


        # Clear knowledge of empty sentences
        clear_knowledge()

        # Debugging prints        
        print("known_mines so far (", len(self.mines), "): ", self.mines)
        print("known_safes so far (", len(self.safes), "): ", self.safes)
        print("Safe moves left: ", len(self.safes) - len(self.moves_made))
        print("Knowledge summary (", len(self.knowledge), "): ")
        for sentence in self.knowledge:
            print(sentence)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if len(self.safes) == 0:
            return None
        
        # Return random cell from safes
        for safe_cell in self.safes:
            if safe_cell not in self.moves_made and safe_cell not in self.mines:
                print("safe move selected: ", safe_cell)
                return safe_cell
            

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_moves = set()
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    possible_moves.add((i, j))

        if len(possible_moves) == 0:
            print("No possible moves")
            return None
        
        random_choice = random.choice(list(possible_moves))
        print("Random move selected: ", random_choice)
        return random_choice
