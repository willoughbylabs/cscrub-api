import feedparser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def start_webdriver():
    """Start a webdriver session and return the driver."""

    print("Starting webdriver...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver


def quit_webdriver(driver):
    print("Quitting webdriver...")
    driver.quit()


def fetch_rss_entries(url, type):
    """Fetch and return entries from an RSS feed."""

    if type == "meetings":
        document = feedparser.parse(url)
        return document.entries
