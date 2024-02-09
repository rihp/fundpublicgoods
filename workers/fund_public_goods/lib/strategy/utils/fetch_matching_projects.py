from fund_public_goods.db import tables
from fund_public_goods.db.entities import Projects
from fund_public_goods.lib.strategy.utils.get_top_matching_projects import get_top_matching_projects


def fetch_matching_projects(prompt: str) -> list[Projects]:
    project_ids = get_top_matching_projects(prompt)[:10]
    projects = tables.projects.get_all(project_ids)
    return projects
