import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}

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
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"


    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")


    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

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
    start = Node(state=source, parent=None, action=None)

    # Initialise final node as empty node and the goal_path as empty list
    goal_node = Node(state=None, parent=None, action=None)
    goal_path = []

    # Add the initial node to the frontier
    frontier = QueueFrontier()
    frontier.add(start)

    # search, until frontier is empty or goal is found
    while not frontier.empty() and goal_node.state == None:
        removed = frontier.remove()
        if removed.state == target:
                goal_node = removed
                break
        
        # If the removed node was not the goal, add it to explored
        explored.append(removed.state)

        # Add removed node's neighbors to the frontier
        neighbors = neighbors_for_person(removed.state)

        for movie_id, person_id in neighbors:
            new_node = Node(state=person_id, parent=removed, action=movie_id)

            # Avoid explored nodes and duplicate nodes
            if not frontier.contains_state(new_node.state) and new_node.state not in explored:
                frontier.add(new_node)

    # Return None if the search did not produce a goal_node
    if goal_node.state == None:
        return None
    
    # If successful, backtrack from the goal_node to the source, adding pairs to the goal path
    while goal_node.state != source:
        goal_path.append((goal_node.action, goal_node.state))
        goal_node = goal_node.parent

    # Reverse the goal path
    goal_path.reverse()

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
