from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint, create_engine, Session, select
from typing import Type, Optional, List, Dict
from datetime import datetime
from pandas import DataFrame as df
from sqlalchemy.schema import CreateTable
import os
from sqlalchemy import Column, JSON, func


class Corpus(SQLModel, table=True):
  id: int = Field(default=None, primary_key=True, nullable=False)
  corpus: str
  docs: List["Doc"] = Relationship(back_populates="corpus")

class Doc(SQLModel, table=True):
  id: int = Field(default=None, primary_key=True, nullable=False)
  doc: str
  corpus_id: int = Field(foreign_key="corpus.id")
  corpus: Corpus = Relationship(back_populates="docs")
  lines: List["Line"] = Relationship(back_populates="doc")

class Line(SQLModel, table=True):
  id: int = Field(default=None, primary_key=True, nullable=False)
  doc_id: int = Field(foreign_key="doc.id")
  num: int
  doc: Doc = Relationship(back_populates="lines")
  line: str
  lemmas: Optional[str]
  forms: List["Form"] = Relationship(back_populates="line")
  predictions: List["Predict"] = Relationship(back_populates="line")
  __table_args__ = (UniqueConstraint("doc_id", "num", name="uq_doc_num"),)

class Form(SQLModel, table=True):
  id: int = Field(default=None, primary_key=True, nullable=False)
  line_id: int = Field(foreign_key="line.id")
  line: Line = Relationship(back_populates="forms")
  num: int
  form: str
  lemma: str
  lemmas: List["Lemma"] = Relationship(back_populates="form")
  __table_args__ = (UniqueConstraint("line_id", "num", name="uq_line_num"),)

class Model(SQLModel, table=True):
  id: int = Field(default=None, primary_key=True, nullable=False)
  model: str
  predictions: List["Predict"] = Relationship(back_populates="model")

class Predict(SQLModel, table=True):
  id: int = Field(default=None, primary_key=True, nullable=False)
  model_id: int = Field(foreign_key="model.id")
  line_id: int = Field(foreign_key="line.id")
  model: Model = Relationship(back_populates="predictions")
  line: Line = Relationship(back_populates="predictions")
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

class PredictRaw(SQLModel, table=True):
  id: int = Field(default=None, primary_key=True, nullable=False, foreign_key="predict.id")
  promt: str
  content: str
  forms: Optional[str]
  lemmas: Optional[str]
  tool_calls: Optional[Dict] = Field(default_factory=dict, sa_column=Column(JSON))

class Lemma(SQLModel, table=True):
  id: int = Field(default=None, primary_key=True, nullable=False)
  predict_id: int = Field(foreign_key="predict.id")
  form_id: int = Field(foreign_key="form.id")
  lemma: str
  eq: bool
  predict: Predict = Relationship(back_populates="lemmas")
  form: Form = Relationship(back_populates="lemmas")

class LemmaRaw(SQLModel, table=True):
  id: int = Field(default=None, primary_key=True, nullable=False, foreign_key="lemma.id")
  en: Optional[str]
  ru: Optional[str]
  morph: Optional[str]
  syntax: Optional[str]
  raw: Dict = Field(default_factory=dict, sa_column=Column(JSON))


class DB():
  db_path = "d/llm/llm.db"

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

    with self.s as s:
      # Mæg gehyran se ðe wyle be þam halgan mædene Eugenian Philyppus dæhter hu heo ðurh mægðhad mærlice þeah and þurh martyrdom þisne middaneard oferswað
      # mag gehyran se þe willan be se halig mægden Eugenia Philippus dohtor hu heo þurh mægþhad mærlice þeon and þurh martyrdom þes middangeard oferswiðan
      s.add(Corpus(id=1, corpus="iswoc"))
      s.add(Doc(id=1, doc="forms.txt", corpus_id=1))
      s.add(Line(id=1, doc_id=1, num=1, line="Mæg gehyran se ðe", lemmas="mag gehyran se þe"))
      s.add(Form(id=1, line_id=1, num=1, form="Mæg", lemma="mag"))
      s.add(Form(id=4, line_id=1, num=4, form="ðe", lemma="þe"))
      s.add(Model(id=1, model="mistral:7b"))
      s.add(Predict(id=1, model_id=1, line_id=1, done=True, no_eq=0, temperature=0.0, at=datetime.fromisoformat('2025-01-03T10:23:28.830015Z'),
        load_duration=21163667, prompt_eval_duration=261000000, eval_duration=551000000, prompt_tokens=30, completion_tokens=31))
      s.add(Lemma(id=1, predict_id=1, form_id=1, lemma="mag", eq=True))
      s.add(LemmaRaw(id=1, en="can", ru="может", morph="pronoun", syntax="subject", 
                     raw={"word_form": "Mæg",
                          "lemma": "mag",
                          "translation_en": "can",
                          "translation_ru": "может",
                          "morph_analysis": "pronoun, 3rd person singular present subjunctive of magan (can)",
                          "syntax_analysis": "subject"}))
      s.commit()

      # corpus = Corpus(corpus="iswoc")
      # s.add(corpus)
      # s.commit()
      # s.refresh(corpus)      
      # doc = Doc(doc="forms.txt", corpus_id=corpus.id)
      # s.add(doc)
      # s.commit()

  def ddl(self):
    with open("db.sql", "w") as file:
      for table in SQLModel.metadata.tables.values():
        file.write(f"{str(CreateTable(table).compile(self.engine)).strip()};\n")        

  def tbl(self, table: Type[SQLModel] = Doc):
    return self.s.exec(select(table))

  def df(self, tbl: Type[SQLModel] = Doc):
    return df([r.model_dump() for r in self.tbl(tbl)], columns=tbl.model_fields)

  def get_doc(self):
    return self.s.exec(select(Doc.id, Doc.doc, Corpus.corpus).where(Corpus.id == Doc.corpus_id))
  
  def get_lemma(self, lemma = 'mag'):
    return self.s.exec(select(LemmaRaw.raw).where(
      func.json_extract(LemmaRaw.raw, '$.lemma') == lemma)).first()

if __name__ == "__main__":
  db = DB()
  db.init()
  # print(db.df(Corpus))
  # print(db.df())
  print(df(db.get_doc()))
  print(db.df(Model))
  print(db.df(Line))
  print(db.df(Form))
  print(db.df(Predict))
  print(db.df(Lemma))
  print(db.df(LemmaRaw))
  print(db.get_lemma())
