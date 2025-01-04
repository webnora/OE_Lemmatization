from sqlmodel import SQLModel, Field, Relationship, create_engine, Session, select
from typing import Optional, List
from datetime import datetime
from typing import Type
import pandas as pd
from sqlalchemy.schema import CreateTable
import os


class Corpus(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    name: str
    docs: List["Doc"] = Relationship(back_populates="corpus")

class Doc(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    name: str
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

class Model(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    name: str
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

    def init(self):
        if os.path.exists(DB.db_path):
            os.remove(DB.db_path)
        # SQLModel.metadata.drop_all(self.engine)
        SQLModel.metadata.create_all(self.engine)
        self.ddl()

        with Session(self.engine) as session:
            corpus = Corpus(name="iswoc")
            session.add(corpus)
            session.commit()
            session.refresh(corpus)
            
            doc = Doc(name="forms.txt", corpus_id=corpus.id)
            session.add(doc)
            session.commit()

    def ddl(self):
        with open("llm.sql", "w") as file:
            for table in SQLModel.metadata.tables.values():
                file.write(f"{str(CreateTable(table).compile(self.engine)).strip()};\n")        

    def df(self, table: Type[SQLModel] = Doc):
        with Session(self.engine) as session:
            statement = select(table)
            results = session.exec(statement)
            items = [item.model_dump() for item in results]
            return pd.DataFrame(items)


if __name__ == "__main__":
    db = DB()
    db.init()
    print(db.df())
    print(db.df(Corpus))
