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
               "Infowars", "Intellihub", "Investors Business Daily", "Liberty Writers", "National Report",
               "Natural News",
               "New York Daily News", "New York Post", "NewsBusters", "Newslo", "NODISINFO", "Observer",
               "Occupy Democrats", "Palmer Report", "Prntly", "Raw Story", "Real News Right Now", "RedState",
               "RT", "Shareblue", "The Beaverton", "The Chaser", "The D.C. Clothesline", "The Duran",
               "The Gateway Pundit", "The Huffington Post", "The Right Scoop", "The Shovel", "The Spoof",
               "TheBlaze", "ThinkProgress", "True Pundit", "TruthFeed", "USA Politics Now", "USA Today",
               "Veterans Today", "Washington Examiner", "World News Politics", "Yahoo News"]

    # initialize variables
    summary = {}
    listForExcel = []
    listOfTags = []
    listOfDictionaryValues = []

    # get list of all tags in Nela dataset
    listOfTags = get_list_of_all_tags()

    # sort the dictionaries
    sort_tags(listOfTags, sources)

    # create a numpy array to send to csv file
    listOfDictionaryValues.append(str(list(listOfTags)))
    for s in sources:
        with open("C:/Users/caire/Desktop/OutputData/OutputHtml/" + s + ".txt") as file:
            summary = json.load(file)
        listOfDictionaryValues.append(str(list(summary.values())) + s)
    listForExcel = np.hstack(listOfDictionaryValues)
    np.savetxt("C:/Users/caire/Desktop/OutputData/OutputHtmlExcel/outputTagCountForExcel.csv", listForExcel,
               delimiter="\n", fmt='%s')


def sort_tags(list_of_tags, sources):
    for s in sources:
        dictKey = {}
        with open("C:/Users/caire/Desktop/OutputData/OutputHtml/" + s + ".txt") as file:
            summary = json.load(file)

        # update the dictionaries of each source with zeroes if a tags from the list of all tags is not in the dict
        for tag in list_of_tags:
            if tag not in summary:
                dictKey = {tag: 0}
                summary.update(dictKey)

        # reorder the dictionaries to match the order of the list of all tags
        sortedDict = {}
        for tag in list_of_tags:
            getDictValues = {tag: summary[tag]}
            sortedDict.update(getDictValues)

        # update the .txt files with new sorted that now have all tags dictionaries
        with open("C:/Users/caire/Desktop/OutputData/OutputHtml/" + s + ".txt", 'w') as newFile:
            json.dump(sortedDict, newFile)


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
    print(
        "There are %d reliable tags that never occur in unreliable source articles" % len(reliableTags_notInUnreliable))
    print("Number of times each reliable tag that is not present in unreliableTags occurs " + str(
        numberOfReliableNotInUnreliable))

    # keep track of unreliable tags that are never used in reliable source articles
    for key in unreliableTags.keys():
        if key not in reliableTags:
            unreliableTags_notInReliable.append(key)
            numberOfUnreliableNotInReliable.append(key + " " + str(unreliableTags[key]))

    print("\nUnreliableTags not present in reliable Tags list are: " + str(unreliableTags_notInReliable))
    print(
        "There are %d unreliable tags that never occur in reliable source articles" % len(unreliableTags_notInReliable))
    print("Number of times each reliable tag that is not present in unreliableTags occurs " + str(
        numberOfUnreliableNotInReliable))

    return listOfAllTags


main()
