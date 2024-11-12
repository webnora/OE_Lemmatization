class Lemmatazer:
  path_in  = 'd/in/'
  path_out = 'd/lemmatazer/'

  def __init__(self, 
               fileStop = path_in + 'stop.txt', 
               fileDict = path_in + 'dict.tsv'):
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
      self.words = [(w, self.form.get(w)) for w in f.read().split(' ') if w not in self.stops]

  def save_debug(self, fileName = path_out + 'debug.txt'):
    with open(fileName, 'w') as f:
      for w in self.words:
        if w[0] == '#':
          f.write('\n')
        else:
          f.write(f'{w[0]} -> {w[1]}\n')

  def save_text(self, fileName = path_out + 'text.txt'):
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


if __name__ == "__main__":
  # lm = Lemmatazer(fileStop = "")
  # lm.parse()
  # lm.stat()

  # print()
  # lm = Lemmatazer()
  # lm.parse()
  # lm.stat()
  # # lm.save_debug()
  # # lm.save_text()

  from lemmas import Lemmas
  lm2 = Lemmatazer('', Lemmas.file_out_norm)
  lm2.parse('d/iswoc/forms.txt')
  lm2.stat()
  lm2.save_debug('d/p_read/debug2.txt')
  lm2.save_text('d/p_read/text2.txt')

