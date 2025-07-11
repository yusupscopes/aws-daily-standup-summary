"""
Unit tests for the Lambda handler.
"""
import json
import os
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock

import pytest

from app.entrypoints.lambda_handler import lambda_handler

@pytest.fixture
def mock_env_vars():
    """Fixture to set up mock environment variables."""
    with patch.dict(os.environ, {
        'ENVIRONMENT': 'test',
        'SNS_TOPIC_ARN': 'arn:aws:sns:us-east-1:123456789012:test-topic'
    }):
        yield

@pytest.fixture
def lambda_event():
    """Fixture to provide a sample Lambda event."""
    return {}

@pytest.fixture
def lambda_context():
    """Fixture to provide a mock Lambda context."""
    context = MagicMock()
    context.function_name = 'test-function'
    context.function_version = '$LATEST'
    return context

def test_lambda_handler_success(mock_env_vars, lambda_event, lambda_context):
    """Test successful execution of the Lambda handler."""
    # Execute the handler
    response = lambda_handler(lambda_event, lambda_context)
    
    # Assert the response structure and status code
    assert response['statusCode'] == 200
    
    # Parse the response body
    body = json.loads(response['body'])
    assert 'message' in body
    assert 'timestamp' in body
    assert body['message'] == 'Daily standup summary generation initiated'
    
    # Verify timestamp is in ISO format and can be parsed
    timestamp = datetime.fromisoformat(body['timestamp'])
    assert isinstance(timestamp, datetime)
    assert timestamp.tzinfo == timezone.utc

def test_lambda_handler_with_exception(mock_env_vars, lambda_event, lambda_context):
    """Test Lambda handler when an exception occurs."""
    # Mock os.environ.get to raise an exception
    with patch('os.environ.get', side_effect=Exception('Test error')):
        response = lambda_handler(lambda_event, lambda_context)
        
        # Assert error response
        assert response['statusCode'] == 500
        
        # Parse the error body
        body = json.loads(response['body'])
        assert 'error' in body
        assert 'message' in body
        assert body['error'] == 'Test error'
        assert body['message'] == 'Failed to generate daily standup summary'

def test_lambda_handler_environment_variables(mock_env_vars, lambda_event, lambda_context):
    """Test Lambda handler's handling of environment variables."""
    response = lambda_handler(lambda_event, lambda_context)
    
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    
    # Verify the handler executed successfully with mock environment variables
    assert os.environ.get('ENVIRONMENT') == 'test'
    assert os.environ.get('SNS_TOPIC_ARN') == 'arn:aws:sns:us-east-1:123456789012:test-topic'
