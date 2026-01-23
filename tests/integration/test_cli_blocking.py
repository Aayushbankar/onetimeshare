
import pytest
from app import create_app
from config import Config
import io

@pytest.fixture
def client():
    Config.TESTING = True
    Config.RATELIMIT_ENABLED = False
    Config.WTF_CSRF_ENABLED = False
    app = create_app()
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_cli_blocking_protected(client):
    """Test that CLI tools are blocked when accessing protected files."""
    # 1. Upload a file (Protected)
    data = {
        'file': (io.BytesIO(b"secret content"), 'secret.txt'),
        'password': 'password123'
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    token = response.get_json()['metadata']['token']

    # 2. Try to access with curl (Should be BLOCKED)
    # User's current implementation returns 406
    cli_response = client.get(f'/d/{token}', headers={'User-Agent': 'curl/7.68.0'})
    assert cli_response.status_code == 406
    assert b"Access Denied for CLI Tools" in cli_response.data

    # 3. Try to access with Browser (Should be ALLOWED -> Password Page)
    browser_response = client.get(f'/d/{token}', headers={'User-Agent': 'Mozilla/5.0'})
    assert browser_response.status_code == 200
    assert b"Enter decryption key..." in browser_response.data

def test_cli_blocking_unprotected(client):
    """Test that CLI tools are blocked when accessing unprotected files."""
    # 1. Upload a file (Unprotected)
    data = {
        'file': (io.BytesIO(b"public content"), 'public.txt'),
        'password': ''
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    token = response.get_json()['metadata']['token']

    # 2. Try to access with wget (Should be BLOCKED)
    cli_response = client.get(f'/d/{token}', headers={'User-Agent': 'Wget/1.20'})
    assert cli_response.status_code == 406
    assert b"Access Denied for CLI Tools" in cli_response.data

    # 3. Try to access with Browser (Should be ALLOWED -> Download/Serve)
    # Note: Unprotected files redirect to serve_and_delete logic if type=False logic in routes is hit
    # But wait, routes logic says:
    # elif metadata.get('is_protected') == 'False': return serve_and_delete(...)
    # So browser should get the FILE directly (if serve_and_delete returns file) 
    # OR if it's the view page route (wait, /d/ is download route, /download/ is view page)
    # The vulnerability was about /d/ route.
    browser_response = client.get(f'/d/{token}', headers={'User-Agent': 'Mozilla/5.0'})
    assert browser_response.status_code == 200
    # It should serve the file content
    assert b"public content" in browser_response.data
