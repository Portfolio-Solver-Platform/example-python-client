import requests
from config import Config


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
