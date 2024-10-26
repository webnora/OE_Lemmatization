class Lemmatazer:
  form = {}

  def __init__(self, fileStop = 'new_stop_OE.txt', fileDict = 'dict.txt'):
    with open(fileDict, 'r') as f:
      for lemma in f.read().split('\n\n'):
        for form in lemma.split('\n'):
          arr = form.split('\t')
          if len(arr) == 2:
            self.form[arr[1]] = arr[0]
    with open(fileStop, 'r') as f:
      self.stops = f.read().split('\n')

  def parse(self, fileName = 'allMeters.txt'):
    with open(fileName, 'r') as f:
      self.words = [(w, self.form.get(w)) for w in f.read().split(' ') if w not in self.stops]

  def save(self, fileName = 'out.txt'):
    with open(fileName, 'w') as f:
      for w in self.words:
        if w[0] == '#':
          f.write('\n')
        else:
          f.write(f'{w[0]} -> {w[1]}\n')

  def save_text(self, fileName = 'out_text.txt'):
    def get_lemma(w):
      if w[0] == '#':
        return '\n'
      return w[1] or w[0]
    
    with open(fileName, 'w') as f:
      arr = [get_lemma(w) for w in self.words]
      f.write(' '.join(arr))

  def print_words(self, limit = 30):
    for w in self.words[:limit]:
      print(w)

  def print_statistics(self):
    notFound = [w for w in self.words if not w[1]]
    print('All words:', len(self.words))
    print('Forms not found:', len(notFound))
    print('Lemms not found:', len(set(notFound)))


if __name__ == "__main__":
    # lm = Lemmatazer(fileStop = 'empty.txt')
    # lm.parse()
    # lm.print_statistics()

    lm = Lemmatazer()
    lm.parse()
    lm.print_statistics()
    # lm.save_text()
