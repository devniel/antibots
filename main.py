from playwright.sync_api import sync_playwright
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
        
    # Visit all followers profile page
    print("Checking followers...")
    for user in users:
        print(f"Checking user {user["username"]} ...")
        page.goto(f"https://x.com/{user["username"]}")
        page.wait_for_timeout(2000)
                        
        # Get user posts
        posts = page.query_selector_all("[aria-label='Home timeline'] [role=heading] ~ div")[0].text_content()
        posts = int(re.sub(r"[,K.]", "", posts, flags=re.IGNORECASE).removesuffix("posts").rstrip())
    
        # unfollow if no posts were found
        if posts == 0:
            print(f"User {user["username"]} has 0 posts, removing as follower...")
            page.get_by_test_id("userActions").click()
            page.get_by_text("Remove this follower").click()
            page.get_by_test_id("confirmationSheetConfirm").click()
    
