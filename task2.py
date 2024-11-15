# Import necessary libraries
from bs4 import BeautifulSoup  # For parsing HTML content
from selenium import webdriver  # For automating web browser interaction
import time  # For adding delays
import csv  # For saving data to CSV files
import re  # For regular expression operations

# Set the path to your ChromeDriver executable
PATH = "C:\\driver\\chromedriver.exe"  # Use double backslashes for Windows paths

# Initialize an empty list to store profile data
l = []

# List of Twitter profile URLs to scrape
target_urls = [
    "https://twitter.com/GTNUK1",
    "https://twitter.com/whatsapp",
    "https://twitter.com/aacb_CBPTrade",
    "https://twitter.com/aacbdotcom",
    "https://twitter.com/@AAWindowPRODUCT",
    "https://www.twitter.com/aandb_kia",
    "https://twitter.com/ABHomeInc",
    "https://twitter.com/Abrepro",
    "http://www.twitter.com",
    "https://twitter.com/ACChristofiLtd",
    "https://twitter.com/aeclothing1",
    "http://www.twitter.com/",
    "https://twitter.com/AETechnologies1",
    "http://www.twitter.com/wix",
    "https://twitter.com/AGInsuranceLLC"
]

# Function to normalize URLs by removing 'www.' and '@'
def normalize_url(url):
    url = url.replace("www.", "")  # Remove 'www.' from URL if present
    url = url.replace("@", "")      # Remove '@' from URL if present
    return url

# Function to scrape profile data from a given URL
def scrape_profile(url):
    driver = webdriver.Chrome(PATH)  # Initialize the Chrome WebDriver
    driver.get(normalize_url(url))   # Navigate to the normalized URL
    time.sleep(5)                    # Wait for the page to load completely

    resp = driver.page_source         # Get the page source HTML content
    driver.close()                    # Close the browser window

    soup = BeautifulSoup(resp, 'html.parser')  # Parse the HTML content with BeautifulSoup
    o = {}  # Dictionary to hold the scraped data for this profile

    # Extract and clean the profile bio
    try:
        bio = soup.find("div", {"data-testid": "UserDescription"}).text  # Locate bio element
        o["profile_bio"] = re.sub(r"http\S+|www\S+", "", bio).strip()  # Remove URLs from bio text
    except:
        o["profile_bio"] = None  # If extraction fails, set bio to None

    profile_header = soup.find("div", {"data-testid": "UserProfileHeader_Items"})  # Locate header items

    # Extract profile website URL if available
    try:
        o["profile_website"] = profile_header.find('a').get('href')  # Get website link from header
    except:
        o["profile_website"] = None  # If extraction fails, set website to None

    # Extract profile location if available
    try:
        o["profile_location"] = profile_header.find("span", {"data-testid": "UserLocation"}).text.strip()  # Get location text
    except:
        o["profile_location"] = None  # If extraction fails, set location to None

    # Extract following count from profile statistics
    try:
        following = soup.find_all("a", {"class": "r-rjixqe"})[0].text  # Locate following count element
        o["profile_following"] = re.sub(r"\D", "", following)  # Remove non-digit characters from following count
    except:
        o["profile_following"] = None  # If extraction fails, set following count to None

    # Extract followers count from profile statistics
    try:
        followers = soup.find_all("a", {"class": "r-rjixqe"})[1].text  # Locate followers count element
        o["profile_followers"] = re.sub(r"\D", "", followers)  # Remove non-digit characters from followers count
    except:
        o["profile_followers"] = None  # If extraction fails, set followers count to None

    l.append(o)  # Append the scraped data dictionary to the list

# Scrape all profiles in the target URLs list
for url in target_urls:
    scrape_profile(url)

# Save scraped data to a CSV file named 'twitter_profiles.csv'
with open('twitter_profiles.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["profile_bio", "profile_website", "profile_location", "profile_following", "profile_followers"])  # Define CSV column headers
    writer.writeheader()  # Write header row to CSV file
    
    for profile in l:     # Iterate through each profile's data in the list
        writer.writerow(profile)  # Write each profile's data as a new row in the CSV file

print("Data saved to twitter_profiles.csv")  # Confirmation message after saving data
