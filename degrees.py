import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps each person's id to another dictionary with values for the person's name, birth year, and the set of all the movies they have starred in
people = {}

# Maps each movie's id to another dictionary with values for that movie's title, release year, and the set of all the movie's stars
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
            movie_id = row["movie_id"]
            person_id = row["person_id"]
            movies[movie_id]["stars"].add(person_id)
            people[person_id]["movies"].add(movie_id)


def person_id_for_name(name):
    """
    Returns the id for a person based on their name.
    """
    person_ids = names.get(name.lower())
    if person_ids is None:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Enter ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids.pop()


def neighbors_for_person(person_id):
    """
    Returns the set of (movie_id, person_id) pairs for all people who starred in a movie with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


def shortest_path(source, target):
    """
    Returns the shortest path from the source to the target person.
    """
    # Create initial node and frontier
    start = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)

    # Create a set to keep track of explored states
    explored = set()

    # Loop until frontier is empty
    while not frontier.empty():
        # Get the current node
        node = frontier.remove()

        # Check if the goal is reached
        if node.state == target:
            path = []
            while node.parent is not None:
                path.append((node.action, node.state))
                node = node.parent
            path.reverse()
            return path

        # Mark the node as explored
        explored.add(node.state)

        # Find the neighbors of the current node
        neighbors = neighbors_for_person(node.state)

        # Add the neighbors to the frontier
        for movie_id, person_id in neighbors:
            if not frontier.contains_state(person_id) and person_id not in explored:
                child = Node(state=person_id, parent=node, action=movie_id)
                frontier.add(child)

    # If no path is found, return None
    return None


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1]

    # Load data from files
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    # Prompt user for source and target actors
    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    # Find the shortest path
    path = shortest_path(source, target)

    # Print the path
    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        for i, (movie_id, person_id) in enumerate(path):
            movie = movies[movie_id]["title"]
            person = people[person_id]["name"]
            print(f"{i+1}: {person} and {path[i-1][1]} starred in {movie}")


if _name_ == "_main_":
    main()