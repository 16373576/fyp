import numpy as np


def main():
    #  a subset of all sources for the articles in the NELA2017 dataset
    sources = ["AP", "BBC", "PBS", "Salon", "Slate", "The New York Times", "BuzzFeed", "Drudge Report", "Faking News",
                "RedState", "The Gateway Pundit", "The Huffington Post", "CNN", "MotherJones", "NPR", "The Hill", "Vox",
               "Addicting Info", "New York Daily News", "Prntly", "The D.C. Clothesline", "The Duran", "Yahoo News",
               "Business Insider", "CNBC",  "Daily Buzz Live", "The Atlantic", "The Fiscal Times", "The Guardian",
               "Xinhua", "Activist Post", "Bipartisan Report", "Breitbart", "Fox News", "Intellihub", "The Spoof",
               "Washington Examiner"]

    listOfArticleNames = getArticleName(sources)

    listOfArticleURL = getArticleURL(sources)

    listForClassification = []
    for i in range(len(listOfArticleNames)):
        articleName = listOfArticleNames[i]
        articleURL = listOfArticleURL[i]
        content = articleName + "," + articleURL
        listForClassification.append(content)
    listForExcel = np.hstack(listForClassification)
    np.savetxt("C:/Users/caire/Desktop/OutputData/OutputHtmlExcel/outputArticleNames.csv", listForExcel,
               delimiter="\n", fmt='%s')


def getArticleName(sources):
    listOfArticleNames = []
    for s in sources:
        with open(
                "C:/Users/caire/Desktop/OutputData/ClassifyArticlesTags/articleNames/" + s + ".txt") as file:
            print("adding article title for " + s)
            for cnt, line in enumerate(file):
                line = line.replace("\n", "")
                listOfArticleNames.append(line)
    return listOfArticleNames


def getArticleURL(sources):
    listOfArticleURL = []
    for s in sources:
        with open(
                "C:/Users/caire/Desktop/OutputData/ClassifyArticlesTags/articleURL/" + s + ".txt") as file:
            print("adding article url for " + s)
            for cnt, line in enumerate(file):
                line = line.replace("\n", "")
                listOfArticleURL.append(line)
    return listOfArticleURL


main()
