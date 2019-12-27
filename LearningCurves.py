from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import LinearSVC
import pandas as pd
from sklearn import tree, metrics

feature_names = ['/title', '/script', '/style', '/noscript', '/div', '/head', '/a', '/li', '/ul', '/nav', '/i', '/span',
                 '/h1', '/h2', '/ins', '/aside', '/section', '/label', '/form', '/header', '/p', '/strong', '/b', '/h3',
                 '/em', '/h4', '/button', '/article', '/cite', '/blockquote', '/hr', '/h5', '/footer', '/body', '/html',
                 '/iframe', '/sup', '/u', '/ol', '/sub', '/bo', '/ht', '/s', '/td', '/tr', '/tbody', '/table', '/small',
                 '/textarea', '/figcaption', '/figure', '/scri', '/xscript', '/del', '/dt', '/dl', '/option', '/select',
                 '/dir', '/time', '/center', '/fieldset', '/g', '/embed', '/object', '/picture', '/video', '/q', '/h6',
                 '/canvas', '/main', '/audio', '/code', '/big', '/th', '/thead', '/pre', '/path', '/rect', '/svg',
                 '/defs', '/symbol', '/use', '/hgroup', '/noembed', '/circle', '/fb', '/scr', '/caption', '/legend',
                 '/font', '/esi', '/img', '/map', '/link', '/opta', '/DataObject', '/PageMap', '/scriptblock', '/menu',
                 '/su', '/var', '/wp-ad', '/polygon', '/ellipse', '/gcse', "/scr'+'ipt", '/dd', '/dli', '/interaction',
                 '/headline', '/source', '/teasetext', '/byline', '/date', '/input', '/filter', '/meta',
                 '/bb-experience-select', '/bb-ad', '/bb-social', '/bb-quick-links', '/bb-search-suggestions',
                 '/address', '/br', '/summary', '/details', '/SCRIPT', '/A', '/Story', '/nobr', '/P', '/NOSCRIPT',
                 '/DIV', "/sc'+'ript", '/desc', '/notag', '/clipPath', '/abbr', '/followus', '/social', '/logo',
                 '/terms', '/acronym', '/template', '/sly', '/colgroup', '/amp-ad', '/Attribute', '/mask', '/o',
                 '/CENTER', '/IFRAME', '/exsi', '/sc', '/polyline', '/progress', '/tspan', '/text', '/tfoot', '/mark',
                 '/noframes', '/placeholder', '/HTML', '/interstitial', '/ad', '/amp-img', '/fbs-accordion', '/fbs-ad',
                 '/router-outlet', '/navbar', '/channel-path', '/metrics', '/article-header', '/sharing',
                 '/contrib-block', '/sig-file', '/article-body-container', '/printbar', '/medianet', '/speed-bump',
                 '/page', '/stream', '/sidenav', '/app', '/app-root', '/LI', '/H2', '/line', '/EMBED', '/OBJECT',
                 '/ad-wx-ws', '/ad-mw-position-1', '/site-notice', '/header-user-settings', '/header-menu-mobile',
                 '/header-menu-desktop', '/search-autocomplete', '/header-search-box', '/header-user-login',
                 '/header-component', '/favorites-bar', '/favorites-more', '/favorites', '/cat-six-title',
                 '/cat-six-article-scripts', '/cat-six-disclaimer', '/cat-six-about-author', '/cat-six-article-detail',
                 '/ad-wx-mid-leader', '/ad-mw-position-3', '/cat-six-article', '/cat-six-recent-articles', '/disqus',
                 '/ad-wx-bottom-leader', '/ad-mw-position-2', '/footer-component', '/cat-six-layout', '/cat-six',
                 '/rdf', '/include', '/amp-analytics', '/amp-timeago', '/amp-list', '/amp-social-share',
                 '/amp-facebook-like', '/amp-accordion', '/amp-lightbox', '/amp-install-serviceworker', '/submit',
                 "/bo'+'dy", "/ht'+'ml", '/lh', '/contentPath', '/content', '/span/', '/amp-youtube', '/H3', '/heading',
                 '/search', '/SPAN', '/xml', '/w', '/m', '/mce', '/feMergeNode', '/feMerge', '/strike', '/rc-container',
                 '/HEAD', '/TABLE', '/TD', '/TR', '/FORM', '/B', '/feFuncA', '/feComponentTransfer', '/clippath', '/h7',
                 '/pagination-nav', '/linearGradient', '/stop', '/wis-scorestrip', '/path/to/file', '/path/to/ept/file',
                 '/path/to/regional/file', '/path/to/css', '/amp-twitter', '/amp-iframe', '/gpt-sizeset', '/gpt-ad',
                 '/amp-sticky-ad', '/amp-image-lightbox', '/amp-pixel', '/amp-video', '/eM', '/href', '/csg-modal',
                 '/h9', '/h8', '/broadstreet-zone', '/red', '/post', '/amp-embed', '/amp-carousel', '/BLOCKQUOTE',
                 '/EM', '/Center', '/h4but', '/h', '/xxx', '/scr+ipt', '/wbr', '/asset-code', "/'+'div", '/hp', '/tt',
                 '/cnt', '/image', '/asset_inline', "/scri'+'pt", '/I', '/ll', '/pullquote', '/scrip', '/customspan']

df = pd.read_csv('C:/Users/caire/OneDrive/Documents/forth yr semester 1/Final Year Project/HTMLTagsFrequency.csv',
                 header=0, delimiter=",")
df = df.sample(frac=1)
train_split = int((len(df) * 2) / 3)
training = df.values[0:train_split]
test = df.values[train_split - 1:]

lsvm_learningCurve_accuracy = []
knn_learningCurve_accuracy = []
clf_learningCurve_accuracy = []
naive_learningCurve_accuracy = []
# get data for learning curves and save to file to be used in excel
for instances in range(11, len(training), 2):
    knn = KNeighborsClassifier(n_neighbors=11)
    knn.fit(training[0:instances, :305], training[0:instances, 307])
    knn_test_predictions = knn.predict(test[:, :305])
    knn_learningCurve_accuracy.append((metrics.accuracy_score(test[:, -1], knn_test_predictions)) * 100)

    lsvm = LinearSVC()
    lsvm.fit(training[0:instances, :305], training[0:instances, 307])
    lsvm_test_predictions = lsvm.predict(test[:, :305])
    lsvm_learningCurve_accuracy.append((metrics.accuracy_score(test[:, -1], lsvm_test_predictions)) * 100)

    clf = tree.DecisionTreeClassifier()
    clf.fit(training[0:instances, :305], training[0:instances, 307])
    clf_test_predictions = clf.predict(test[:, :305])
    clf_learningCurve_accuracy.append((metrics.accuracy_score(test[:, -1], clf_test_predictions)) * 100)

    naive = GaussianNB()
    naive.fit(training[0:instances, :305], training[0:instances, 307])
    naive_test_predictions = naive.predict(test[:, :305])
    naive_learningCurve_accuracy.append((metrics.accuracy_score(test[:, -1], naive_test_predictions)) * 100)

print(lsvm_learningCurve_accuracy)
print(knn_learningCurve_accuracy)
print(clf_learningCurve_accuracy)
print(naive_learningCurve_accuracy)
newFile = open("C:/Users/caire/PycharmProjects/fyp/LearningCurve.csv", 'a+')
newFile.write(str(lsvm_learningCurve_accuracy))
newFile.write(str(knn_learningCurve_accuracy))
newFile.write(str(clf_learningCurve_accuracy))
newFile.write(str(naive_learningCurve_accuracy))
newFile.close()

print("KNN")
print(confusion_matrix(test[:, -1], knn_test_predictions))
print(classification_report(test[:, -1], knn_test_predictions))

print("LSVM")
print(confusion_matrix(test[:, -1], lsvm_test_predictions))
print(classification_report(test[:, -1], lsvm_test_predictions))

print("CART")
print(confusion_matrix(test[:, -1], clf_test_predictions))
print(classification_report(test[:, -1], clf_test_predictions))

print("Naive")
print(confusion_matrix(test[:, -1], naive_test_predictions))
print(classification_report(test[:, -1], naive_test_predictions))

