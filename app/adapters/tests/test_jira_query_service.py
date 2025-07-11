import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from app.adapters.jira_query_service import JiraQueryService
from app.domain.model.task import Task
import requests

@pytest.fixture
def jira_service():
    return JiraQueryService()

@pytest.fixture
def mock_env_vars():
    env_vars = {
        "JIRA_URL": "https://your-domain.atlassian.net",
        "JIRA_TOKEN": "dummy-token",
        "JIRA_ASSIGNEE_ID": "user123"
    }
    with patch.dict('os.environ', env_vars):
        yield env_vars

def test_get_today_tasks_success(jira_service, mock_env_vars):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "issues": [{
            "fields": {
                "summary": "Test Task",
                "description": "Test Description",
                "status": {"name": "In Progress"},
                "assignee": {"displayName": "John Doe"}
            },
            "self": "https://jira.example.com/rest/api/3/issue/123"
        }]
    }
    
    expected_date = datetime.now().strftime('%Y-%m-%d')
    expected_url = f"{mock_env_vars['JIRA_URL']}/rest/api/3/search"
    
    with patch('requests.get', return_value=mock_response) as mock_get:
        tasks = jira_service.get_today_tasks()
        
        mock_get.assert_called_once_with(expected_url)
        assert len(tasks) == 1
        assert isinstance(tasks[0], Task)
        assert tasks[0].title == "Test Task"
        assert tasks[0].description == "Test Description"
        assert tasks[0].status == "In Progress"
        assert tasks[0].source == "JIRA"
        assert tasks[0].url == "https://jira.example.com/rest/api/3/issue/123"
        assert tasks[0].assignee == "John Doe"

def test_get_today_tasks_missing_env_vars(jira_service):
    with patch.dict('os.environ', {}, clear=True):
        with pytest.raises(ValueError) as exc_info:
            jira_service.get_today_tasks()
        assert str(exc_info.value) == "JIRA_URL, JIRA_TOKEN, and JIRA_ASSIGNEE_ID must be set"

def test_get_today_tasks_api_error(jira_service, mock_env_vars):
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("API Error")
        with pytest.raises(requests.exceptions.RequestException):
            jira_service.get_today_tasks()

def test_get_today_tasks_empty_response(jira_service, mock_env_vars):
    mock_response = MagicMock()
    mock_response.json.return_value = {"issues": []}
    
    with patch('requests.get', return_value=mock_response):
        tasks = jira_service.get_today_tasks()
        assert len(tasks) == 0
