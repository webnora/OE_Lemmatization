from lemmatazer import Lemmatazer

class ISWOC:
  path_in = 's/syntacticus-treebank-data/iswoc/'
  path_out = 'd/iswoc/'
  file_forms = 'forms.txt'

  def __init__(self, index = 1, path_out = path_out, path_in = path_in):
    with open(path_in + 'README.md', 'r') as f:
      self.files = [[e.strip() for e in l.split('|')] for l in f.read().split('\n') if 'Old English' in l]
    self.text = []
    self.index = index
    for f in self.files:
      self.readFile(path_in + f[2] + '.conll')
  
  def readFile(self, file):
    def getWord(line):
      arr = line.split('\t')
      if len(arr) > self.index:
        return arr[self.index]
      return ""

    with open(file, 'r') as f:
      for sentence in f.read().split('\n\n'):
        text = " ".join((getWord(l) for l in sentence.split('\n') if getWord(l)))
        self.text.append(text)

  def save(self, file = file_forms):
    print(f'save text to: {file}')
    with open(self.path_out + file, 'w') as f:
      f.write("\n".join(self.text))

  def lemmatize(self, file = path_out + file_forms, file_out = path_out + 'lemmatize.txt'):
    lm = Lemmatazer("")
    lm.parse(file)
    lm.stat()
    lm.save_text(file_out)


if __name__ == "__main__":
  cl = ISWOC(2)
  cl.save('lemmas.txt')

  cf = ISWOC()
  cf.save()
  cf.lemmatize()

  import pandas as pd
  print(pd.DataFrame(cf.files))
