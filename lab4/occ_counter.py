import json
import re
from collections import Counter
import pickle
from string import ascii_lowercase

import sys
sys.path.append('../lab3/')
import dict

date_pattern = re.compile("^2012-")
digit_pattern = re.compile("\d")
html_pattern = re.compile("<[^>]*>")
interpunction_signs = "(?:\.|…|,|\(|\)|!|:|-|;|\?|„|”|[|]|\")*"
interpunction_pattern = re.compile("(?:^%s)|(?:%s$)" % (interpunction_signs, interpunction_signs))

first_index = 392
last_index = 550
# last_index = 400

if __name__ == "__main__":
  wordCounter = Counter()
  bigramCounter = Counter()

  print("Initializing dictionary...")
  sys.stdout.flush()
  dictionary = dict.Dict()


  print("Parsing...")
  for index in range(first_index, last_index):
    path = ('../lab3/data/json/judgments-%s.json' % index)
    data = json.load(open(path))['items']

    data = [j for j in data if date_pattern.match(j['judgmentDate']) ]


    for j in data:
      text = j['textContent']
      text = text.replace("-\n", "")
      text = html_pattern.sub("", text)

      splitted = re.split(' |\s|/|-', text)
      splitted = [interpunction_pattern.sub("", word.strip().lower()) for word in splitted]
      splitted = filter(lambda word: len(word) > 1 and dictionary.has_key(word), splitted)

      splitted = list(splitted)

      wordCounter.update(splitted)
      shifted_splitted = splitted[1:]
      bigrams = list(zip(splitted, shifted_splitted))
      bigramCounter.update(bigrams)


  # dump wordCounter
  cfile = open('counter.data','wb')
  pickle.dump((wordCounter, bigramCounter), cfile)
  cfile.close()

  # print(bigramCounter)
