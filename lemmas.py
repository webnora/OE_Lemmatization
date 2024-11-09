class Lemmas:
  file_in  = 'd/unimorph/dict.tsv'
  file_out = 'd/lemmas/dict.tsv'            # merged all source
  file_out_norm = 'd/lemmas/dict_norm.tsv'  # merged all source & normalize
  file_unknown = 'd/in/dict.tsv'
  file_unimorph_norm = 'd/lemmas/unimorph_norm.tsv'

  def __init__(self, file = file_in, lemmas = None):
    self.lemmas = lemmas or self.load(file)
    self.file = file

  def save(self, file = file_out):
    print(f'save dict to: {file}')
    with open(file, 'w') as f:
      for lemma in sorted(self.lemmas.keys()):
        if lemma:
          for form in sorted(self.lemmas[lemma]):
            f.write(f'{lemma}\t{form}\n')
          f.write('\n')

  def load(self, file):
    lemmas = {}
    with open(file, 'r') as f:
      for lemma in f.read().split('\n\n'):
        forms = [l.split('\t') for l in lemma.split('\n')]
        key = forms[0][0]
        if key:
          lemmas[key] = [l[1] for l in forms if len(l) > 1]
    return lemmas

  def diff(self, file = file_unknown):
    lemmas = self.load(file)
    diff = set(self.lemmas.keys()) - set(lemmas.keys())
    print(f'new lemmas: {len(diff)} in {file}')

  def merge(self, file = file_unknown):
    lemmas = self.load(file)
    keys = {*set(self.lemmas.keys()), *set(lemmas.keys())}
    for lemma in keys:
      self.lemmas[lemma] = sorted({
        *set(lemmas.get(lemma, [])), 
        *set(self.lemmas.get(lemma, []))
        })

  def norm(self):
    def normalize(s): # ū ē ġ ċ ā ǣ ō ī ȳ
      for v in [('ū','u'),('ē','e'),('ġ','g'),('ċ','с'),('ā','a'),
                ('ǣ','æ'),('ō','o'),('ī','i'),('ȳ','y')]:
        s = s.replace(v[0], v[1]) 
      return s
    lemmas = {}
    for lemma in self.lemmas.keys():
      n_lemma = normalize(lemma)
      lemmas[n_lemma] = sorted(set(normalize(w) for w in 
          self.lemmas[lemma] + self.lemmas.get(n_lemma, []) + lemmas.get(n_lemma, [])))
    self.lemmas = lemmas

  def fix(self):
    for lemma in self.lemmas.keys():
      arr = []
      for form in self.lemmas[lemma]:
        arr += form.split(',')
      self.lemmas[lemma] = list(set(arr))

  def stat(self):
    print(f'lemmas: {len(self.lemmas.keys())} in {self.file}')
    print(f'Forms:  {sum(len(a) for a in self.lemmas.keys())} in {self.file}')

  def print(self, limit = 3):
    keys = list(self.lemmas.keys())
    for lemma in keys[:limit] + keys[-limit:]:
      print(f'{lemma}: {self.lemmas[lemma]}')


if __name__ == "__main__":
  # l0 = Lemmas(Lemmas.file_unknown)
  # l0.stat()

  # l1 = Lemmas()
  # l1.stat()
  # l1.diff()
  # l1.merge()
  # l1.save()

  # l2 = Lemmas(Lemmas.file_out)
  # l2.stat()
  # l2.print(1)

  # l3 = Lemmas()
  # l3.stat()
  # l3.norm()
  # l3.stat()
  # l3.save(Lemmas.file_unimorph_norm)

  # l3 = Lemmas(Lemmas.file_out)
  # l3.stat()
  # l3.fix()
  # l3.stat()
  # l3.save()

  l4 = Lemmas(Lemmas.file_out)
  l4.stat()
  l4.norm()
  l4.stat()
  l4.save(Lemmas.file_out_norm)
