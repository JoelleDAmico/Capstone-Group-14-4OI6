import requests, httpx, urllib

from recipe_scrapers import scrape_html
url = "https://www.allrecipes.com/recipe/158968/spinach-and-feta-turkey-burgers/"
name = "Capstone"
html = requests.get(url, headers={"User-Agent": f"Burger Seeker {name}"}).content #What does this line do?
scraper = scrape_html(html, org_url=url)

### Example Outputs ###
print(" ~~~~~~~~~ Example Outputs ~~~~~~~~~ ")
print("Ingredients: " + str(scraper.ingredients()))

print ("-----------------------------------")
print("Instructions: " + scraper.instructions())

print ("-----------------------------------")
print("Total Recipe Time: " + str(scraper.total_time()) + " minutes")

#help(scraper)
