

from playwright.sync_api  import Page , expect
import pytest
import re 


def test_homepage_has_title(page: Page):
    page.goto("http://localhost:5000")
    
    # Expect a title "OneTimeShare"
    expect(page).to_have_title(re.compile("OneTimeShare"))



def test_upload_flow(page: Page):
    page.goto("http://localhost:5000")
    
    # Fill input (if hidden file input, use specialized locator)
    # Testing file upload usually requires locating input[type="file"]
    page.locator("input[type='file']").set_input_files("tests/test_data.txt")
    
    # Start upload
    page.get_by_role("button", name="Upload").click()
    
    # Verify success
    # Verify success
    expect(page.locator("h2.success-title")).to_contain_text("FILE UPLOADED")