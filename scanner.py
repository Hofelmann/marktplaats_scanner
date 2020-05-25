from time import sleep
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import webbrowser


class Scanner:
    """
    urls - Marktplaats urls to search through.
    ignore - keywords to ignore
    prev - previously found usernames
    """
    def __init__(self, urls, ignore):
        self.urls = urls
        self.ignore = ignore
        self.prev = []

    """
    Main loop that scans each given url for the wanted adverts. When one is found, it is opened in the webbrowser.

    initial - run an initial scan that won't alert you to the adverts at 
              the time of starting the scanner.
    """
    def loop(self, initial):
        for url in self.urls:
            print("Checking {}".format(url))
            # Read requested url and retrieve all user listings
            uClient = uReq(url)
            html = uClient.read()
            uClient.close()
            html_soup = soup(html, "html.parser")
            advs = html_soup.findAll("li", {"mp-Listing mp-Listing--list-item"})

            for advert in advs:
                # Remove all unwanted advertisements
                if any(i in advert.find("h3", {"mp-Listing-title"}).text.strip() for i in self.ignore):
                    continue

                # Remove adverts from previously found users
                poster = advert.find("span", {"mp-Listing-seller-name"}).text.strip()
                if poster in prev:
                    print("advert found earlier")
                    continue

                # New user, adding it to found list and opening advert
                self.prev.append(poster)
                
                # Continue if this is the first run
                if initial:
                    continue

                link = advert.find("a", {"mp-Listing-coverLink"}).get("href")
                webbrowser.open("https://www.marktplaats.nl/" + link)


    """
    Runs while ctrl+c is not pressed, sleeping between each scan.

    initial - run an initial scan that won't alert you to the adverts at 
              the time of starting the scanner. Highly recommended to leave as True.
    time - time to sleep between scans.
    """
    def run(self, initial=True, time=15):
        print("Starting scanner...")
        try:
            while True:
                self.loop(initial)
                sleep(time)
                print("\nRefreshing pages...\n")
        except KeyboardInterrupt:
            print("\nAre you sure you want to stop the scanner? (y/n)")
            while True:
                user_input = input()
                if user_input == "y":
                    exit(0)
                elif user_input == "n":
                    print("Resuming the scanner...")
                    self.run(False, time)
                else:
                    print("Please answer n for no and y for yes.")


# Search urls to scrape
urls = ["https://www.marktplaats.nl/l/dieren-en-toebehoren/katten-en-kittens-raskatten-langhaar/#offeredSince:Vandaag",
        "https://www.marktplaats.nl/l/dieren-en-toebehoren/katten-en-kittens-raskatten-korthaar/#offeredSince:Vandaag",
        "https://www.marktplaats.nl/l/dieren-en-toebehoren/katten-en-kittens-overige-katten/#offeredSince:Vandaag"]
# Previously found usernames
prev = []
# Strings to ignore in listing titles
ignore = ["dekkater", "gezocht", "GEZOCHT", "Gezocht", "dek kater", "Dekkater", "Dek kater", "bengaal", "Bengaal", "perzische", "Perzische", "Naaktkat", "naaktkat", "Naakt kat", "naakt kat", "Sphinx", "spinx", "Sphynx", "sphynx"]

s = Scanner(urls, ignore)
s.run(False)
