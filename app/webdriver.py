import feedparser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def start_webdriver():
    """Start a webdriver session and return the driver."""

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    print("Starting webdriver...")
    return driver


def quit_webdriver(driver):
    print("Quitting webdriver...")
    driver.quit()


def fetch_rss_entries(url, type):
    """Fetch and return entries from an RSS feed."""

    if type == "meetings":
        document = feedparser.parse(url)
        return document.entries
    if type == "legislation":
        document = feedparser.parse(url)
        feed_title = {"feed_title": document.feed.title}
        document.entries.insert(0, feed_title)
        return document.entries
