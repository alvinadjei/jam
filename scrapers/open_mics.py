from flask import Flask, jsonify
import threading
import time
from requests_html import HTMLSession
from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = "https://your-project-url.supabase.co"
SUPABASE_KEY = "your-anon-key"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)
session = HTMLSession()

def scrape_data():
    while True:
        try:
            url = "http://joerizzo.com/openmics"
            response = session.get(url)
            response.html.render()  # Render JavaScript content if needed

            # Example extraction
            data = {
                "name": response.html.find("h1", first=True).text if response.html.find("h1", first=True) else "N/A",
                "price": response.html.find(".price", first=True).text if response.html.find(".price", first=True) else "N/A",
                "description": response.html.find(".description", first=True).text if response.html.find(".description", first=True) else "N/A",
            }

            # Insert data into Supabase
            supabase.table("products").insert(data).execute()
            print("Data inserted:", data)

        except Exception as e:
            print("Error scraping data:", e)

        time.sleep(300)  # Refresh every 5 minutes

scraper_thread = threading.Thread(target=scrape_data, daemon=True)
scraper_thread.start()

@app.route("/product")
def get_product():
    # Fetch the latest product from Supabase
    response = supabase.table("products").select("*").order("updated_at", desc=True).limit(1).execute()
    return jsonify(response.data[0] if response.data else {})

if __name__ == "__main__":
    app.run(debug=True)
