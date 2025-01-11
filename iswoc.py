from lemmatazer import Lemmatazer
from db import DB, Corpus, Doc, Line, Form

class ISWOC:
  path_in = 's/syntacticus-treebank-data/iswoc/'
  path_out = 'd/iswoc/'
  file_forms = 'forms.txt'
  file_lemmas = 'lemmas.txt'

  def __init__(self, path_out = path_out, path_in = path_in):
    with open(path_in + 'README.md', 'r') as f:
      self.files_desc = [[e.strip() for e in l.split('|')] for l in f.read().split('\n') if 'Old English' in l]
    self.files = [f[2] + '.conll' for f in self.files_desc]
    self.text = []
    self.path_in = path_in
    self.path_out = path_out
    self.corpus = Corpus(id=1, corpus="iswoc", path=path_in, docs=self.read_docs())

  def read_docs(self):
    return [self.read_doc(file) for file in self.files]

  def read_doc(self, file):
    with open(self.path_in + file, 'r') as f:
      doc = Doc(doc=file) # type: ignore
      for line_num, sentence in enumerate(f.read().split('\n\n')):
        line = Line(num=line_num) # type: ignore
        num = 0
        for word in sentence.split('\n'):
          if word:
            arr = word.split('\t')
            if len(arr) > 2:
              form, lemma = arr[1:3]
              line.forms.append(Form(num=num, form=form, lemma=lemma)) # type: ignore
              num += 1
        line.line   = " ".join(f.form  for f in line.forms)
        line.lemmas = " ".join(f.lemma for f in line.forms)
        doc.lines.append(line)
        # text = " ".join()
        # self.text.append(text)
    return doc

  def lines(self):
    return (line for doc in self.corpus.docs for line in doc.lines)

  def save(self, file = file_forms, key="line"):
    print(f'save text to: {file}')
    with open(self.path_out + file, 'w') as f:
      f.write("\n".join(list(getattr(line, key) for line in self.lines())))

  def save_lemmas(self, file = file_lemmas):
    self.save(file, "lemmas")

  def lemmatize(self, file = path_out + file_forms, file_out = path_out + 'lemmatize.txt'):
    lm = Lemmatazer("")
    lm.parse(file)
    lm.stat()
    lm.save_text(file_out)

  def commit(self, init=False):
    db = DB()
    if init:
      db.init()
    db.s.add(self.corpus)
    db.s.commit()
    db.stat()


if __name__ == "__main__":
  o = ISWOC()
  # o.commit()
  o.save()
  o.save_lemmas()
  o.lemmatize()

  from pandas import DataFrame as df
  print(df(o.files_desc))
