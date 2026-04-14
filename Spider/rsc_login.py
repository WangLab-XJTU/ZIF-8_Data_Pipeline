# rsc_login.py

from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("goto Login page")
        page.goto("https://pubs.rsc.org/doi/10.1039/c9cc08724a")

        
        print("enter your password")
        
        # waiting for login succeed
        page.wait_for_selector("#divWelcomeUser > span", timeout=0) 

        # save state file
        context.storage_state(path="auth_state.json")
        print("State saved auth_state.json")
        
        browser.close()

if __name__ == "__main__":
    run()