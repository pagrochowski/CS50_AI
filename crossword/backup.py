def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Initialize a dictionary to store the number of values each value rules out
        value_scores = {}

        # Initialise a list of values with scores 0
        value_scores = {value: 0 for value in self.domains[var]}

        # Print out assignment
        print("Assignment: ")
        for each in assignment:
            print(each, ": ", assignment[each])

        print("Variable: ", var)
        print("Values: ", self.domains[var])

        # Check how many values each value rules out for neighboring variables
        for value in self.domains[var]:

            # Assign value
            print("Assigning value: ", value)
            assignment[var] = value

            # Loop through neighbors
            for neighbor in self.crossword.neighbors(var):
                print("Checking neighbor: ", neighbor)
            
                # Skip neighbor if it has a value assigned
                if neighbor in assignment and assignment[neighbor] is not None:
                    print("Neighbor has a value assigned", assignment[neighbor])
                    continue

                # Check if there is an overlap
                if (var, neighbor) in self.crossword.overlaps:
                    print("There is an overlap")
                
                    # Loop through neighbor's domain values
                    for neighbor_value in self.domains[neighbor]:
                        if neighbor in assignment:      
                            current_value = assignment[neighbor]    # Store original value
                            assignment[neighbor] = neighbor_value   # Assign new neighbor's value

                            # Check if the assignment is consistent
                            if not self.consistent(assignment):
                                print("Value", value, "rules out for neighbor its value", neighbor_value)
                                value_scores[value] = value_scores.get(value, 0) + 1    # Increment the value in the dictionary
                            else:
                                print("Value ", value, " does not rule out for neighbor its value", neighbor_value)

                            # Reset neighbor's value
                            #print("Resetting neighbor value")
                            assignment[neighbor] = current_value

                    # Print total ruled out count
                    if value in value_scores:
                        print("Total ruled out count: ", value_scores[value])

        print("Value scores: ", value_scores)

        # Sort the values by the number of values they rule out
        sorted_values = sorted(value_scores, key=value_scores.get)
        print("Sorted values: ", sorted_values)

        return sorted_values