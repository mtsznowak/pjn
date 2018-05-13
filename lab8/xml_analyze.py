import xml.etree.ElementTree
import numpy as np
import matplotlib.pyplot as plt
from textwrap import wrap
from collections import Counter


def print_counter(counter, n):
  mc = counter.most_common(n)
  for v, c in mc:
    print(v + " = " + str(c))

def plot_histogram(counter, title):
  objects = list(counter.keys())
  objects = [ '\n'.join(wrap(l, 12)) for l in objects ]
  performance = list(counter.values())
  performance, objects = zip(*sorted(zip(performance, objects)))

  y_pos = np.arange(len(objects))

  plt.bar(y_pos, performance, align='center', alpha=0.5)
  plt.xticks(y_pos, objects, rotation='vertical')
  plt.ylabel('Liczba wystąpień')
  plt.title(title)

  plt.show()

if __name__ == "__main__":
  e = xml.etree.ElementTree.parse('xml_data').getroot()

  small_class_counter = Counter()
  big_class_counter = Counter()
  phrase_counter = Counter()
  most_common_in_big_class = {}


  for chunk in e.findall('chunk'):
    for sentence in chunk.findall('sentence'):
      phrases = {}

      for token in sentence.findall('tok'):
        lex = token.find('lex')
        orth = token.find('orth')
        base = lex.find('base')

        for nam in token.findall('ann'):

          if int(nam.text):
            key = nam.text + "_" + nam.attrib['chan']
            phrases[key] = (phrases.get(key, "") + " " + base.text).strip()
            # phrases[key] = (phrases.get(key, "") + " " + orth.text).strip()


      for p in phrases:
        splitted = p.split("_")

        big_class = "_".join(splitted[2:3])
        small_class = "_".join(splitted[2:])
        phrase = phrases[p]

        small_class_counter.update([small_class])
        big_class_counter.update([big_class])
        phrase_counter.update([phrase + " (" + small_class + ")"])

        c = most_common_in_big_class.get(big_class, Counter())
        c.update([phrase])
        most_common_in_big_class[big_class] = c



  plot_histogram(small_class_counter, "klasyfikacja drobnoziarnista")
  plot_histogram(big_class_counter, "klasyfikacja gruboziarnista")

  print("Najczęstsze wyrażenia:")
  print("---------------")
  print_counter(phrase_counter, 100)
  print("\n\n\n")

  print("Najczęstsze wyrażenia dla każdej z klas")
  for c in most_common_in_big_class:
    print("---------------")
    print(c + ":")
    print_counter(most_common_in_big_class[c], 10)
  print("\n\n")

