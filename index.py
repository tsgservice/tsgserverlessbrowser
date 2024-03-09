import json
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

async def extract_table_data():
    options = Options()
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')

    # Initialize webdriver
    driver = webdriver.Chrome(options=options)
    try:
        # Navigate to webpage
        driver.get("https://cfonline.labour.gov.za/VerifyLOGS/?0")
        await asyncio.sleep(5)  # Adjust sleep time as necessary

        # Find input field and submit number
        input_field = driver.find_element(By.ID, 'cert')
        input_field.clear()
        input_field.send_keys('2022185380')
        input_field.send_keys(Keys.RETURN)

        # Wait for the table to load
        await asyncio.sleep(5)  # Adjust sleep time as necessary

        # Find the table and extract data
        table = driver.find_element(By.TAG_NAME, 'table')
        headers = [cell.text for cell in table.find_elements(By.TAG_NAME, "th")]
        rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip header row
        data = []
        for row in rows:
            row_data = [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
            data.append(dict(zip(headers, row_data)))

        # Convert data to JSON
        json_data = json.dumps(data, indent=4)
        return json_data

    finally:
        # Close the webdriver
        driver.quit()

async def my_async_function():
    table_data = await extract_table_data()
    print(table_data)

# Call my_async_function
asyncio.run(my_async_function())
