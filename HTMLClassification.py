from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
import pandas as pd
from sklearn import tree
from dtreeplt import dtreeplt


def main():
    feature_names = ['/title', '/script', '/style', '/noscript', '/div', '/head', '/a', '/li', '/ul', '/nav', '/i',
                     '/span', '/h1', '/h2', '/ins', '/aside', '/section', '/label', '/form', '/header', '/p', '/strong',
                     '/b', '/h3', '/em', '/h4', '/button', '/article', '/cite', '/blockquote', '/hr', '/h5', '/footer',
                     '/body', '/html', '/iframe', '/sup', '/u', '/ol', '/sub', '/bo', '/ht', '/s', '/td', '/tr',
                     '/tbody', '/table', '/small', '/textarea', '/figcaption', '/figure', '/scri', '/xscript', '/del',
                     '/dt', '/dl', '/option', '/select', '/dir', '/time', '/center', '/fieldset', '/g', '/embed',
                     '/object', '/picture', '/video', '/q', '/h6', '/canvas', '/main', '/audio', '/code', '/big', '/th',
                     '/thead', '/pre', '/path', '/rect', '/svg', '/defs', '/symbol', '/use', '/hgroup', '/noembed',
                     '/circle', '/fb', '/scr', '/caption', '/legend', '/font', '/esi', '/img', '/map', '/link', '/opta',
                     '/DataObject', '/PageMap', '/scriptblock', '/menu', '/su', '/var', '/wp-ad', '/polygon',
                     '/ellipse', '/gcse', "/scr'+'ipt", '/dd', '/dli', '/interaction', '/headline', '/source',
                     '/teasetext', '/byline', '/date', '/input', '/filter', '/meta', '/bb-experience-select', '/bb-ad',
                     '/bb-social', '/bb-quick-links', '/bb-search-suggestions', '/address', '/br', '/summary',
                     '/details', '/SCRIPT', '/A', '/Story', '/nobr', '/P', '/NOSCRIPT', '/DIV', "/sc'+'ript", '/desc',
                     '/notag', '/clipPath', '/abbr', '/followus', '/social', '/logo', '/terms', '/acronym', '/template',
                     '/sly', '/colgroup', '/amp-ad', '/Attribute', '/mask', '/o', '/CENTER', '/IFRAME', '/exsi', '/sc',
                     '/polyline', '/progress', '/tspan', '/text', '/tfoot', '/mark', '/noframes', '/placeholder',
                     '/HTML', '/interstitial', '/ad', '/amp-img', '/fbs-accordion', '/fbs-ad', '/router-outlet',
                     '/navbar', '/channel-path', '/metrics', '/article-header', '/sharing', '/contrib-block',
                     '/sig-file', '/article-body-container', '/printbar', '/medianet', '/speed-bump', '/page',
                     '/stream', '/sidenav', '/app', '/app-root', '/LI', '/H2', '/line', '/EMBED', '/OBJECT',
                     '/ad-wx-ws', '/ad-mw-position-1', '/site-notice', '/header-user-settings', '/header-menu-mobile',
                     '/header-menu-desktop', '/search-autocomplete', '/header-search-box', '/header-user-login',
                     '/header-component', '/favorites-bar', '/favorites-more', '/favorites', '/cat-six-title',
                     '/cat-six-article-scripts', '/cat-six-disclaimer', '/cat-six-about-author',
                     '/cat-six-article-detail', '/ad-wx-mid-leader', '/ad-mw-position-3', '/cat-six-article',
                     '/cat-six-recent-articles', '/disqus', '/ad-wx-bottom-leader', '/ad-mw-position-2',
                     '/footer-component', '/cat-six-layout', '/cat-six', '/rdf', '/include', '/amp-analytics',
                     '/amp-timeago', '/amp-list', '/amp-social-share', '/amp-facebook-like', '/amp-accordion',
                     '/amp-lightbox', '/amp-install-serviceworker', '/submit', "/bo'+'dy", "/ht'+'ml", '/lh',
                     '/contentPath', '/content', '/span/', '/amp-youtube', '/H3', '/heading', '/search', '/SPAN',
                     '/xml', '/w', '/m', '/mce', '/feMergeNode', '/feMerge', '/strike', '/rc-container', '/HEAD',
                     '/TABLE', '/TD', '/TR', '/FORM', '/B', '/feFuncA', '/feComponentTransfer', '/clippath', '/h7',
                     '/pagination-nav', '/linearGradient', '/stop', '/wis-scorestrip', '/path/to/file',
                     '/path/to/ept/file', '/path/to/regional/file', '/path/to/css', '/amp-twitter', '/amp-iframe',
                     '/gpt-sizeset', '/gpt-ad', '/amp-sticky-ad', '/amp-image-lightbox', '/amp-pixel', '/amp-video',
                     '/eM', '/href', '/csg-modal', '/h9', '/h8', '/broadstreet-zone', '/red', '/post', '/amp-embed',
                     '/amp-carousel', '/BLOCKQUOTE', '/EM', '/Center', '/h4but', '/h', '/xxx', '/scr+ipt', '/wbr',
                     '/asset-code', "/'+'div", '/hp', '/tt', '/cnt', '/image', '/asset_inline', "/scri'+'pt", '/I',
                     '/ll', '/pullquote', '/scrip', '/customspan']

    # read in the data from the .csv file and shuffle
    df = pd.read_csv(
        "C:/Users/caire/Desktop/OutputData/OutputHtmlExcel/HTMLTagsNormalizedCombined.csv",
        header=0, delimiter=",")
    df = df.sample(frac=1)

    # assign the labels as the Reliability column
    labels = df["Reliability"]

    # conduct feature selection so the algorithms will run faster as now only the 5 most related attributes are used
    data = feature_selection(df)

    # initialise the algorithms and fit to the data
    knn = KNeighborsClassifier(n_neighbors=11)
    lsvm = LinearSVC()
    clf = tree.DecisionTreeClassifier()
    clf.fit(data, labels)
    naive = GaussianNB()
    naive.fit(data, labels)
    logReg = LogisticRegression()
    logReg.fit(data, labels)

    # run 10 fold cross-validation
    cross_validation_test(knn, "KNN", data, labels)
    cross_validation_test(lsvm, "LSVM", data, labels)
    cross_validation_test(clf, "CART", data, labels)
    cross_validation_test(naive, "Naive Bayes Model", data, labels)
    cross_validation_test(logReg, "logistic regression", data, labels)

    # print out the sklearn decision tree
    dtree = dtreeplt(model=clf, feature_names=feature_names, target_names=["reliable", "unreliable"])
    fig = dtree.view()
    # fig.savefig('DecisionTree.png')
    fig.savefig('ArticleDecisionTree.png')


# checks the results of the algorithms using 10-fold cross-validation and prints out the results
def cross_validation_test(algorithm, algorithm_name, data, results):
    scores = cross_val_score(algorithm, data, results, cv=10)
    print(algorithm_name + ":\n" + str(scores))
    print("Accuracy: {:0.4} (+/- {:0.3})\n".format(scores.mean(), scores.std() * 2))


# method to find the attributes with highest correlation to the class
def feature_selection(dataframe):
    cor = dataframe.corr(method='pearson')
    cor_target = abs(cor["Reliability"])
    relevant_features = cor_target[cor_target > 0.2826]
    print(relevant_features)
    data = dataframe[[relevant_features.index[0], relevant_features.index[1], relevant_features.index[2],
                      relevant_features.index[3], relevant_features.index[4]]]
    return data


main()
