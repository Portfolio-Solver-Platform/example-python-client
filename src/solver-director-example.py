from time import sleep
from auth import Token
from auth.device_auth import DeviceAuth
from config import Config
import requests
from pprint import pprint
from solver_director import (
    create_project,
    delete_project,
    get_project_config,
    get_project_solution,
    get_project_status,
    get_projects,
)


def create_example_project(token: Token) -> dict:
    project_config = {
        "name": "Test Project",
        "problem_groups": [
            {
                "problemGroup": 1,
                "problems": [
                    {"problem": 10, "instances": [1, 2, 3]},
                    {"problem": 11, "instances": [4, 5]},
                ],
                "extras": {
                    "repetitions": 1,
                    "solvers": [
                        {
                            "id": 1,
                            "vcpus": 1,
                        },
                        {
                            "id": 2,
                            "vcpus": 1,
                        },
                    ],
                },
            }
        ],
    }
    return create_project(token, project_config)


def create_read_delete_project(token: Token):
    """Example workflow: Create, read, and delete a project."""

    # 1. Create a new project
    new_project = create_example_project(token)
    pprint(new_project)
    project_id = new_project["id"]
    print()
    print("New project ID:", project_id)
    print()

    print("==== Listing all projects ====")
    all_projects = get_projects(token)
    pprint(all_projects)
    print()

    sleep(8)
    # 3. Get project status
    print(f"==== Getting project {project_id} status ====")
    status = get_project_status(token, project_id)
    pprint(status)
    print()

    # 4. Get project configuration
    print(f"==== Getting project {project_id} configuration ====")
    config = get_project_config(token, project_id)
    pprint(config)
    print()

    # 5. Try to get project solution (not implemented yet)
    print(f"==== Getting project {project_id} solution ====")
    try:
        solution = get_project_solution(token, project_id)
        pprint(solution)
    except requests.HTTPError as e:
        print(f"Expected error: {e}")
    print()

    # 6. Delete the project
    print(f"==== Deleting project {project_id} ====")
    delete_project(token, project_id)
    print("Project deleted successfully")
    print()


def choose_create_and_get_solution(token: Token):
    print("1) Create example project and print solution")
    print("2) Print solution of existing project")
    print()
    while True:
        choice = input("Choose: ")
        if choice == "1":
            project_id = create_example_project(token)["id"]
            print("Project ID:", project_id)
        elif choice == "2":
            project_id = input("Project ID: ")
        else:
            print(f"Unknown choice '{choice}'")
            continue
        break

    print_solution_continuously(token, project_id)


def print_solution_continuously(token: Token, project_id: int):
    while True:
        solution = get_project_solution(token.get(), project_id)
        print()
        print("==== SOLUTION ====")
        pprint(solution)
        sleep(10)
        print()
        print()


if __name__ == "__main__":
    token = DeviceAuth(Config).token()
    choose_create_and_get_solution(token)
