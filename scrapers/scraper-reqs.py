import csv
from requests_html import HTML, HTMLSession

# # Start session1
# session = HTMLSession()
# # First check Joe Rizzo open mics list, has lots of venues and links to their websites
# r1 = session.get('http://joerizzo.com/openmics')

# # Extract calendar
# calendar = r1.html.find('tbody', first=True)
# # print(calendar.text)

# # Extract venue links and save to links array
# cal_rows = calendar.find('tr')[1:]
# links = []
# for row in cal_rows:
#     for link in row.absolute_links:
#         if 'joerizzo' not in link:
#             links.append(link)


# # Start session2
link_test = "https://riptidesf.com/index.html"
session = HTMLSession()  # remove later
r2 = session.get(link_test)
html = r2.html
html.render()

calendar = html.find('body', first=True)
print(calendar.html)