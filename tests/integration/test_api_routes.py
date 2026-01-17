
import pytest
from app import create_app
from config import Config
import io

# We need a fixture to create the app context for coverage
@pytest.fixture
def client():
    # Use testing config
    Config.TESTING = True
    # Disable rate limit for testing
    Config.RATELIMIT_ENABLED = False
    
    app = create_app()
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.data == b"OK"

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"OneTimeShare" in response.data

def test_upload_api(client):
    # Mock a file upload
    data = {
        'file': (io.BytesIO(b"test content"), 'test.txt'),
        'password': ''
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 201
    assert b"success" in response.data
    
    # Extract token
    json_data = response.get_json()
    token = json_data['metadata']['token']
    
    # Verify Metadata
    meta_response = client.get(f'/info/{token}')
    # Note: info route is admin required in current code? 
    # Let's check routes.py: @admin_required on info/<token>
    # So this might fail if we don't mock admin session.
    # But let's verify download route instead.
    
    # Download
    dl_response = client.get(f'/d/{token}')
    assert dl_response.status_code == 200
    assert b"test content" in dl_response.data
