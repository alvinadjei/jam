from playwright.sync_api import sync_playwright
from requests_html import HTML

# Function 
def fetch_page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Use headless=True to run without opening a browser
        page = browser.new_page()
        page.goto(url, timeout=60000)  # Wait up to 60 seconds for page load
        content = page.content()  # Get the full page source after JavaScript execution
        browser.close()
        return content

url = "https://riptidesf.com/index.html"
data = fetch_page(url)
html = HTML(html=data)  # This prints the rendered HTML
cal = html.find('tbody', first=True)
print(cal.html)
