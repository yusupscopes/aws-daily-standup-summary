from app.domain.ports.tasks_query_service import TasksQueryService
from app.domain.model.task import Task
from typing import List
import requests
import os
from datetime import datetime

class JiraQueryService(TasksQueryService):
    def get_today_tasks(self) -> List[Task]:
        jira_url = os.environ.get("JIRA_URL")
        jira_token = os.environ.get("JIRA_TOKEN")
        assignee_id = os.environ.get("JIRA_ASSIGNEE_ID")

        if not jira_url or not jira_token or not assignee_id:
            raise ValueError("JIRA_URL, JIRA_TOKEN, and JIRA_ASSIGNEE_ID must be set")
        
        jql_query = f"assignee = {assignee_id} AND dueDate = {datetime.now().strftime('%Y-%m-%d')}"

        response = requests.get(
            f"{jira_url}/rest/api/3/search",
        )

        response.raise_for_status()

        tasks = []
        for item in response.json()["issues"]:
            tasks.append(Task(
                title=item["fields"]["summary"],
                description=item["fields"]["description"],
                status=item["fields"]["status"]["name"],
                source="JIRA",
                url=item["self"],
                assignee=item["fields"]["assignee"]["displayName"],
            ))
        return tasks