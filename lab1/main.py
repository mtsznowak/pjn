import json
import re
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from collections import Counter
import collections

zl_pattern = re.compile("\d(?:\d|(?:(?: |\.)\d\d\d))*(?:,\d\d)?(?=\s*(?:zł|PLN))")
normalize = re.compile("\.|\s")
ge_million_pattern = re.compile("\d{6}\d*(:?,\d\d)?")
date_pattern = re.compile("^2012-")
patternTitle = re.compile("Ustawa\ z\ dnia\ 23\ kwietnia\ 1964\ r.\ -\ Kodeks\ cywilny")
pattern445 = re.compile("art.\ 445")
szkoda_pattern = re.compile("(?:(?<!\w)|^)(?:S|s)zk(?:(?:oda)|(?:ody)|(?:ód)|(?:odami)|(?:odzie)|(?:odom)|(?:odę)|(?:ami)|(?:odą))(?=\W|$)")


all_zl_matches = []
ge_million = []
lt_million = []
count445 = 0
szkod = 0

def plot_histogram(data, title):
  q = list(collections.Counter((data)).items())
  q.sort(key=lambda x: -x[1])
  objects, performance = zip(*q)
  objects = objects[:100]
  performance = performance[:100]

  y_pos = np.arange(len(objects))

  plt.bar(y_pos, performance, align='center', alpha=0.5)
  plt.xticks(y_pos, objects)
  plt.ylabel('Liczba wystąpień')
  plt.title(title)

  plt.show()

if __name__ == "__main__":
  pathlist = Path('data/json').glob('**/judgments*.json')
  for path in pathlist:
    data = json.load(open(path))['items']

    data = [j for j in data if date_pattern.match(j['judgmentDate']) ]

    for j in data:

      for ref in j['referencedRegulations']:
        if pattern445.search(ref['text']) and patternTitle.search(ref['journalTitle']):
          count445 = count445 + 1
          break

      zl_matches = zl_pattern.findall(j['textContent'])
      zl_matches = [normalize.sub("", x) for x in zl_matches]
      all_zl_matches = all_zl_matches + zl_matches
      szkod = szkod + min(1, len(szkoda_pattern.findall(j['textContent'])));


  for m in all_zl_matches:
    if ge_million_pattern.match(m):
      ge_million.append(m)
    else:
      lt_million.append(m)




  print("wszystkich: %s" % (len(all_zl_matches)))
  print("powyzej 10^6: %s" % len(ge_million))
  print("ponizej 10^6: %s" % len(lt_million))
  print("ilosc 445: %s" % count445)
  print("odmian szkody: %s" % szkod)


  plot_histogram(all_zl_matches, "Wszystkie kwoty")
  plot_histogram(ge_million, "Kwoty powyżej miliona")
  plot_histogram(lt_million, "Kwoty poniżej miliona")



