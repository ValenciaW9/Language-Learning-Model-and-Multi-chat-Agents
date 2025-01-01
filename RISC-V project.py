import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Function to download all PDFs from a given Arxiv page
def download_pdfs(driver, folder_path):
    # Find all PDF links on the current page
    pdf_links = driver.find_elements(By.XPATH, '//a[contains(@href, "/pdf/")]')

    for link in pdf_links:
        try:
            pdf_url = link.get_attribute('href')
            pdf_name = pdf_url.split('/')[-1] + ".pdf"  # Generate a simple filename from the PDF link
            pdf_path = os.path.join(folder_path, pdf_name)

            # Download the PDF only if it doesn't already exist in the folder
            if not os.path.exists(pdf_path):
                response = requests.get(pdf_url)
                if response.status_code == 200:
                    with open(pdf_path, 'wb') as file:
                        file.write(response.content)
                    print(f'Downloaded: {pdf_name}')
                else:
                    print(f'Failed to download {pdf_name}: HTTP {response.status_code}')
            else:
                print(f'Already exists: {pdf_name}')

            time.sleep(1)  # Small delay to ensure the page loads properly before continuing
        except (NoSuchElementException, TimeoutException, requests.RequestException) as e:
            print(f"Error downloading {pdf_name}: {e}")
            continue

# Function to navigate to the next page
def go_to_next_page(driver):
    try:
        next_button = driver.find_element(By.LINK_TEXT, "Next")
        next_button.click()
        time.sleep(2)  # Wait for the next page to load
        return True
    except NoSuchElementException:
        return False

# Main function to scrape Arxiv
def scrape_arxiv(url, folder_name):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode, remove if you want to see the browser action
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Setup Chrome driver using the default path
    service = Service()  # Since ChromeDriver is in the PATH, you don't need to specify a path
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Create a directory for the downloads
        folder_path = os.path.join(os.getcwd(), f'Archive X - {folder_name}')
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        driver.get(url)

        while True:
            # Download PDFs on the current page
            download_pdfs(driver, folder_path)

            # Check if there is a next page, and navigate to it if exists
            if not go_to_next_page(driver):
                break  # No next page, exit the loop

    finally:
        driver.quit()
        print(f"All PDFs downloaded in folder: {folder_path}")

# Example usage:
if __name__ == "__main__":
    arxiv_url = input("Enter the Arxiv URL: ")
    folder_name = input("Enter the name for the folder: ")
    scrape_arxiv(arxiv_url, folder_name)