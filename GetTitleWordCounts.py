import json
import os
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# define variables
articles_path = []
articleTitles = []
articleData = []
wordCount = {}
tokenTitle = []
summaryAllArticles = {}


#  a subset of all sources for the articles in the NELA2017 dataset
# sources = ["AP", "BBC", "PBS", "Salon", "Slate", "The New York Times", "BuzzFeed", "Drudge Report", "Faking News", "RedState",
#            "The Gateway Pundit", "The Huffington Post"]

# second subset sources used to determine if the results so far are dependent on the current sources being used
sources = ["CNN", "MotherJones", "NPR", "PBS", "The Hill", "Vox", "Addicting Info", "New York Daily News", "Prntly",
           "The D.C. Clothesline", "The Duran", "Yahoo News"]

#  set of commonly used words such as "the", "a", "in" etc.
englishStopWords = set(stopwords.words('english'))
stopwords = englishStopWords.union(
    {":", ";", "'", '"', '”', '“', ",", ".", "-", "_", "?", "$", "&", '...', '.', '�', '!', "''", "``", "%", "@", "--",
     ")", "(", "[", "]", "[]", "[ ]", "’", "|", "‘", " "})

#  listdir() returns a list containing the names of the entries in the directory path given
# ['1_April', '2_May', '3_June', '4_July', '5_August', '6_September', '7_October'] is returned from NELA2017
month_directories = os.listdir("C:/NELA2017/NELA2017.tar/NELA2017")


#  need an object to hold the month and date info together
class Directories:
    def __init__(self, month, date):
        self.month = month
        self.date = date


for m in month_directories:  # go through all items in month_directories and get contents
    #  date_directories in the form ['2017-10-01', '2017-10-02', '2017-10-03', '2017-10-04', '2017-10-05'.....]
    date_directories = os.listdir("C:/NELA2017/NELA2017.tar/NELA2017/" + m)
    # create a list of objects that hold both the month and date for article paths
    directoryPath = Directories(m, date_directories)
    articles_path.append(directoryPath)

#  the path to the files with the HTML is C:/NELA2017/NELA2017.tar/NELA2017/"month"/"date"/"source"/"article_title.txt"
for s in sources:
    # clear the html data for each source
    summaryAllArticles.clear()
    if not os.path.isfile("C:/Users/caire/Desktop/OutputData/OutputTitleArticles2/" + s + ".txt"):
        for p in articles_path:
            for d in p.date:
                fileFound = True
                try:
                    #  get a list of articleTitles for that source on that date in format
                    #  ['AP--2017-04-17--Absences fitness atmosphere _ new ways to track schools.txt',.....]
                    articleTitles = os.listdir("C:/NELA2017/NELA2017.tar/NELA2017/" + p.month + "/" + d + "/" + s)
                except FileNotFoundError:
                    fileFound = False

                if fileFound:  # if the source had articles on that date open all articles using articleTitles list
                    for articleTitle in articleTitles:
                        # empty lists for each iteration of the loop
                        tokenTitle.clear()
                        articleData.clear()

                        if articleTitle != "PaxHeader":
                            # open the file and specify mode (read, write, etc.)
                            # using the keyword "with automatically closes the file afterwards
                            with open("C:/NELA2017/NELA2017.tar/NELA2017/" + p.month + "/" + d + "/" + s + "/" +
                                      articleTitle, 'rb') as file:
                                try:
                                    articleData = json.load(file)

                                    # save content of the json file
                                    tokenTitle = word_tokenize(articleData['title'])

                                    # add word from the tokenized data to create a list of all words for that article
                                    for word in tokenTitle:
                                        if word not in stopwords:
                                            if word not in wordCount:
                                                wordCount[word] = 1
                                            else:
                                                wordCount[word] += 1

                                except ValueError:
                                    print("JsonDecodeError for file " + articleTitle)
                        if len(wordCount) != 0:
                            with open("C:/Users/caire/Desktop/OutputData/OutputTitleArticles2/" + s + ".txt", 'a', encoding='utf-8') as newFile:
                                newFile.write(str(Counter(wordCount)) + "\n")
                        wordCount.clear()
    print(s + "'s title words counted for each article and added to file")
