from unimorph import Unimorph

class Lemmas:
  file_in = Unimorph.file_out
  file_out = 'd/lemmas/dict.txt'
  file_unknown = 'd/in/dict.txt'

  def __init__(self, file = file_in):
    self.lemmas = self.load(file)
    self.file = file

  def load(self, file = file_in):
    lemmas = {}
    with open(file, 'r') as f:
      for lemma in f.read().split('\n\n'):
        forms = [l.split('\t') for l in lemma.split('\n')]
        key = forms[0][0]
        if key:
          lemmas[key] = [l[1] for l in forms if len(l) > 1]
    return lemmas

  def save(self, file = file_out):
    print(f'save dict to: {file}')
    with open(file, 'w') as f:
      for lemma in sorted(self.lemmas.keys()):
        if lemma:
          for form in self.lemmas[lemma]:
            f.write(f'{lemma}\t{form}\n')
          f.write('\n')

  def stat(self):
    print(f'lemmas: {len(self.lemmas.keys())} in {self.file}')

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

  def print(self, limit = 3):
    keys = list(self.lemmas.keys())
    for lemma in keys[:limit] + keys[-limit:]:
      print(f'{lemma}: {self.lemmas[lemma]}')


if __name__ == "__main__":
  u0 = Lemmas(Lemmas.file_unknown)
  u0.stat()

  u1 = Lemmas()
  u1.stat()
  u1.diff()
  u1.merge()
  u1.save()

  u2 = Lemmas(Lemmas.file_out)
  u2.stat()
  u2.print()
