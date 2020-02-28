import json
import os
from collections import Counter

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from biased_stop_words import genres, get_stop_words
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

# define variables
articles_path = []
articleTitles = []
articleData = []
wordCount = 0
tokenContent = []

# #  a subset of all sources for the articles in the NELA2017 dataset
sources = ["AP", "BBC", "PBS", "Salon", "Slate", "The New York Times", "BuzzFeed", "Drudge Report", "Faking News",
           "RedState", "The Gateway Pundit", "The Huffington Post", "CNN", "MotherJones", "NPR", "The Hill", "Vox",
           "Addicting Info", "New York Daily News", "Prntly",
           "The D.C. Clothesline", "The Duran", "Yahoo News", "Business Insider", "CNBC",  "Daily Buzz Live",
           "The Atlantic", "The Fiscal Times", "The Guardian", "Xinhua", "Activist Post", "Bipartisan Report",
           "Breitbart", "Fox News", "Intellihub", "The Spoof", "Washington Examiner"]

#  set of commonly used words such as "the", "a", "in" etc.
englishStopWords = set(stopwords.words('english'))

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
    if not os.path.isfile(
            "C:/Users/caire/Desktop/OutputData/ClassifyArticlesContentandTitle/OutputStopCountTitle/" + s + ".txt"):
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
                        tokenContent.clear()
                        articleData.clear()
                        if articleTitle != "PaxHeader":
                            # open the file and specify mode (read, write, etc.)
                            # using the keyword "with automatically closes the file afterwards
                            with open("C:/NELA2017/NELA2017.tar/NELA2017/" + p.month + "/" + d + "/" + s + "/" +
                                      articleTitle, 'rb') as file:
                                try:
                                    articleData = json.load(file)

                                    # save content of the json file
                                    tokenContent = word_tokenize(articleData['title'])

                                    # add word from the tokenized data to create a list of all words for that article
                                    for word in tokenContent:
                                        # convert all words to lower case to avoid duplicates
                                        word = word.lower()
                                        # check if the word contains a number or is a stopword
                                        if word in englishStopWords:
                                            wordCount = wordCount + 1
                                except ValueError:
                                    print("JsonDecodeError for file " + articleTitle)
                        with open(
                                "C:/Users/caire/Desktop/OutputData/ClassifyArticlesContentandTitle/OutputStopCountTitle/" + s + ".txt",
                                'a',
                                encoding='utf-8') as newFile:
                            newFile.write(str(wordCount) + "\n")
                        wordCount = 0
    print(s + "'s stop words counted for each article and added to file")

