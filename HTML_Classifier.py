import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
import os, sys

#  set of commonly used words such as "the", "a", "in" etc.
englishStopWords = set(stopwords.words('english'))
characterStopWords = [":", ";", "'", '"', '”', '“', ",", ".", "-", "_", "?", "$", "&", '...', '.', '�', '!',
                      "''", "``", "%", "@", "--", ")", "(", "[", "]", "[]", "[ ]", "’", "|", "‘", " "]

#  a list of all sources for the articles in the NELA2017 dataset
sources = ["AP", "BBC", "Business Insider", "CBS News", "CNBC", "CNN", "Counter Current News",
           "Daily Buzz Live", "MotherJones", "National Review", "NPR", "PBS", "Salon", "Slate",
           "Talking Points Memo", "The Atlantic", "The Fiscal Times", "The Guardian", "The Hill",
           "The New York Times", "Vox", "Xinhua", "Activist Post", "Addicting Info", "Alternative Media Syndicate",
           "Bipartisan Report", "Breitbart", "BuzzFeed", "CNS News", "Conservative Tribune", "Daily Koz",
           "Daily Mail", "Daily Stormer", "DC Gazette", "Drudge Report", "End the Fed", "Faking News",
           "Fox News", "Freedom Daily", "Freedom Outpost", "FrontPage Magazine", "Fusion", "Hang The Bankers",
           "Infowars", "Intellihub", "Investors Business Daily", "Liberty Writers", "National Report", "Natural News",
           "New York Daily News", "New York Post", "News Busters", "Newslo", "NODISINFO", "Observer",
           "Occupy Democrats", "Palmer Report", "Prntly", "Raw Story", "Real News Right Now", "RedState",
           "RT", "Shareblue", "The Beaverton", "The Chaser", "The DC Clothesline", "The Duran",
           "The Gateway Pundit", "The Huffington Post", "The Right Scope", "The Shovel", "The Spoof",
           "TheBlaze", "ThinkProgress", "True Pundit", "TruthFeed", "USA Politics Now", "USA Today",
           "Veterans Today", "Washington Examiner", "World News Politics", "Yahoo News", "Young Conservatives"]

#  a sublist of the sources that have been deemed reliable after research
reliableSources = ["AP", "BBC", "Business Insider", "CBS News", "CNBC", "CNN", "Counter Current News",
                   "Daily Buzz Live", "MotherJones", "National Review", "NPR", "PBS", "Salon", "Slate",
                   "Talking Points Memo", "The Atlantic", "The Fiscal Times", "The Guardian", "The Hill",
                   "The New York Times", "Vox", "Xinhua"]

#  a sublist of the sources that have been deemed unreliable after research
unreliableSources = ["Activist Post", "Addicting Info", "Alternative Media Syndicate", "Bipartisan Report", "Breitbart",
                     "BuzzFeed", "CNS News", "Conservative Tribune", "Daily Koz", "Daily Mail", "Daily Stormer",
                     "DC Gazette", "Drudge Report", "End the Fed", "Faking News", "Fox News", "Freedom Daily",
                     "Freedom Outpost", "FrontPage Magazine", "Fusion", "Hang The Bankers", "Infowars", "Intellihub",
                     "Investors Business Daily", "Liberty Writers", "National Report", "Natural News",
                     "New York Daily News", "New York Post", "News Busters", "Newslo", "NODISINFO", "Observer",
                     "Occupy Democrats", "Palmer Report", "Prntly", "Raw Story", "Real News Right Now", "RedState",
                     "RT", "Shareblue", "The Beaverton", "The Chaser", "The DC Clothesline", "The Duran",
                     "The Gateway Pundit", "The Huffington Post", "The Right Scope", "The Shovel", "The Spoof",
                     "TheBlaze", "ThinkProgress", "True Pundit", "TruthFeed", "USA Politics Now", "USA Today",
                     "Veterans Today", "Washington Examiner", "World News Politics", "Yahoo News",
                     "Young Conservatives"]

reliableHTMLTags = []
unreliableHTMLTags = []

#  listdir() returns a list containing the names of the entries in the directory path given
months = os.listdir("C:/NELA2017/NELA2017.tar/NELA2017")
