from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint, create_engine, Session, select
from typing import Optional, List
from datetime import datetime
from typing import Type
from pandas import DataFrame as df
from sqlalchemy.schema import CreateTable
import os


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
  doc: Doc = Relationship(back_populates="lines")
  forms: List["Form"] = Relationship(back_populates="line")
  predictions: List["Predict"] = Relationship(back_populates="line")

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
  at: datetime
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
  forms: str
  lemmas: str
  tool_calls: Optional[str]

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
  en: str
  ru: str
  morph: str
  syntax: str
  raw: str


class DB():
  db_path = "d/llm/llm.db"
  engine = create_engine("sqlite:///" + db_path)

  def init(self, drop = False):
    if drop:
      db = DB.db_path
      if os.path.exists(db):
        os.remove(db)
        print(f"DB deleted: {db}")
    else:
      SQLModel.metadata.drop_all(self.engine)
    SQLModel.metadata.create_all(self.engine)
    self.ddl()

    with Session(self.engine) as session:
      corpus = Corpus(corpus="iswoc")
      session.add(corpus)
      session.commit()
      session.refresh(corpus)
      
      doc = Doc(doc="forms.txt", corpus_id=corpus.id)
      session.add(doc)
      session.commit()

  def ddl(self):
    with open("llm.sql", "w") as file:
      for table in SQLModel.metadata.tables.values():
        file.write(f"{str(CreateTable(table).compile(self.engine)).strip()};\n")        

  def tbl(self, table: Type[SQLModel] = Doc):
    return Session(self.engine).exec(select(table))

  def df(self, table: Type[SQLModel] = Doc):
    return df([r.model_dump() for r in self.tbl(table)])

  def doc(self):
    return Session(self.engine).exec(
      select(Doc.id, Doc.doc, Corpus.corpus)
      .where(Corpus.id == Doc.corpus_id))

  # def print(self, dataFrame: df):
  #   print(df(dataFrame))


if __name__ == "__main__":
  db = DB()
  db.init()
  print(db.df())
  print(db.df(Corpus))
  print(df(db.doc()))
