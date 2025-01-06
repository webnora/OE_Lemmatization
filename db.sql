CREATE TABLE corpus (
	id INTEGER NOT NULL, 
	corpus VARCHAR NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE doc (
	id INTEGER NOT NULL, 
	doc VARCHAR NOT NULL, 
	corpus_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(corpus_id) REFERENCES corpus (id)
);
CREATE TABLE line (
	id INTEGER NOT NULL, 
	doc_id INTEGER NOT NULL, 
	num INTEGER NOT NULL, 
	line VARCHAR NOT NULL, 
	lemmas VARCHAR, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_doc_num UNIQUE (doc_id, num), 
	FOREIGN KEY(doc_id) REFERENCES doc (id)
);
CREATE TABLE form (
	id INTEGER NOT NULL, 
	line_id INTEGER NOT NULL, 
	num INTEGER NOT NULL, 
	form VARCHAR NOT NULL, 
	lemma VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_line_num UNIQUE (line_id, num), 
	FOREIGN KEY(line_id) REFERENCES line (id)
);
CREATE TABLE predict (
	id INTEGER NOT NULL, 
	line_id INTEGER NOT NULL, 
	model VARCHAR NOT NULL, 
	done BOOLEAN NOT NULL, 
	no_eq INTEGER NOT NULL, 
	at DATETIME NOT NULL, 
	load_duration INTEGER NOT NULL, 
	prompt_eval_duration INTEGER NOT NULL, 
	eval_duration INTEGER NOT NULL, 
	prompt_tokens INTEGER NOT NULL, 
	completion_tokens INTEGER NOT NULL, 
	temperature FLOAT NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(line_id) REFERENCES line (id)
);
CREATE TABLE predictraw (
	id INTEGER NOT NULL, 
	promt VARCHAR NOT NULL, 
	content VARCHAR NOT NULL, 
	forms VARCHAR, 
	lemmas VARCHAR, 
	tool_calls JSON, 
	PRIMARY KEY (id), 
	FOREIGN KEY(id) REFERENCES predict (id)
);
CREATE TABLE lemma (
	id INTEGER NOT NULL, 
	predict_id INTEGER NOT NULL, 
	form_id INTEGER NOT NULL, 
	lemma VARCHAR NOT NULL, 
	eq BOOLEAN NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(predict_id) REFERENCES predict (id), 
	FOREIGN KEY(form_id) REFERENCES form (id)
);
CREATE TABLE lemmaraw (
	id INTEGER NOT NULL, 
	en VARCHAR, 
	ru VARCHAR, 
	morph VARCHAR, 
	syntax VARCHAR, 
	raw JSON, 
	PRIMARY KEY (id), 
	FOREIGN KEY(id) REFERENCES lemma (id)
);
