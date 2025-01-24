import sys, requests, httpx, urllib, json
 # Using Python 3.12 (do not try to run with 3.13 interpreter because you did
 # not install the library package for that)
 # Its possible to use it I just don't have it setup
 
from recipe_scrapers import scrape_html
# url = "https://www.allrecipes.com/recipe/158968/spinach-and-feta-turkey-burgers/"
# name = "Capstone"
# html = requests.get(url, headers={"User-Agent": f"Burger Seeker {name}"}).content #What does this line do?
# scraper = scrape_html(html, org_url=url)

### Example Outputs ###
#print(" ~~~~~~~~~ Example Outputs ~~~~~~~~~ ")
# print("Host: " + str(scraper.host()))

# print ("-----------------------------------")
# print("Title: " + str(scraper.title()))

# print ("-----------------------------------")
# print("Total Recipe Time: " + str(scraper.total_time()) + " minutes")

# print ("-----------------------------------")
# print("Image: " + str(scraper.image()))

# print ("-----------------------------------")
# print("Ingredients: " + str(scraper.ingredients()))

# print ("-----------------------------------")
# print("Ingredient Groups: " + str(scraper.ingredient_groups()))

# print ("-----------------------------------")
# print("Instructions: " + str(scraper.instructions()))

#print ("-----------------------------------")
#print("Instructions List: " + str(scraper.instructions_list()))


# print ("-----------------------------------")
# print("Yields: " + str(scraper.yields()))

# print ("-----------------------------------")
# print("JSON: " + str(scraper.to_json()))


# Links method is dog don't use it
#print ("-----------------------------------")
#print("Links: " + str(scraper.links()))

#exit()

#help(scraper)
#parsed = json.loads(result)
#return json.dumps(result, indent=4)


# Example of the JSON test input
'''
{
    "link_input":"https://www.allrecipes.com/recipe/158968/spinach-and-feta-turkey-burgers/"
}
'''


# Ideally this should work when a the test JSON in AWS is applied
def handler(event, context):
    # Handler function:
        # event parameter is the JSON input that is evaluated 
        # event object contains information from the invoking service
        # Evoking a function determines the structure and contents of the event
        # When an AWS service invokes the function, the service defines the event structure
    url = '{}'.format(event['link_input'])
    #takes formatting JSON string and converts to 
    #print(str(url))
    name = "Capstone"
    html = requests.get(url, headers={"User-Agent": f"Burger Seeker {name}"}).content #What does this line do?
    scraper = scrape_html(html, org_url=url)
    result = str(scraper.to_json())
    result2 = str(scraper.instructions())
    return result2