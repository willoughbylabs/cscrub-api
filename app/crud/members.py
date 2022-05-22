import models, schemas
import time
import webdriver
from selenium import webdriver as swd
from selenium.webdriver.common.keys import Keys


def fetch_members():
    """Fetch City Council members from City Clerk's website."""

    members = []
    url = "https://chicago.legistar.com/People.aspx"

    driver = webdriver.start_webdriver()

    driver.get(url)
    time.sleep(1)
    # Select "all" from view menu
    view_btn = driver.find_element_by_xpath(
        "//*[@id='ctl00_ContentPlaceHolder1_menuPeople']/ul/li[4]/a"
    )
    view_btn.click()
    time.sleep(1)
    # Select "page 1" from view menu
    swd.ActionChains(driver).send_keys(Keys.ARROW_DOWN).send_keys(
        Keys.ARROW_DOWN
    ).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
    page1_members = driver.find_elements_by_xpath("//*[contains(@id,'_hypPerson')]")
    for member in page1_members:
        members.append(member.text)
    # Select "page 2" from view menu
    page2 = driver.find_element_by_xpath(
        "//*[@id='ctl00_ContentPlaceHolder1_gridPeople_ctl00']/thead/tr[1]/td/table/tbody/tr/td/div[1]/a[2]"
    )
    page2.click()
    time.sleep(1)
    page2_members = driver.find_elements_by_xpath("//*[contains(@id,'_hypPerson')]")
    for member in page2_members:
        members.append(member.text)

    webdriver.quit_webdriver(driver)
    return members


def create_records(entries):
    """ "Creates a list of new Member row objects for inserting to the database."""

    members = []
    for entry in entries:
        member = create_member(entry)
        members.append(member)
    return members


def create_member(member: schemas.CreateMember):
    """Create a new Member ORM object."""

    db_member = models.Member(name=member)
    return db_member
