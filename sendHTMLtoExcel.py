import json

import numpy as np
import pandas as pd

def main():
    #  a list of all sources for the articles in the NELA2017 dataset
    sources = ["AP", "BBC", "Business Insider", "CBS News", "CNBC", "CNN", "Counter Current News",
               "Daily Buzz Live", "MotherJones", "National Review", "NPR", "PBS", "Salon", "Slate",
               "Talking Points Memo", "The Atlantic", "The Fiscal Times", "The Guardian", "The Hill",
               "The New York Times", "Vox", "Xinhua", "Activist Post", "Addicting Info", "Alternative Media Syndicate",
               "Bipartisan Report", "Breitbart", "BuzzFeed", "Conservative Tribune", "Daily Kos",
               "Daily Mail", "Daily Stormer", "DC Gazette", "Drudge Report", "End the Fed", "Faking News",
               "Fox News", "Freedom Daily", "Freedom Outpost", "FrontPage Magazine", "Fusion", "Hang The Bankers",
               "Infowars", "Intellihub", "Investors Business Daily", "Liberty Writers", "National Report", "Natural News",
               "New York Daily News", "New York Post", "News Busters", "Newslo", "NODISINFO", "Observer",
               "Occupy Democrats", "Palmer Report", "Prntly", "Raw Story", "Real News Right Now", "RedState",
               "RT", "Shareblue", "The Beaverton", "The Chaser", "The DC Clothesline", "The Duran",
               "The Gateway Pundit", "The Huffington Post", "The Right Scope", "The Shovel", "The Spoof",
               "TheBlaze", "ThinkProgress", "True Pundit", "TruthFeed", "USA Politics Now", "USA Today",
               "Veterans Today", "Washington Examiner", "World News Politics", "Yahoo News", "reliableTags", "unreliableTags"]

    #  a sublist of the sources that have been deemed reliable after research
    reliableSources = ["AP", "BBC", "Business Insider", "CBS News", "CNBC", "CNN", "Counter Current News",
                       "Daily Buzz Live", "MotherJones", "National Review", "NPR", "PBS", "Salon", "Slate",
                       "Talking Points Memo", "The Atlantic", "The Fiscal Times", "The Guardian", "The Hill",
                       "The New York Times", "Vox", "Xinhua"]

    #  a sublist of the sources that have been deemed unreliable after research
    unreliableSources = ["Activist Post", "Addicting Info", "Alternative Media Syndicate", "Bipartisan Report", "Breitbart",
                         "BuzzFeed", "Conservative Tribune", "Daily Kos", "Daily Mail", "Daily Stormer",
                         "DC Gazette", "Drudge Report", "End the Fed", "Faking News", "Fox News", "Freedom Daily",
                         "Freedom Outpost", "FrontPage Magazine", "Fusion", "Hang The Bankers", "Infowars", "Intellihub",
                         "Investors Business Daily", "Liberty Writers", "National Report", "Natural News",
                         "New York Daily News", "New York Post", "News Busters", "Newslo", "NODISINFO", "Observer",
                         "Occupy Democrats", "Palmer Report", "Prntly", "Raw Story", "Real News Right Now", "RedState",
                         "RT", "Shareblue", "The Beaverton", "The Chaser", "The DC Clothesline", "The Duran",
                         "The Gateway Pundit", "The Huffington Post", "The Right Scope", "The Shovel", "The Spoof",
                         "TheBlaze", "ThinkProgress", "True Pundit", "TruthFeed", "USA Politics Now", "USA Today",
                         "Veterans Today", "Washington Examiner", "World News Politics", "Yahoo News"]

    summary = {}
    listForExcel = []

    # read in HTMLDictionaries from all sources and create a csv file to be used in excel
    # for s in sources:
    #     with open("C:/Users/caire/Desktop/OutputData/OutputHtml/" + s + ".txt") as file:
    #         summary = json.load(file)
    #     listForExcel = np.column_stack((str(list(summary.keys())), str(list(summary.values()))))
    #     print(listForExcel)
    #     np.savetxt("C:/Users/caire/Desktop/OutputData/OutputHtmlExcel/" + s + ".csv", listForExcel, delimiter="\n", fmt='%s')

    # for s in sources:
    #     with open("C:/Users/caire/Desktop/OutputData/OutputHtml/" + s + ".txt") as file:
    #         summary = json.load(file)


def get_list_of_all_tags():
    listOfAllTags = []
    reliableTags_notInUnreliable = []
    unreliableTags_notInReliable = []
    numberOfReliableNotInUnreliable = []
    numberOfUnreliableNotInReliable = []

    # get a list of all tags
    with open("C:/Users/caire/Desktop/OutputData/OutputHtml/" + "unreliableTags" + ".txt") as file:
        unreliableTags = json.load(file)
    with open("C:/Users/caire/Desktop/OutputData/OutputHtml/" + "reliableTags" + ".txt") as file:
        reliableTags = json.load(file)
    # add all unreliable tags to the list
    for unreliableKey in unreliableTags.keys():
        listOfAllTags.append(unreliableKey)

    # add any reliable tags that weren't in unreliable to the list also
    for reliableKey in reliableTags.keys():
        if reliableKey not in unreliableTags:
            listOfAllTags.append(reliableKey)
            # keep track of reliable tags that are never used in unreliable source articles
            reliableTags_notInUnreliable.append(reliableKey)
            numberOfReliableNotInUnreliable.append(reliableKey + " " + str(reliableTags[reliableKey]))

    print("List of all tags in reliable and unreliable: " + str(listOfAllTags))
    print("There are %d types of tags in total that occur in the Nela dataset " % len(listOfAllTags))

    print("\nReliableTags not present in unreliable Tags list are: " + str(reliableTags_notInUnreliable))
    print("There are %d reliable tags that never occur in unreliable source articles" % len(reliableTags_notInUnreliable))
    print("Number of times each reliable tag that is not present in unreliableTags occurs " + str(numberOfReliableNotInUnreliable))

    # keep track of unreliable tags that are never used in reliable source articles
    for key in unreliableTags.keys():
        if key not in reliableTags:
            unreliableTags_notInReliable.append(key)
            numberOfUnreliableNotInReliable.append(key + " " + str(unreliableTags[key]))

    print("\nUnreliableTags not present in reliable Tags list are: " + str(unreliableTags_notInReliable))
    print("There are %d unreliable tags that never occur in reliable source articles" % len(unreliableTags_notInReliable))
    print("Number of times each reliable tag that is not present in unreliableTags occurs " + str(numberOfUnreliableNotInReliable))

    return listOfAllTags


main()
