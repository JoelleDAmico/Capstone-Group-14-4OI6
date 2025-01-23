import sys, requests, httpx, urllib, json
 # Using Python 3.12 (do not try to run with 3.13 interpreter because you did
 # not install the library package for that)
 # Its possible to use it I just don't have it setup
 
from recipe_scrapers import scrape_html

# AWS Testing: 
# Want to be able to have user input a string of a url
# Take that string and put into url_dict format

url_dict = '{"link_input":"https://www.allrecipes.com/recipe/158968/spinach-and-feta-turkey-burgers/"}' 
url_dict = '{"link_input":"blank_URL"}'
#Now just need to make url_dict something that the user can input the link into (i.e. need to send over
# a format from user input that looks like this)

url_dict_s = json.loads(url_dict) #takes formatting JSON string and converts to 
url = url_dict_s.get("link_input")
name = "Capstone"
html = requests.get(url, headers={"User-Agent": f"Burger Seeker {name}"}).content #What does this line do?
scraper = scrape_html(html, org_url=url)
result = str(scraper.to_json())
result2 = str(scraper.instructions())

print(result2)