'''
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
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # Add the cell and neighboring cells to knowledge as sentence
        neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i, j) != cell:
                        if (i, j) not in self.moves_made and (i, j) not in self.mines and (i, j) not in self.safes:
                            neighbors.add((i, j))

        self.knowledge.append(Sentence(neighbors, count))            
                    
        # Mark cells as safe or mines
        for sentence in self.knowledge:
            if len(sentence.cells) == sentence.count and sentence.count > 0:
                print("adding known mine: ", sentence.known_mines())
                print("sentence cells: ", len(sentence.cells), "sentence count: ", sentence.count)
                self.mines.update(sentence.known_mines())
            if sentence.count == 0:
                self.safes.update(sentence.known_safes())
                
        print("known_mines so far: ", self.mines)
        print("known_safes left to explore: ", len(self.safes) - len(self.moves_made))
        print("moves made so far: ", len(self.moves_made))
        
        # Add any new sentences to the AI's knowledge base
        knowledge_update = []
        knowledge_copy = copy.deepcopy(self.knowledge)

        
        for sentence in self.knowledge:
            for new_sentence in self.knowledge:
                if sentence != new_sentence:
                    if sentence.cells.issubset(new_sentence.cells):
                        new_sentence.count -= sentence.count
                        new_sentence.cells -= sentence.cells
            if len(new_sentence.cells) > 0:
                knowledge_update.append(new_sentence)
        self.knowledge = knowledge_update

        print("add_knowledge(): ", cell, count)
        print("number of sentences: ", len(self.knowledge))
        if len(self.knowledge) == 1:
            print("only sentence: ", self.knowledge[0])
''' 