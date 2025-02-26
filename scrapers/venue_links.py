from requests_html import HTML, HTMLSession

# Start session
session = HTMLSession()
# First check Joe Rizzo open mics list, has lots of venues and links to their websites
r = session.get('http://joerizzo.com/openmics')

# Extract calendar
calendar = r.html.find('tbody', first=True)
# print(calendar.text)

# Extract venue links
cal_rows = calendar.find('tr')[1:]
for row in cal_rows:
    for link in row.absolute_links:
        if 'joerizzo' not in link:
            print(link)