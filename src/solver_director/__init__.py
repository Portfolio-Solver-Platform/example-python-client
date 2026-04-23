import requests
from config import Config
from auth import Token

url = "http://psp.jonasbork.dk"


def create_project(token: Token, config: dict) -> dict:
    """Create a new project - requires projects:write scope"""
    response = requests.post(
        f"{url}/api/solverdirector/v1/projects",
        headers={"Authorization": f"Bearer {token.get()}"},
        json=config,
        timeout=Config.Timeout.default,
    )
    response.raise_for_status()
    return response.json()


def get_projects(token: Token) -> list:
    """Get all projects for the authenticated user - requires projects:read scope"""
    response = requests.get(
        f"{url}/api/solverdirector/v1/projects",
        headers={"Authorization": f"Bearer {token.get()}"},
        timeout=Config.Timeout.default,
    )
    response.raise_for_status()
    return response.json()


def get_project_status(token: Token, project_id: str) -> dict:
    """Get project status with solver controller info - requires projects:read scope"""
    response = requests.get(
        f"{url}/api/solverdirector/v1/projects/{project_id}/status",
        headers={"Authorization": f"Bearer {token.get()}"},
        timeout=Config.Timeout.default,
    )
    response.raise_for_status()
    return response.json()


def get_project_config(token: Token, project_id: str) -> dict:
    """Get project configuration - requires projects:read scope"""
    response = requests.get(
        f"{url}/api/solverdirector/v1/projects/{project_id}/config",
        headers={"Authorization": f"Bearer {token.get()}"},
        timeout=Config.Timeout.default,
    )
    response.raise_for_status()
    return response.json()


def get_project_solution(token: Token, project_id: str) -> dict:
    """Get project solution/results - requires projects:read scope (not yet implemented)"""
    response = requests.get(
        f"{url}/api/solverdirector/v1/projects/{project_id}/solution",
        headers={"Authorization": f"Bearer {token.get()}"},
        timeout=Config.Timeout.default,
    )
    response.raise_for_status()
    return response.json()


def delete_project(token: Token, project_id: str) -> None:
    """Delete a project - requires projects:write scope"""
    response = requests.delete(
        f"{url}/api/solverdirector/v1/projects/{project_id}",
        headers={"Authorization": f"Bearer {token.get()}"},
        timeout=Config.Timeout.default,
    )
    response.raise_for_status()
