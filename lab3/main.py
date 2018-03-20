import json
import dict
import correction
import re
from collections import Counter
import sys
import pylab
import matplotlib.pyplot as plt

date_pattern = re.compile("^2012-")
digit_pattern = re.compile("\d")
html_pattern = re.compile("<[^>]*>")
interpunction_signs = "(?:\.|…|,|\(|\)|!|:|-|;|\?|„|”|[|]|\")*"
interpunction_pattern = re.compile("(?:^%s)|(?:%s$)" % (interpunction_signs, interpunction_signs))

first_index = 392
last_index = 550
# last_index = 395

if __name__ == "__main__":
  wordCounter = Counter()

  for index in range(first_index, last_index):
    path = ('data/json/judgments-%s.json' % index)
    data = json.load(open(path))['items']

    data = [j for j in data if date_pattern.match(j['judgmentDate']) ]


    for j in data:
      text = j['textContent']
      text = text.replace("-\n", "")
      text = html_pattern.sub("", text)

      splitted = re.split(' |\s|/|-', text)
      splitted = [interpunction_pattern.sub("", word.strip().lower()) for word in splitted]
      splitted = filter(lambda word: not digit_pattern.search(word) and len(word)>1, splitted)

      wordCounter.update(splitted)


  values = sorted(list((wordCounter.values())), reverse=True)
  fig = plt.figure()
  ax = fig.add_subplot(2, 1, 1)
  line, = ax.plot(values, color='blue', lw=2)
  ax.set_yscale('log')
  pylab.show()

  unknown_words = []
  print("Initializing dictionary...")
  sys.stdout.flush()
  dictionary = dict.Dict()

  print("Checking vocabulary...")
  sys.stdout.flush()
  for word in wordCounter.keys():
    if not dictionary.has_key(word):
      unknown_words.append(word)

  print(unknown_words[:30])

  print("Corrections:")

  for word in unknown_words[:30]:
    best_corr = "NONE"
    best_corr_count = -1

    corr = correction.gen_corrections(word, 1, dictionary)
    if len(corr) == 0:
      corr = correction.gen_corrections(word, 2, dictionary)

    for new_word in corr:
      if wordCounter[new_word] > best_corr_count:
        best_corr_count = wordCounter[new_word]
        best_corr = new_word

    print("%s -> %s [%s]" % (word, best_corr, best_corr_count))



