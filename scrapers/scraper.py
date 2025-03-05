import os
from dotenv import load_dotenv
from together import Together
from playwright.sync_api import sync_playwright
from requests_html import HTML

# 🔹 Access together API
load_dotenv()  # Load environment variables from .env file
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")  # Read API key from environment variable
client = Together(api_key=TOGETHER_API_KEY)  # Initialize client
 
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
    return html.find('ul')[2].html
    # return [ul.html for ul in html.find('ul')]


# Function to send extracted <ul> to Llama 3.3 for event parsing
def extract_event_info(ul_elements):
    """Sends <ul> elements to Llama 3.3 API to extract structured event details"""
    
    prompt = f"""Extract event details (name, artist, date, description) from the following HTML list elements. Return JSON format only:
    
    {ul_elements}

    Example output:
    {{
      "events": [
        {{
          "event_name": "Jazz Night at The Club",
          "artist": "John Doe Trio",
          "date": "March 10, 2025",
          "description": "A live jazz performance in downtown SF."
        }},
        ...
      ]
    }}
    """
    
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=None,
        temperature=0.0,  # Keep deterministic output
        top_p=0.7,
        top_k=50,
        repetition_penalty=1,
        stop=["<|eot_id|>", "<|eom_id|>"],
        stream=False  # Set to True if you want streaming output
    )

    return response.choices[0].message.content  # Extract Llama response


def scrape_events(url):
    html = fetch_page(url)
    ul_elements = parse_events(html)
    
    if not ul_elements:
        print("No <ul> elements found on the page.")
        return None

    extracted_data = extract_event_info(ul_elements)
    return extracted_data

# Url with html to parse
page = "https://www.waystonesf.com/calendar"
event_data = scrape_events(page)
print(event_data)
