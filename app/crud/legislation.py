from . import meetings
from sqlalchemy.orm import Session
import config
import re
import models, schemas
import webdriver


def fetch_legislation(db: Session):
    """Fetch legislation from City Clerk RSS feed."""

    if config.set_legislation_links_list:
        links = config.links_list
    else:
        links = meetings.get_meeting_links(db)

    legislation_entries = []
    driver = webdriver.start_webdriver()

    for index, link in enumerate(links):
        try:
            driver.get(link)
            rss_btn = driver.find_element_by_xpath("//*[@id='ctl00_ButtonRSS']")
        except Exception as e:
            print(
                f"Error occured. Unable to fetch legislation from City Clerk RSS feed.\nLink at index {index} may be incorrect:{link}\nSkipping link...",
                e,
            )
            continue
        try:
            rss_btn.click()
            driver.switch_to.window(driver.window_handles[-1])
            url = driver.current_url
            entries = webdriver.fetch_rss_entries(url, "legislation")
            if entries[1].title == "No records":
                print(
                    f"No legislation entries found for this meeting: {link}. Skipping to next meeting..."
                )
                driver.close()
                driver.switch_to.window(driver.window_handles[-1])
                continue
            driver.close()
            driver.switch_to.window(driver.window_handles[-1])
            legislation_entries.append(entries)
        except Exception as e:
            print(
                "Error occurred. Unable to parse legislation entries from City Clerk RSS feed.",
                e,
            )
            continue
    return legislation_entries


def create_records(entries):
    """Create a list of new Member row objects for inserting to the database."""

    formatted_entries = format_entries(entries)
    records = []
    for entry in formatted_entries:
        legislation = create_legislation(entry)
        records.append(legislation)
    return records


def create_legislation(legislation: schemas.CreateLegislation):
    """Create a new Legislation ORM object."""

    db_legislation = models.Legislation(
        record_num=legislation["record_num"],
        type=legislation["type"],
        title=legislation["title"],
        result=legislation["result"],
        action_text=legislation["action_text"],
        mtg_date=legislation["mtg_date"],
    )
    return db_legislation


def format_entries(entries):
    """Accepts list of RSS entries and returns list of formatted dictionaries."""

    parsed_entries = []
    for leg_per_mtg in entries:
        mtg_title = leg_per_mtg[0]["feed_title"]
        date = get_date_from_title(mtg_title)
        leg_per_mtg.pop(0)
        print(
            f"Parsing {len(leg_per_mtg)} legislation from RSS feed for meeting date: {date}."
        )
        for leg in leg_per_mtg:
            formatted_entry = {}
            formatted_entry["mtg_date"] = date
            formatted_entry["record_num"] = leg.title.replace("-", "")
            formatted_entry["type"] = leg.tags[0].term
            other_entries = other_keys(leg.summary)
            formatted_entry.update(other_entries)
            parsed_entries.append(formatted_entry)
    parsed_entries_iterator = filter(remove_no_results, parsed_entries)
    formatted_entries = list(parsed_entries_iterator)
    print(
        f"Formatted {len(formatted_entries)} total legislation from City Clerk RSS feed."
    )
    return formatted_entries


def get_date_from_title(title):
    """Accepts a string, 'title', and splits on each hyphen to extract the meeting date."""

    match = re.search("\d{1,2}/\d{1,2}/\d{4}", title)
    return match.group()


def other_keys(summary):
    """Extracts 'title', 'result', and 'action_text' from RSS entry summary."""

    title = re.search("<br />Title:(.+?)<br />", summary)
    if title:
        title = title.group(1).strip()
    action = re.search("<br />Action:(.+?)<br />", summary)
    if action:
        action = action.group(1).strip()
    result = re.search("<br />Result:(.*)", summary)
    if result:
        result = result.group(1).strip()
    other_keys = {"title": title, "result": result, "action_text": action}
    return other_keys


def remove_no_results(entry):
    """Check if a legislation entry contains no results. If not results found, entry will be removed from the 'formatted_entries' array."""

    if entry["result"] == "":
        print(
            f"Skipping legislation record number {entry['record_num']} from {entry['mtg_date']} (no results or votes found)."
        )
        return False
    return True
