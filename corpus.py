from os import listdir
from lemmatazer import Lemmatazer

class Corpus:
  def __init__(self, path = 'd/in/calgary/'):
    self.path = path
    self.files = (f for f in listdir(path) if f.endswith('.txt'))
    self.lm = Lemmatazer()
  
  def parse(self, path_out = 'd/corpus/out/'):
    for f in self.files:
      print('FILE:', f)
      self.lm.parse(self.path + f)
      self.lm.save_text(path_out + f)
      self.lm.stat(stop_len = False)
      print()


if __name__ == "__main__":
  co = Corpus()
  co.parse()
