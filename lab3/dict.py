class Dict:
  def __init__(self):
    filepath = 'polimorfologik-2.1/polimorfologik-2.1.txt'
    self.dict = set()

    with open(filepath) as fp:
      line = fp.readline()
      while line:
        splitted = line.split(';')
        self.dict.add(splitted[1].lower())
        line = fp.readline()

  def has_key(self, word):
    return word in self.dict

