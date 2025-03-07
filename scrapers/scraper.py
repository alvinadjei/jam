import os
from dotenv import load_dotenv
from google import genai
from playwright.sync_api import sync_playwright
from requests_html import HTML

# Load environment variables from .env file
load_dotenv()

# # 🔹 Access together API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)
 
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
    td_events = html.find('td')  # Events in table/calendaρ
    li_events = html.find('li')  # Events in list
    return {'li': [li.html for li in li_events], 'td': [td.html for td in td_events]}


# Function to send extracted html to Llama 3.3 for event parsing
def extract_event(component, component_type):
        
    """Sends html elements to Llama 3.3 API to extract structured event details"""
    
    prompt = f"""Extract music performance event details (artist, date, time) from the following HTML {component_type} element if it contains event info. If it doesn't contain event info, feel free to just return the string "None". Otherwise, return JSON format only:
    
    {component}

    Example output:
    {{
      "events": [
        {{
          "artist": "John Doe Trio",
          "date": "March 10, 2025",
          "time": 8:00 p.m.,
        }},
        ...
      ]
    }}
    """
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",  # 30 RPM, 1500 RPD, 1,000,000 TPM
        contents=prompt,
    )
    
    return response.text  # Extract Gemini response


def scrape_events(url):
    html = fetch_page(url)
    li_events, td_events = parse_events(html)['li'], parse_events(html)['td']

    if not li_events and not td_events:
        print("No events found on the page.")
    
    parsed_events = []
    
    # Feed <li> components to Gemini
    for event in li_events:
        parsed_event = extract_event(event, '<li>')
        if parsed_event != "None\n":
            parsed_events.append(parsed_event)
    
    # Feed <td> components to Gemini
    for event in td_events:
        parsed_event = extract_event(event, '<td>')
        if parsed_event != "None\n":
            parsed_events.append(parsed_event)

    return parsed_events

# Url with html to parse
if __name__ == "__main__":
    page = "https://www.waystonesf.com/calendar"
    events = scrape_events(page)
    for event in events:
        print(event)
