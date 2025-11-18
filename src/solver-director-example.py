from time import sleep
from device_auth import DeviceAuth
from config import Config
import requests
from pprint import pprint


def main():
    access_token, refresh_token = DeviceAuth(Config).get_token()
    print("==== Access token ====")
    print(access_token)
    print()
    print("==== Refresh token ====")
    print(refresh_token)
    print()

    # Example workflow: Create, read, and delete a project



    # 1. Create a new project
    print("==== Creating a new project ====")
    project_config = {
        "name": "Test Project",
        "configuration": [
            {
                "problemGroup": 1,
                "solvers": [1, 2],
                "problems": [
                    {"problem": 10, "instances": [1, 2, 3]},
                    {"problem": 11, "instances": [4, 5]},
                ],
            }
        ]
    }
    new_project = create_project(access_token, project_config)
    pprint(new_project)
    project_id = new_project["id"]
    print()

    # 2. List all projects
    print("==== Listing all projects ====")
    all_projects = get_projects(access_token)
    pprint(all_projects)
    print()

    sleep(8)
    # 3. Get project status
    print(f"==== Getting project {project_id} status ====")
    status = get_project_status(access_token, project_id)
    pprint(status)
    print()

    # 4. Get project configuration
    print(f"==== Getting project {project_id} configuration ====")
    config = get_project_config(access_token, project_id)
    pprint(config)
    print()

    # 5. Try to get project solution (not implemented yet)
    print(f"==== Getting project {project_id} solution ====")
    try:
        solution = get_project_solution(access_token, project_id)
        pprint(solution)
    except requests.HTTPError as e:
        print(f"Expected error: {e}")
    print()

    # 6. Delete the project
    print(f"==== Deleting project {project_id} ====")
    delete_project(access_token, project_id)
    print("Project deleted successfully")
    print()


def create_project(token: str, config: dict) -> dict:
    """Create a new project - requires projects:write scope"""
    response = requests.post(
        "http://local/api/solverdirector/v1/projects",
        headers={"Authorization": f"Bearer {token}"},
        json=config,
        timeout=Config.Timeout.default,
    )
    response.raise_for_status()
    return response.json()


def get_projects(token: str) -> list:
    """Get all projects for the authenticated user - requires projects:read scope"""
    response = requests.get(
        "http://local/api/solverdirector/v1/projects",
        headers={"Authorization": f"Bearer {token}"},
        timeout=Config.Timeout.default,
    )
    response.raise_for_status()
    return response.json()


def get_project_status(token: str, project_id: str) -> dict:
    """Get project status with solver controller info - requires projects:read scope"""
    response = requests.get(
        f"http://local/api/solverdirector/v1/projects/{project_id}/status",
        headers={"Authorization": f"Bearer {token}"},
        timeout=Config.Timeout.default,
    )
    response.raise_for_status()
    return response.json()


def get_project_config(token: str, project_id: str) -> dict:
    """Get project configuration - requires projects:read scope"""
    response = requests.get(
        f"http://local/api/solverdirector/v1/projects/{project_id}/config",
        headers={"Authorization": f"Bearer {token}"},
        timeout=Config.Timeout.default,
    )
    response.raise_for_status()
    return response.json()


def get_project_solution(token: str, project_id: str) -> dict:
    """Get project solution/results - requires projects:read scope (not yet implemented)"""
    response = requests.get(
        f"http://local/api/solverdirector/v1/projects/{project_id}/solution",
        headers={"Authorization": f"Bearer {token}"},
        timeout=Config.Timeout.default,
    )
    response.raise_for_status()
    return response.json()


def delete_project(token: str, project_id: str) -> None:
    """Delete a project - requires projects:write scope"""
    response = requests.delete(
        f"http://local/api/solverdirector/v1/projects/{project_id}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=Config.Timeout.default,
    )
    response.raise_for_status()


if __name__ == "__main__":
    main()
