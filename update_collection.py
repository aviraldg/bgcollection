from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import re
import time

JSON_FILE_PATH = "/home/aviraldg/Downloads/boardgames.json"
BGG_BASE_URL = "https://boardgamegeek.com"

def update_bgg_collection():
    try:
        with open(JSON_FILE_PATH, 'r') as f:
            boardgames_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {JSON_FILE_PATH}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {JSON_FILE_PATH}")
        return

    # Setup Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    print("Please log in to BoardGameGeek in the opened browser window.")
    print(f"Navigate to: {BGG_BASE_URL}")
    input("Press Enter after you have successfully logged in and are on the BGG homepage...")

    for game in boardgames_data:
        title = game.get("title")
        url = game.get("url")

        if not url:
            print(f"Skipping '{title}': No URL found.")
            continue

        match = re.search(r'/boardgame/(\d+)', url)
        if not match:
            print(f"Skipping '{title}': Invalid BGG URL format.")
            continue

        game_id = match.group(1)
        game_page_url = f"{BGG_BASE_URL}/boardgame/{game_id}"

        print(f"Processing '{title}' (ID: {game_id})...")
        try:
            driver.get(game_page_url)
            time.sleep(2) # Give page time to load

            # Check if already in collection (e.g., "Owned" status is visible)
            try:
                # Look for the 'Owned' status link/button, which indicates it's already in collection
                owned_status_link = driver.find_element(By.XPATH, "//a[contains(@class, 'collection-status-owned')] | //span[contains(@class, 'collection-status-owned')] | //div[contains(@class, 'collection-status-owned')] ")
                if owned_status_link.is_displayed():
                    print(f"'{title}' is already in your collection as 'Owned'. Skipping.")
                    continue
            except:
                pass # Not found, proceed to add

            # Try to find and click the "Add to Collection" button
            add_to_collection_button = None
            try:
                # Attempt 1: Find by text content (most common)
                add_to_collection_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Add to Collection')] | //button[contains(text(), 'Add to Collection')] "))
                )
            except:
                try:
                    # Attempt 2: Find by a common class name for collection buttons
                    add_to_collection_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'collection-add-button')] | //button[contains(@class, 'collection-add-button')] "))
                    )
                except:
                    print(f"Could not find 'Add to Collection' button for '{title}'.")
                    continue

            if add_to_collection_button:
                add_to_collection_button.click()
                print(f"Clicked 'Add to Collection' for '{title}'.")
                time.sleep(3) # Wait for modal to appear and load

                # Now, try to find and click the "Owned" checkbox within the modal
                try:
                    owned_checkbox = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "owned")) # Common ID for owned checkbox
                    )
                    if not owned_checkbox.is_selected():
                        owned_checkbox.click()
                        print(f"Selected 'Owned' status for '{title}'.")
                    else:
                        print(f"'{title}' already marked as 'Owned' in modal.")

                    # Find and click the 'Save' button in the modal
                    save_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Save')] | //input[@value='Save']"))
                    )
                    save_button.click()
                    print(f"Saved collection status for '{title}'.")
                    time.sleep(2) # Wait for save to process
                except Exception as e:
                    print(f"Error interacting with collection modal for '{title}': {e}")
                    # If modal interaction fails, try to close it to proceed
                    try:
                        close_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Cancel')] | //a[contains(text(), 'Cancel')] ")
                        close_button.click()
                        time.sleep(1)
                    except:
                        pass # Couldn't close, just move on

        except Exception as e:
            print(f"An error occurred while processing '{title}': {e}")
        finally:
            time.sleep(5) # Longer delay between games to be safe

    driver.quit()
    print("Script finished. Check your BoardGameGeek collection.")

if __name__ == "__main__":
    update_bgg_collection()
