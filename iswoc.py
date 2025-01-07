from lemmatazer import Lemmatazer
from db import DB, Corpus, Doc, Line, Form

class ISWOC:
  path_in = 's/syntacticus-treebank-data/iswoc/'
  path_out = 'd/iswoc/'
  file_forms = 'forms.txt'

  def __init__(self, index = 1, path_out = path_out, path_in = path_in):
    with open(path_in + 'README.md', 'r') as f:
      self.files_desc = [[e.strip() for e in l.split('|')] for l in f.read().split('\n') if 'Old English' in l]
    self.files = [f[2] + '.conll' for f in self.files_desc]
    self.text = []
    self.docs = []
    self.index = index
    self.path_in = path_in
    self.path_out = path_out
    self.corpus = Corpus(id=0, corpus="iswoc", path=path_in)
    self.readAll()

  def readAll(self):
    for id, doc in enumerate(self.files):
      self.docs.append(Doc(id=id, doc=doc, corpus_id=self.corpus.id))
      self.readFile(id, doc)

  def readFile(self, id, file):
    def getWord(line):
      arr = line.split('\t')
      if len(arr) > self.index:
        return arr[self.index]
      return ""

    with open(self.path_in + file, 'r') as f:
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

  def commit(self):
    db = DB()
    db.init()
    with db.s as s:
      s.add(self.corpus)
      for doc in self.docs:
        s.add(doc)
      s.commit()
    db.stat()

if __name__ == "__main__":
  o = ISWOC()
  o.commit()

  cl = ISWOC(2)
  cl.save('lemmas.txt')

  cf = ISWOC()
  cf.save()
  cf.lemmatize()

  import pandas as pd
  print(pd.DataFrame(cf.files_desc))
