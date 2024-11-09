from lemmas import Lemmas

class Unimorph(Lemmas):
  file_in  = 's/unimorph-ang/ang'
  file_out = 'd/unimorph/dict.tsv'

  def __init__(self, file = file_in):
    super().__init__(file)

  def save(self, file = file_out):
    super().save(file)

  def load(self, file):
    lemmas = {}
    with open(file, 'r') as f:
      for line in f.read().split('\n'):
        arr = line.split('\t')
        if len(arr) > 1:
          key = arr[0]
          if key not in ['-','–']:
            lemma = lemmas.get(key, [])
            lemma.append(arr[1])
            lemmas[key] = sorted(set(lemma))
    return lemmas


if __name__ == "__main__":
  u = Unimorph()
  u.stat()
  u.save()
  u.print(1)
