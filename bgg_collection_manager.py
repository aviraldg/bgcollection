from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

BGG_BASE_URL = "https://boardgamegeek.com"


def setup_driver():
    """Sets up the Chrome WebDriver."""
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    return driver


def login_to_bgg(driver):
    """Handles the login process for BoardGameGeek."""
    print("Please log in to BoardGameGeek in the opened browser window.")
    print(f"Navigate to: {BGG_BASE_URL}")
    input("Press Enter after you have successfully logged in and are on the BGG homepage...")


def add_game_to_collection(driver, game):
    """Adds a single game to the user's BGG collection."""
    title = game.get("title")
    url = game.get("url")

    if not url:
        print(f"Skipping '{title}': No URL found.")
        return

    match = re.search(r'/boardgame/(\d+)', url)
    if not match:
        print(f"Skipping '{title}': Invalid BGG URL format.")
        return

    game_id = match.group(1)
    game_page_url = f"{BGG_BASE_URL}/boardgame/{game_id}"

    print(f"Processing '{title}' (ID: {game_id})...")
    try:
        driver.get(game_page_url)
        time.sleep(2)  # Give page time to load

        # Check if already in collection
        try:
            owned_status_link = driver.find_element(By.XPATH, "//a[contains(@class, 'collection-status-owned')] | //span[contains(@class, 'collection-status-owned')] | //div[contains(@class, 'collection-status-owned')] ")
            if owned_status_link.is_displayed():
                print(f"'{title}' is already in your collection as 'Owned'. Skipping.")
                return
        except:
            pass  # Not found, proceed to add

        # Click "Add to Collection"
        add_to_collection_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Add to Collection')] | //button[contains(text(), 'Add to Collection')] "))
        )
        if add_to_collection_button:
            add_to_collection_button.click()
            print(f"Clicked 'Add to Collection' for '{title}'.")
            time.sleep(3)

            # Mark as "Owned" and save
            owned_checkbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "owned"))
            )
            if not owned_checkbox.is_selected():
                owned_checkbox.click()
                print(f"Selected 'Owned' status for '{title}'.")

            save_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Save')] | //input[@value='Save']"))
            )
            save_button.click()
            print(f"Saved collection status for '{title}'.")
            time.sleep(2)

    except Exception as e:
        print(f"An error occurred while processing '{title}': {e}")
    finally:
        time.sleep(5)
