import json
import re
from collections import Counter
import pickle
import subprocess
from string import ascii_lowercase
import sys

html_pattern = re.compile("<[^>]*>")

sys.path.append('../lab1/')

date_pattern = re.compile("^2012-")
digit_pattern = re.compile("\d")
html_pattern = re.compile("<[^>]*>")
interpunction_signs = "(?:\.|…|,|\(|\)|!|:|-|;|\?|„|”|[|]|\")*"
interpunction_pattern = re.compile("(?:^%s)|(?:%s$)" % (interpunction_signs, interpunction_signs))

first_index = 392
last_index = 550
# last_index = 396

if __name__ == "__main__":
  p = subprocess.Popen(['curl', '-XPOST', 'localhost:9200', '-d', '@-'],stdout=subprocess.PIPE,stdin=subprocess.PIPE)

  wordCounter = Counter()
  bigramCounter = Counter()


  print("Parsing...")
  for index in range(first_index, last_index):
    path = ('../lab1/data/json/judgments-%s.json' % index)
    data = json.load(open(path))['items']

    data = [j for j in data if date_pattern.match(j['judgmentDate']) ]

    for j in data:
      text = j['textContent']

      text = text.replace("-\n", "")
      text = html_pattern.sub("", text)

      p.stdin.write(text.encode('UTF-8'))
      p.stdin.write(b" ")


  print("Communicating")
  (stdout, stderr) = p.communicate()
  tagged_text = stdout.decode('UTF-8')

  tagged_text = tagged_text.splitlines()

  words = []

  for line in tagged_text:
    if ":" in line:
      line_splitted = line.split()
      base = line_splitted[0]
      form = line_splitted[1].split(':')[0]
      if form != "interp":
        print(base + " " + form)
        words.append(base + ":" + form)


  wordCounter.update(words)
  shifted_words = words[1:]
  bigrams = list(zip(words, shifted_words))
  bigramCounter.update(bigrams)

  print(bigramCounter.most_common(30))

  print("Saving")


  # dump wordCounter
  cfile = open('counter.data','wb')
  pickle.dump((wordCounter, bigramCounter), cfile)
  cfile.close()

  # print(bigramCounter)
