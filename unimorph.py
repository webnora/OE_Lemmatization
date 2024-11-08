class Unimorph:
  file_in = 's/unimorph-ang/ang'
  file_out = 'd/unimorph/dict.txt'

  def __init__(self, file = file_in):
    self.lemmas = {}
    with open(file, 'r') as f:
      for line in f.read().split('\n'): #[:20]:
        arr = line.split('\t')
        # print(arr)
        if len(arr) > 1:
          key = arr[0]
          if key not in ['-','–']:
            lemma = self.lemmas.get(key, [])
            lemma.append(arr[1])
            self.lemmas[key] = lemma

  def stat(self):
    print(f'lemmas: {len(self.lemmas.keys())}')
  
  def save(self, file = file_out):
    print(f'save dict to: {file}')
    with open(file, 'w') as f:
      for lemma in sorted(self.lemmas.keys()):
        for form in self.lemmas[lemma]:
          f.write(f'{lemma}\t{form}\n')
        f.write('\n')


if __name__ == "__main__":
  u = Unimorph()
  u.save()
  u.stat()
