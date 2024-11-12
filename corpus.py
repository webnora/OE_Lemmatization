from os import listdir
from lemmatazer import Lemmatazer

class Corpus:
  path = 'd/in/calgary/'
  file_out = 'd/corpus/out.txt'

  def __init__(self, path = path, lm = Lemmatazer()):
    self.path = path
    self.files = (f for f in listdir(path) if f.endswith('.txt'))
    self.lm = lm
  
  def parse(self, path_out = 'd/corpus/out/'):
    for f in self.files:
      print('FILE:', f)
      self.lm.parse(self.path + f)
      self.lm.save_text(path_out + f)
      self.lm.stat(stop_len = False)
      print()

  def parse_to_one(self, file = file_out):
    words = []
    for f in self.files:
      self.lm.parse(self.path + f)
      words += self.lm.words
    self.lm.words = words
    self.lm.save_text(file)
    self.lm.stat(stop_len = False)


if __name__ == "__main__":
  co = Corpus()
  # co.parse()
  co.parse_to_one()
