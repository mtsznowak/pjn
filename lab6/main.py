import json
import re
from collections import Counter
import pickle
import subprocess
from string import ascii_lowercase
import sys
from cases import Case
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, precision_score, f1_score, recall_score
from sklearn.pipeline import Pipeline
from nltk.corpus import stopwords
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
stop_words = set()

html_pattern = re.compile("<[^>]*>")
date_pattern = re.compile("^2012-")
digit_pattern = re.compile("\d")
html_pattern = re.compile("<[^>]*>")
interpunction_signs = "(?:\.|…|,|\(|\)|!|:|-|;|\?|„|”|[|]|\")*"
interpunction_pattern = re.compile("(?:^%s)|(?:%s$)" % (interpunction_signs, interpunction_signs))

first_index = 392
last_index = 550
# last_index = 396

if __name__ == "__main__":

  cfile = open('counter.data', 'br')
  (wordCounter, _) = pickle.load(cfile)

  print("Parsing...")

  data = []
  for index in range(first_index, last_index):
    path = ('data/json/judgments-%s.json' % index)
    items = json.load(open(path))['items']

    items = [j for j in items if date_pattern.match(j['judgmentDate']) ]
    items = filter(lambda d: d['courtType'] in ['SUPREME', 'COMMON'], items)

    for j in items:
      caseNumber = j['courtCases'][0]['caseNumber']

      case = None
      if re.match('.*\\bA?C.*', caseNumber):
        case = Case.CYWILNE
      elif re.match('.*\\bA?U.*', caseNumber):
        case = Case.UBEZPIECZENIA_SPOŁECZNE
      elif re.match('.*\\bA?K.*', caseNumber):
        case = Case.KARNE
      elif re.match('.*\\bG.*', caseNumber):
        case = Case.GOSPODARCZE
      elif re.match('.*\\bA?P.*', caseNumber):
        case = Case.PRAWO_PRACY
      elif re.match('.*\\bR.*', caseNumber):
        case = Case.PRAWO_RODZINNE
      elif re.match('.*\\bW.*', caseNumber):
        case = Case.WYKROCZENIA
      elif re.match('.*\\bAm.*', caseNumber):
        case = Case.PRAWO_KONKURENCJI

      content = j['textContent']
      content = content.replace("-\n", "")
      content = html_pattern.sub("", content)

      cindex = content.find("Uzasadnienie")
      if cindex >= 0:
        content = content[cindex + len('Uzasadnienie'):]
        splitted = re.split(' |\s|/|-|:', content)
        splitted = [interpunction_pattern.sub("", word.strip().lower()) for word in splitted]
        splitted = filter(lambda word: wordCounter[word] > 0, splitted)
        content = " ".join(splitted)
      else:
        content = None

      if case and content:
        data.append((content, case.value))

  print("Wszystkich: %s" % len(data))

  classCounter = Counter()
  X, y = map(list, zip(*data))
  classCounter.update(y)

  for k in classCounter:
    print(Case(k).name + ": " + str(classCounter[k]))

  data = filter(lambda a,b: classCounter[b] > 10, data)
  target_names = [Case(x).name for x in range(1,9)]
  target_names = filter(lambda name: classCounter[Case[name].value] > 10, target_names)
  target_names = list(target_names)


  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=10)

  stop_words = [word for word, _ in wordCounter.most_common(20)]
  pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words=stop_words)),
    ('clf', OneVsRestClassifier(LinearSVC())),
    ])


  pipeline.fit(X_train, y_train)
  predictions = pipeline.predict(X_test)

  print(classification_report(y_test, predictions, target_names=target_names))

  print("precision micro: %s\nprecision macro: %s\nrecall micro: %s\nrecall macro: %s\nf1 micro: %s\nf1 macro: %s" % (
      precision_score(y_test, predictions, average='micro'),
      precision_score(y_test, predictions, average='macro'),
      recall_score(y_test, predictions, average='micro'),
      recall_score(y_test, predictions, average='macro'),
      f1_score(y_test, predictions, average='micro'),
      f1_score(y_test, predictions, average='macro')))















