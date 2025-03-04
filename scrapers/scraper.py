from playwright.sync_api import sync_playwright
from requests_html import HTML

# Url with html to parse
page = "https://www.waystonesf.com/calendar"
 
def fetch_page(url):
    """Fetch html from input url

    Args:
        url (str): URL of events page

    Returns:
        str: HTML of web page at url
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Use headless=True to run without opening a browser
        page = browser.new_page()
        page.goto(url, timeout=60000)  # Wait up to 60 seconds for page load
        content = page.content()  # Get the full page source after JavaScript execution
        browser.close()
        return content

def parse_events(content):
    html = HTML(html=content)  # This prints the rendered HTML
    return html.find('.SITE_CONTAINER')
    # events = []
    # for event in html.find('tr'):
    #     print(event.html)


def scrape_events(url):
    html = fetch_page(url)
    events = parse_events(html)
    return events

print(scrape_events(page))
