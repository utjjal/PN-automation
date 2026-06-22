import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select  # Imported for handling dropdowns

# 1. Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
profile_path = os.path.join(script_dir, "chrome_profile")
csv_path = os.path.join(script_dir, "data.csv")

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument(f"--user-data-dir={profile_path}")
options.add_argument('--ignore-certificate-errors')

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

try:
    driver.get("https://ss-dev-adminpanel-705829581.us-west-2.elb.amazonaws.com/dashboard")
    print("Webpage loaded. Starting loop...")

    with open(csv_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for index, row in enumerate(csv_reader, start=1):
            deeplink_data = row['Deeplink']
            rewards_data = row['Rewards']
            
            # --- STEP 1: Input text data ---
            link_id_box = wait.until(EC.presence_of_element_located((By.NAME, "LinkId")))
            reward_box = wait.until(EC.presence_of_element_located((By.ID, "reward_amount")))
            
            link_id_box.clear()
            link_id_box.send_keys(deeplink_data)
            
            reward_box.clear()
            reward_box.send_keys(rewards_data)
            
            # --- STEP 2: Handle the 3 Dropdowns based on the Deeplink content ---
            # !!! REPLACE placeholders with actual dropdown element IDs/Names !!!
            drop1_element = wait.until(EC.presence_of_element_located((By.ID, "dropdown_one_id")))
            drop2_element = wait.until(EC.presence_of_element_located((By.ID, "dropdown_two_id")))
            drop3_element = wait.until(EC.presence_of_element_located((By.ID, "dropdown_three_id")))
            
            select1 = Select(drop1_element)
            select2 = Select(drop2_element)
            select3 = Select(drop3_element)
            
            # Smart Decision Logic
            # Example: If the link contains the word "google", select specific options.
            if "coins" in deeplink_data.lower():
                select1.select_by_visible_text("Free Coins!")
            elif "tickets" in deeplink_data.lower():
                select1.select_by_visible_text("Free Tickets!")
            else:
                # Default backup options if no keywords match
                select1.select_by_visible_text("Default Option")
                select2.select_by_visible_text("Default Category")
                select3.select_by_visible_text("Pending")
                
            print(f"Row {index}: Text fields filled and dropdowns mapped.")

            # --- STEP 3: Click the Submit Button ---
            # !!! REPLACE with your actual Submit Button element selector !!!
            submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "deeplink_submit")))
            submit_btn.click()
            print("Submit pressed.")
            
            # Small pause to allow the database to register the submission
            time.sleep(2.0)

            # --- STEP 4: Click 'New Deeplink' to reset the form for the next loop iteration ---
            # !!! REPLACE with your actual New Deeplink Button element selector !!!
            new_deeplink_btn = wait.until(EC.element_to_be_clickable((By.ID, "/deeplinks/edit")))
            new_deeplink_btn.click()
            print("Form reset via 'New Deeplink' button.")
            
            # Small buffer pause before restarting the loop
            time.sleep(1.5)

    print("Finished! All rows processed flawlessly.")

except Exception as e:
    print(f"An error occurred: {e}")