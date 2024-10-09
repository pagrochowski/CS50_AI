import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}

#directory = "//workspaces//CS50_AI//degrees"

def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    """
    ORIGINAL CODE
    
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"
    """

    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "small"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = "129"  # Tom Cruise
    target = "158"  # Tom Hanks

    #shortest_path(source, target)

    """
    #source = person_id_for_name(input("Name: "))
    #if source is None:
    #    sys.exit("Person not found.")
    
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")
    """
    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")
    
    

def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    # Initialise explored nodes list
    explored = []

    # Initialise the first (current) node
    current = Node(state=source, parent=None, action=None)

    # Initialise final node as empty node and the goal_path as empty list
    goal_node = Node(state=None, parent=None, action=None)
    goal_path = []

    # Add the initial node to the frontier
    frontier = QueueFrontier()
    frontier.add(current)

    # Add possible next nodes to the frontier
    neighbors = neighbors_for_person(source)

    """
    Iterate through each pair in neighbors.
    For each pair, create a new Node object.
    Set the state of the new node to the person ID.
    Set the parent to the current node.
    Set the action to the movie ID.
    Add the new node to the frontier.
    """
    for movie_id, person_id in neighbors:
        new_node = Node(state=person_id, parent=current, action=movie_id)
        frontier.add(new_node)

    """
    Remove a node from the frontier
    Check if the node has the goal state
    If not the goal, add node to the explored list
    """

    while not frontier.empty():
        removed = frontier.remove()
        #print(f"Removed: {removed.state}")

        # Check if the removed node is the goal
        if removed.state == target:
            print("Path found to ", target)
            goal_node = removed
            break 
        else:
            explored.append(removed)
            #print(f"Explored: {[node.state for node in explored]}")

        # Add neighbors of the removed node to the frontier
        removed_neighbors = neighbors_for_person(removed.state)

        for movie_id, person_id in removed_neighbors:
            new_node = Node(state=person_id, parent=removed, action=movie_id)
            # avoiding explored nodes
            flag = False
            for explored_node in explored:
                if new_node == explored_node:
                    flag = True
                    break
            if flag == False:
                frontier.add(new_node)
    
    """
    Start from the goal node.
    Follow the parent pointers back to the start node.
    Collect the movie_id and person_id pairs along the way.

    Here's a conceptual outline:

    Initialize an empty list to store the path.
    Set the current node to the goal node.
    While the current node is not the start node:
    Add the (movie_id, person_id) pair of the current node to the path.
    Move to the parent node.
    Reverse the path to get it from start to goal.
    """
    print("goal_node state id:", goal_node.state)
    while goal_node.state != source:
        #print("Starting goal node path while loop")
        goal_path.append((goal_node.action, goal_node.state))
        goal_node = goal_node.parent

    goal_path.reverse()
    print(goal_path)
    return goal_path



def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
