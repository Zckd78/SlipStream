from data.structs import *
import time
import requests
import bs4
from utilities import IOFunctions, DisplayFunctions

class MetaScraper():

    def __init__(self, exOptions: ExecutionOption, artists: []):
        self.Name = "MetaCritic (New Release) Scraper"
        self.CurrentUri = ""
        self.Items = {}
        self.History = []
        self.OutputLog = ""
        self.Interrupt = False
        # Options DTOs for transferring set tings between here and other classes
        self.ExecutionOptions = exOptions
        self.Artists = artists

    ## Root Function - Navigates to a page, and decides what to do from there.
    def Go(self, url: str):
        # Display and Save starting time
        startTime = "Started on: " + time.ctime() + "\n"
        self.OutputLog += startTime
        print(startTime)
        self.CurrentUri = url
        headers = {'User-Agent': 'Mozilla/5.0'}

        try:
            res = self.GetRequest(self.CurrentUri, headers)
        except Exception as excpt:
            print(excpt)

        if res is not None:
            # Take care of the Albums already on the page
            bsoupAll = self.GetSoup(res)
            self.EnumerateRecentAlbums(bsoupAll)

            # Then move on and hit the other pages to check
            pagesTotal = len(bsoupAll.select(".pages > li"))
            for page in range(1,pagesTotal):
                pageUrl = Statics.META_CRITIC_URI + Statics.META_CRITIC_PAGE_NO + str(page)
                DisplayFunctions.PrintVerbose(self.ExecutionOptions ,"Moving to page" + str(page))
                try:
                    pageRes = self.GetRequest(pageUrl, headers)
                except Exception as excpt:
                    print(excpt)
                if res is not None:
                    bsoupPage = self.GetSoup(pageRes)
                    self.EnumerateRecentAlbums(bsoupPage)
                    # Catch when we've interrupted the program with Ctrl+C
                    if self.Interrupt:
                        return
        else:
            print(" Halting Go(), unable to reach %s -> SHUTTING DOWN!" % self.Name)

        return


    # Simply returns a Beautiful Soup object
    def GetSoup(self, res):
        # Create the Beautiful Soup Object
        return bs4.BeautifulSoup(res.text, "html.parser")


    ## When given the url, returns the request.get obj
    def GetRequest(self, url, headers):
        # Go grab the page
        res = requests.get(url, headers=headers)

        # Error checking
        try:
            res.raise_for_status()
        except Exception as exc:
            print('Error in Meta Scraper: %s' % (exc))
            res = None
            return res

        return res

    """
    ------------------------ BEGIN SITE SPECIFIC CODE ------------------------
    # Code here is specific to the Site we're Parsing and Capturing
    # When creating a new Scraper, edit code here to change it's function
    --------------------------------------------------------------------------
    """

    def SerializeAlbumItem(self, bsoup: bs4.BeautifulSoup):

        albumItem = bsoup.contents[0].select(".product_title")
        dateItem = bsoup.contents[0].select(".release_date")

        dateItems = dateItem[0].text.split('\n')

        date = dateItems[2]

        titleMesh = albumItem[0].contents[0].text
        titleMesh = titleMesh.split('-')

        albumTitle = titleMesh[0].rstrip()
        artist = titleMesh[1].lstrip()

        url = Statics.META_CRITIC_HOME_URI + albumItem[1].contents[0].attrs["href"]

        matchesArtist = False
        if artist in self.Artists:
            matchesArtist = True

        albumObject = AlbumItem(url,albumTitle,artist,date, matchesArtist)

        # Store the Album we serialized
        self.Items[albumTitle] = albumObject
        self.History.append(albumObject)

        # Display the Album
        message = "Discovered [" + albumTitle + " by " + artist + "]"
        DisplayFunctions.PrintVerbose(self.ExecutionOptions, message)

        return

    def EnumerateRecentAlbums(self, bsoupAll):
        try:
            # Grabs the list items <li>
            releases = bsoupAll.select(".list_products > li")

            # Start Digging into those pastes and Serialize them
            for rel in releases:

                if rel is not None:
                    self.SerializeAlbumItem(rel)
                    # Add item to history to prevent duplicates
                    # self.History.append(title)
                else:
                    continue

            # Finally done
        except KeyboardInterrupt:
            self.Interrupt = True
            return

        return

    def PrepareStatsReport(self):
        if self.Name and len(self.History) >= 1:
            print("\n\n")
            title = "[> Statistic Report for " + self.Name + "<]"
            DisplayFunctions.PrintTitle(title.center(80,'-'))
            print("Number of Albums Scraped: "+ str(len(self.History)))
        if len(self.Items) > 0:
            DisplayFunctions.PrintTitle("Found New Albums!")
            for item in self.Items.values():
                if item.Matches:
                    message = "\n[Album] - " + item.Title + "\n[Artist] - " + item.Artist + "\n[Date Released] - " + item.Date + "\n"
                    print( message )
                    self.OutputLog += message

        else:
            print("No matching albums found... ")


