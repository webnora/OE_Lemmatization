from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint, create_engine, Session, select
from typing import Type, Optional, List, Dict
from datetime import datetime
from pandas import DataFrame as df
from sqlalchemy.schema import CreateTable
import os
from sqlalchemy import Column, JSON, func, text

class Corpus(SQLModel, table=True):
  id: int = Field(default=None, primary_key=True)
  corpus: str
  path: Optional[str]
  docs: List["Doc"] = Relationship(back_populates="corpus")

class Doc(SQLModel, table=True):
  id: int = Field(default=None, primary_key=True)
  doc: str
  corpus_id: int = Field(foreign_key="corpus.id")
  corpus: Corpus = Relationship(back_populates="docs")
  lines: List["Line"] = Relationship(back_populates="doc")

class Line(SQLModel, table=True):
  id: int = Field(default=None, primary_key=True)
  doc_id: int = Field(foreign_key="doc.id")
  num: int
  doc: Doc = Relationship(back_populates="lines")
  line: str
  lemmas: Optional[str]
  forms: List["Form"] = Relationship(back_populates="line")
  predictions: List["Predict"] = Relationship(back_populates="line")
  __table_args__ = (UniqueConstraint("doc_id", "num", name="uq_doc_num"),)

class Form(SQLModel, table=True):
  id: int = Field(default=None, primary_key=True)
  line_id: int = Field(foreign_key="line.id")
  line: Line = Relationship(back_populates="forms")
  num: int
  form: str
  lemma: str
  lemmas: List["Lemma"] = Relationship(back_populates="form")
  __table_args__ = (UniqueConstraint("line_id", "num", name="uq_line_num"),)

# class Model(SQLModel, table=True):
#   id: str = Field(primary_key=True)
#   # model: str
#   predictions: List["Predict"] = Relationship(back_populates="model")

class Predict(SQLModel, table=True):
  id: int = Field(default=None, primary_key=True)
  line_id: int = Field(foreign_key="line.id")
  line: Line = Relationship(back_populates="predictions")
  # model: Model = Relationship(back_populates="predictions")
  # model_id: int = Field(foreign_key="model.id")
  model: str
  done: bool
  no_eq: int
  at: datetime # = Field(default_factory=datetime.utcnow)
  load_duration: int
  prompt_eval_duration: int
  eval_duration: int
  prompt_tokens: int
  completion_tokens: int
  temperature: float
  lemmas: List["Lemma"] = Relationship(back_populates="predict")
  raw: Optional["PredictRaw"] = Relationship(back_populates="predict")

class PredictRaw(SQLModel, table=True):
  id: int = Field(default=None, primary_key=True, foreign_key="predict.id")
  promt: str
  content: str
  forms: Optional[str]
  lemmas: Optional[str]
  tool_calls: Optional[Dict] = Field(default_factory=dict, sa_column=Column(JSON))
  predict: Predict = Relationship(back_populates="raw")

class Lemma(SQLModel, table=True):
  id: int = Field(default=None, primary_key=True)
  predict_id: int = Field(foreign_key="predict.id")
  form_id: int = Field(foreign_key="form.id")
  lemma: str
  eq: bool
  predict: Predict = Relationship(back_populates="lemmas")
  form: Form = Relationship(back_populates="lemmas")
  raw: Optional["LemmaRaw"] = Relationship(back_populates="lemma")

class LemmaRaw(SQLModel, table=True):
  id: int = Field(default=None, primary_key=True, foreign_key="lemma.id")
  en: Optional[str]
  ru: Optional[str]
  morph: Optional[str]
  syntax: Optional[str]
  raw: Dict = Field(default_factory=dict, sa_column=Column(JSON))
  lemma: Lemma = Relationship(back_populates="raw")

class DB():
  db_path = "db/llm.db"

  def __init__(self, echo=False, db_path=db_path) -> None:
    self.engine = create_engine("sqlite:///" + db_path, echo=echo)
    self.s = Session(self.engine)

  def init(self, drop=0):
    if drop:
      db = DB.db_path
      if os.path.exists(db):
        os.remove(db)
        print(f"DB deleted: {db}")
    else:
      SQLModel.metadata.drop_all(self.engine)
    SQLModel.metadata.create_all(self.engine)
    self.ddl()

  def ddl(self):
    with open("db.sql", "w") as file:
      for table in SQLModel.metadata.tables.values():
        file.write(f"{str(CreateTable(table).compile(self.engine)).strip()};\n")        
  
  def stat(self):
    for v in self.s.exec(text("SELECT name FROM sqlite_master WHERE type='table'")): # type: ignore
      print(f"{self.s.exec(text(f"SELECT COUNT(*) FROM {v[0]}")).one()[0]}: {v[0]}") # type: ignore

  def tbl(self, table: Type[SQLModel] = Doc):
    return self.s.exec(select(table))

  def df(self, tbl: Type[SQLModel] = Doc):
    return df([r.model_dump() for r in self.tbl(tbl)], columns=tbl.model_fields)

  def get_doc(self):
    return self.s.exec(select(Doc.id, Doc.doc, Corpus.corpus).where(Corpus.id == Doc.corpus_id))
  
  def get_lemma(self, lemma = 'mag'):
    return self.s.exec(select(LemmaRaw.raw).where(
      func.json_extract(LemmaRaw.raw, '$.lemma') == lemma)).first()

  def add_test(self):
    with self.s as s:
      form = Form(num=0, form="Mæg", lemma="mag") # type: ignore
      corpus = Corpus(corpus="iswoc", path="", docs=[
        Doc(doc="forms.txt", 
          lines=[Line(num=0, line="Mæg gehyran se ðe", lemmas="mag gehyran se þe", 
            forms=[form],  
            predictions=[Predict(model="mistral:7b", done=True, no_eq=0, temperature=0.0, 
              at=datetime.fromisoformat('2025-01-03T10:23:28.830015Z'),
              load_duration=21163667, prompt_eval_duration=261000000, eval_duration=551000000, 
              prompt_tokens=30, completion_tokens=31, 
              raw=PredictRaw(promt="", content=""), # type: ignore
              lemmas=[Lemma(form=form, lemma="mag", eq=True,
                raw=LemmaRaw(id=1, en="can", ru="может", morph="pronoun", syntax="subject", 
                  raw={"word_form": "Mæg",
                    "lemma": "mag",
                    "translation_en": "can",
                    "translation_ru": "может",
                    "morph_analysis": "pronoun, 3rd person singular present subjunctive of magan (can)",
                    "syntax_analysis": "subject"}) 
              )] # type: ignore
            )]
          )]
        )]
      )
      s.add(corpus)
      s.commit() # s.refresh(corpus)
      # line = corpus.docs[0].lines[0]
      # print(line.forms[0].lemmas[0].raw)
      # print(line.predictions[0].raw)         


if __name__ == "__main__":
  db = DB()
  # db.init()
  # db.add_test()
  db.stat()
  # print(db.df(Corpus))
  # print(db.df())
  # print(df(db.get_doc()))
  # print(db.df(Line))
  # print(db.df(Form))
  # print(db.df(Predict))
  # print(db.df(PredictRaw))
  # print(db.df(Lemma))
  # print(db.df(LemmaRaw))
  # print(db.get_lemma())
