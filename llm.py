from sqlmodel import SQLModel, Field, Relationship, create_engine, Session
from typing import List
from datetime import datetime


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
    llms: List["LLM"] = Relationship(back_populates="form")


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
    llms: List["LLM"] = Relationship(back_populates="predict")


class PredictRaw(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    promt: str
    content: str
    forms: str
    lemmas: str
    tool_calls: str = None


class LLM(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    predict_id: int = Field(foreign_key="predict.id")
    form_id: int = Field(foreign_key="form.id")
    lemma: str
    eq: bool
    predict: Predict = Relationship(back_populates="llms")
    form: Form = Relationship(back_populates="llms")


class LLMRaw(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    en: str
    ru: str
    morph: str
    syntax: str
    raw: str


# Создание базы данных
def init_db():
    engine = create_engine("sqlite:///d/llm/llm.db")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        corpus = Corpus(name="iswoc")
        session.add(corpus)
        session.commit()
        session.refresh(corpus)
        
        doc = Doc(name="forms.txt", corpus_id=corpus.id)
        session.add(doc)
        session.commit()

if __name__ == "__main__":
    init_db()
