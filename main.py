from playwright.sync_api import sync_playwright, expect
import re

USERNAME = "devniel"

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    default_context = browser.contexts[0]
    page = default_context.pages[0]
    followers_page = f"https://x.com/{USERNAME}/followers"
    page.goto(followers_page)
    page.wait_for_timeout(1000)
    items = page.get_by_test_id("cellInnerDiv").all()
    # Get all followers in the page
    print(f"Getting all visible followers in {followers_page}")
    users = []
    for item in items:
        links = item.get_by_role("link").all()
        name = links[0].text_content()
        username = links[1].text_content().lstrip("@")
        users.append({
            "name": name,
            "username": username
        })
    print("Checking followers...")
    # Visit all followers profile page
    for user in users:
        print(f"Checking {user["username"]}...")
        page.goto(f"https://x.com/{user["username"]}")
        page.wait_for_timeout(2000)
        
        #screenshot_bytes = page.screenshot()
        #base64_screenshot = base64.b64encode(screenshot_bytes).decode()
        #response = analyzeImage(base64_screenshot, silent=True)
        
        # Get user name and username
        expect(page.get_by_test_id("UserName")).to_be_visible()
        text = page.get_by_test_id("UserName").all_text_contents()[0].removesuffix("Follows you")
        [name, username] = text.split("@")
        print(name, username)
        
        # Get user description
        # Seems not available if user didn't add it
        # expect(page.get_by_test_id("UserDescription")).to_be_visible()
        # text = page.get_by_test_id("UserDescription").all_text_contents()[0]
        # print(text)
        
        # Get user join data
        expect(page.get_by_test_id("UserJoinDate")).to_be_visible()
        text = page.get_by_test_id("UserJoinDate").all_text_contents()[0]
        print(text)
        
        # Get user posts
        posts = page.query_selector_all("[aria-label='Home timeline'] [role=heading] ~ div")[0].text_content()
        posts = int(re.sub(r"[,K.]", "", posts, flags=re.IGNORECASE).removesuffix("posts").rstrip())
        print(posts)
    
        # unfollow if no posts were found
        if posts == 0:
            page.get_by_test_id("userActions").click()
            page.get_by_text("Remove this follower").click()
            page.get_by_test_id("confirmationSheetConfirm").click()
    
