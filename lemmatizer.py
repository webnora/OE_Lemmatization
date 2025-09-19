class Lemmatizer:
  path_in  = 'd/in/'
  path_out = 'd/lemmatizer/'

  def __init__(self, 
               fileStop = path_in + 'stop.txt', 
               fileDict = path_in + 'dict.tsv'):
    self.eq = 0
    self.form = {}
    with open(fileDict, 'r') as f:
      for lemma in f.read().split('\n\n'):
        for line in lemma.split('\n'):
          self.make_form(line)
            
    self.stops = []
    if fileStop:
      with open(fileStop, 'r') as f:
        self.stops = f.read().split('\n')

  def make_form(self, line):
      arr = line.split('\t')
      if len(arr) == 2:
        self.form[arr[1]] = arr[0]

  def parse(self, fileName = path_in + 'calgary/allMeters.txt'):
    with open(fileName, 'r') as f:
      self.words = [(w, self.form.get(w)) for w in f.read().split() if w not in self.stops]

  def save_debug(self, fileName = path_out + 'debug.tsv', diff = None):
    print(f'save debug to: {fileName}')
    if diff and len(diff) != len(self.words):
      print(f'wrong diff len: {len(diff)}')
    with open(fileName, 'w') as f:
      add = ""
      for i, w in enumerate(self.words):
        if w[0] == '#':
          f.write('\n')
        else:
          lemmas = w[1]
          if diff:
            lemma = diff[i][0]
            if lemma in '&' or (lemmas and lemma.lower() in lemmas.split('|')):
              add = '+'
              self.eq += 1
            else:
              add = '-'              
            add += f'\t{lemma}\t'
          f.write(f'{add}{w[0]}\t{lemmas}\n')

  def save_text(self, fileName = path_out + 'text.txt'):
    print(f'save text to: {fileName}')
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

  def stat(self, stop_len = True):
    notFound = [w for w in self.words if not w[1]]
    if stop_len:
      print('Stop words:', len(self.stops))
    all = len(self.words)
    nf = len(notFound)
    nl = len(set(notFound))
    print(f'All words: {all}')
    print(f'Forms not found: {nf} ({nf/all*100:.2f}%)')
    print(f'Lemms not found: {nl} ({nl/all*100:.2f}%)')
    if self.eq:
      print(f'Found in diff: {self.eq} ({(self.eq)/all*100:.2f}%)')

  def save_not_found(self, fileName='d/lemmatizer/not_found.txt'):
    print(f'Saving not found words to: {fileName}')
    notFound_forms = [w[0] for w in self.words if not w[1]]
    unique_notFound = sorted(list(set(notFound_forms)))
    with open(fileName, 'w') as f:
      f.write('\n'.join(unique_notFound))


if __name__ == "__main__":
  lm0 = Lemmatizer()
  lm0.parse()
  lm0.stat()
  lm0.save_debug()
  lm0.save_text()

  from lemmas import Lemmas
  lm1 = Lemmatizer('', Lemmas.file_out_norm)
  lm1.parse('d/iswoc/lemmas.txt')
  lm2 = Lemmatizer('', Lemmas.file_out_norm)
  lm2.parse('d/iswoc/forms.txt')
  lm2.save_debug(Lemmatizer.path_out + 'diff.tsv', diff = lm1.words)
  lm2.stat()
  lm2.save_not_found(f'{Lemmatizer.path_out}not_found.txt')

  # lm2 = Lemmatizer('', Lemmas.file_out_norm)
  # lm2.parse('d/iswoc/forms.txt')
  # lm2.save_debug(diff = lm1.words)
  # lm2.stat()


  # lm2 = Lemmatizer('', Lemmas.file_out_norm)
  # lm2.parse('d/iswoc/forms.txt')
  # lm2.stat()
  # lm2.save_debug('d/p_read/debug2.tsv')
  # lm2.save_text('d/p_read/text2.txt')

  # from lemmas import Lemmas
  # diff = Lemmatizer('', Lemmas.file_out_norm)
  # diff = Lemmatizer('', Lemmas.file_out_norm)
  # diff.parse('d/iswoc/lemmas.txt')

  # lm = Lemmatizer('', Lemmas.file_out_norm)
  # lm.parse('d/iswoc/forms.txt')
  # lm.save_debug(diff = diff.words)
  # lm.stat()
