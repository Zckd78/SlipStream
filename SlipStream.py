from scraper.MetaScraper import *
from data.structs import *
from utilities import IOFunctions, LibraryImport

# Function to start all the main work.
def Main(args, artists: []):
    GatherNewReleases(args, artists)

# Does all the work.
def GatherNewReleases(params, artists: []):
    # Set the Execution Options
    options = ExecutionOption()
    # These will be parameters when the program is live, setting here for testing.
    options.DetermineMode(params)
    options.DetermineVerbose(params)

    # Go find those new Albums!
    scrap = MetaScraper(options, artists)
    try:
        scrap.Go(Statics.META_CRITIC_URI)
    except KeyboardInterrupt:
        print("!!! --- {CTRL-C Pressed, Cleaning up...} --- !!!")

    # Print out results here
    scrap.PrepareStatsReport()

    # Save the Output to Log file
    IOFunctions.SaveLog(scrap.OutputLog)

    print("\n\rFinished!")

# Wrapper method to call LibraryImport
def ImportArtistsXML():
    return LibraryImport.Import()


# Fill this out with Artists to look out for
artistsList = [
    "AFI",
    "The 1975",
    "Capital Cities",
    "Queens of the Stone Age",
    "Com Truise",
    "Explosions in the Sky",
    "ODESZA",
    "HelloGoodBye",
    ""
]

# Add all the Artists in the provided iTunes Library Export file
artistsList.extend(ImportArtistsXML())

# Light the coals in this crazy train.
Main("", artistsList)
