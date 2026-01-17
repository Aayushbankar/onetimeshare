
import re
import pytest
from playwright.sync_api import Page, expect

def test_full_lifecycle_share(page: Page):
    """
    Test the complete flow:
    1. Upload a file
    2. Get the share link
    3. Download the file
    4. Verify the link is expired (404/410)
    """
    # --- STEP 1: UPLOAD ---
    page.goto("http://localhost:5000")
    
    # Create a dummy file
    page.locator("input[type='file']").set_input_files("tests/test_data.txt")
    
    # Click Upload
    page.get_by_role("button", name="Upload").click()
    
    # Verify Success Page
    expect(page.locator("h2.success-title")).to_contain_text("FILE UPLOADED")
    
    # --- STEP 2: GET LINK ---
    # The link is in an input with id="share-link"
    # Wait for the input to be populated
    expect(page.locator("#share-link")).not_to_be_empty()
    share_link = page.locator("#share-link").input_value()
    assert "/download/" in share_link
    
    # --- STEP 3: DOWNLOAD PHASE ---
    # Navigate to the download link
    page.goto(share_link)
    
    # Verify Download Page content
    expect(page.locator("h2.success-title")).to_contain_text("FILE AVAILABLE")
    expect(page.locator("body")).to_contain_text("test_data.txt")
    
    # Start download
    # In Playwright, we wait for the download event
    with page.expect_download() as download_info:
        # Click the download button (class btn-primary inside download-button div)
        page.get_by_role("link", name="DOWNLOAD").click()
        
    download = download_info.value
    # Verify filename
    assert download.suggested_filename == "test_data.txt"
    
    # --- STEP 4: VERIFY EXPIRATION ---
    # Reload the page or visit link again
    page.goto(share_link)
    
    # Expect Error Page "LOST IN SPACE" (404)
    expect(page.locator("h2.error-title")).to_contain_text("LOST IN SPACE")
    expect(page.locator(".warning-box")).to_contain_text("deleted, expired")
