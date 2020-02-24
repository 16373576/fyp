import json
import os
import numpy as np


def main():
    #  a subset of all sources for the articles in the NELA2017 dataset
    sources1 = ["AP", "BBC"]#, "PBS", "Salon", "Slate", "The New York Times", "BuzzFeed", "Drudge Report", "Faking News",
               # "RedState", "The Gateway Pundit", "The Huffington Post"]

    # # second subset sources used to determine if the results so far are dependent on the current sources being used
    # sources2 = ["CNN", "MotherJones", "NPR", "PBS", "The Hill", "Vox", "Addicting Info", "New York Daily News", "Prntly",
    #            "The D.C. Clothesline", "The Duran", "Yahoo News"]

    # initialize variables
    lineDict = {}
    listForExcel = []
    listOfTags = []
    listOfDictionaryValues = []

    # get list of all tags in Nela dataset
    listOfWords = get_list_of_all_words(sources1)

    # sort the dictionaries
    sort_words(listOfWords, sources1)

    # create a numpy array to send to csv file
    listOfDictionaryValues.append(str(list(listOfTags)))
    for s in sources1:
        with open("C:/Users/caire/Desktop/OutputData/OutputTitleArticlesSorted/" + s + ".txt") as file:
            print("adding article info for " + s)
            for cnt, line in enumerate(file):
                line = line.replace("Counter(", "").replace(")", "")
                lineDict = eval(line)
                listOfDictionaryValues.append(str(list(lineDict.values())) + s)
                print(cnt)

    listForExcel = np.hstack(listOfDictionaryValues)
    np.savetxt("C:/Users/caire/Desktop/OutputData/OutputHtmlExcel/outputTitleCountForExcelArticles.csv", listForExcel,
               delimiter="\n", fmt='%s')


def get_list_of_all_words(sources1):
    listOfAllWords = []

    # get a list of all tags
    for s1 in sources1:
        with open("C:/Users/caire/Desktop/OutputData/OutputTitleArticles/" + s1 + ".txt", 'r',
                  encoding='latin1') as file:
            print(s1 + " adding words to list")
            for cnt, line in enumerate(file):
                line = line.replace("Counter(", "").replace(")", "")
                lineDict1 = eval(line)
                for word1 in lineDict1.keys():
                    if word1 not in listOfAllWords:
                        listOfAllWords.append(word1)

    return listOfAllWords


def sort_words(list_of_words, sources):
    for s in sources:
        if not os.path.isfile("C:/Users/caire/Desktop/OutputData/OutputTitleArticlesSorted/" + s + ".txt"):
            dictKey = {}
            sortedArticles = []
            print(s + " sorted")
            with open("C:/Users/caire/Desktop/OutputData/OutputTitleArticles/" + s + ".txt", 'r',
                      encoding='utf-8') as file:
                for cnt, line in enumerate(file):
                    line = line.replace("Counter(", "").replace(")", "")
                    if not line:
                        continue
                    lineDict = eval(line)

                    # update the dict of each article in source with 0 if a tag from the list of all tags isn't in dict
                    for word in list_of_words:
                        if word not in lineDict:
                            dictKey = {word: 0}
                            lineDict.update(dictKey)

                    # reorder the dictionaries to match the order of the list of all tags
                    sortedDict = {}
                    sortedDict.clear()
                    for tag in list_of_words:
                        getDictValues = {tag: lineDict[tag]}
                        sortedDict.update(getDictValues)
                    with open("C:/Users/caire/Desktop/OutputData/OutputTitleArticlesSorted/" + s + ".txt",
                              'a') as newFile:
                        newFile.write(str(sortedDict) + "\n")


main()
