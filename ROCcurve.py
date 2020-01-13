from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
import pandas as pd
from sklearn import tree, metrics
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from matplotlib import pyplot

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

df = pd.read_csv(
    'C:/Users/caire/OneDrive/Documents/forth yr semester 1/Final Year Project/HTMLTagsIndividualArticlesNormalized.csv',
    header=0, delimiter=",")

labels = df["Reliability"]
data_before_feature_sel = df.values[:, :305]
cor = df.corr(method='pearson')
cor_target = abs(cor["Reliability"])
relevant_features = cor_target[cor_target > 0.35]
print(relevant_features)
data = df[[relevant_features.index[0], relevant_features.index[1], relevant_features.index[2],
           relevant_features.index[3], relevant_features.index[4], 'Reliability']]

data = data.sample(frac=1)
train_split = int((len(data) * 2) / 3)
training = data.values[0:train_split]
test = data.values[train_split - 1:]

# fit all models to the data and make predictions
knn = KNeighborsClassifier(n_neighbors=11)
knn.fit(training[:, :4], training[:, 5])
knn_test_predictions = knn.predict_proba(test[:, :4])

lsvm = SVC(kernel="linear", probability=True)
lsvm.fit(training[:, :4], training[:, 5])
lsvm_test_predictions = lsvm.predict_proba(test[:, :4])

clf = tree.DecisionTreeClassifier()
clf.fit(training[:, :4], training[:, 5])
clf_test_predictions = clf.predict_proba(test[:, :4])

naive = GaussianNB()
naive.fit(training[:, :4], training[:, 5])
naive_test_predictions = naive.predict_proba(test[:, :4])

# keep probabilities for the positive outcome only
knn_test_predictions = knn_test_predictions[:, 1]
lsvm_test_predictions = lsvm_test_predictions[:, 1]
clf_test_predictions = clf_test_predictions[:, 1]
naive_test_predictions = naive_test_predictions[:, 1]

# calculate ROC AUC scores
knn_auc = roc_auc_score(test[:, 5], knn_test_predictions)
lsvm_auc = roc_auc_score(test[:, 5], lsvm_test_predictions)
clf_auc = roc_auc_score(test[:, 5], clf_test_predictions)
naive_auc = roc_auc_score(test[:, 5], naive_test_predictions)

# summarize scores
print('KNN: ROC AUC=%.3f' % (knn_auc))
print('LSVM: ROC AUC=%.3f' % (lsvm_auc))
print('CART: ROC AUC=%.3f' % (clf_auc))
print('Naive: ROC AUC=%.3f' % (naive_auc))

# calculate roc curves
knn_fpr, knn_tpr, _ = roc_curve(test[:, 5], knn_test_predictions)
lsvm_fpr, lsvm_tpr, _ = roc_curve(test[:, 5], lsvm_test_predictions)
clf_fpr, clf_tpr, _ = roc_curve(test[:, 5], clf_test_predictions)
naive_fpr, naive_tpr, _ = roc_curve(test[:, 5], naive_test_predictions)

# plot the roc curve for the model
pyplot.plot(knn_fpr, knn_tpr, marker='.', label='KNN')
pyplot.plot(lsvm_fpr, lsvm_tpr, marker='.', label='LSVM')
pyplot.plot(clf_fpr, clf_tpr, marker='.', label='CART')
pyplot.plot(naive_fpr, naive_tpr, marker='.', label='Naive')

# axis labels
pyplot.title('ROC curve')
pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')
# show the legend
pyplot.legend()
pyplot.savefig('ROCcurve.png', bbox_inches='tight')
# show the plot
pyplot.show()
