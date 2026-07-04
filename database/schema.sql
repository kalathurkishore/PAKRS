-- SQLite Schema for PAKRS

CREATE TABLE IF NOT EXISTS notes (
    id TEXT PRIMARY KEY,
    title TEXT,
    body TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    labels TEXT -- Comma separated labels
);

CREATE TABLE IF NOT EXISTS links (
    id TEXT PRIMARY KEY,
    note_id TEXT,
    platform TEXT,
    url TEXT,
    FOREIGN KEY (note_id) REFERENCES notes (id) ON DELETE CASCADE
);

-- Full Text Search Table for Notes
CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(
    title,
    body,
    labels,
    content='notes',
    content_rowid='id',
    tokenize='porter'
);

-- Triggers to keep FTS index updated

CREATE TRIGGER IF NOT EXISTS notes_ai AFTER INSERT ON notes BEGIN
  INSERT INTO notes_fts(rowid, title, body, labels) VALUES (new.rowid, new.title, new.body, new.labels);
END;

CREATE TRIGGER IF NOT EXISTS notes_ad AFTER DELETE ON notes BEGIN
  INSERT INTO notes_fts(notes_fts, rowid, title, body, labels) VALUES('delete', old.rowid, old.title, old.body, old.labels);
END;

CREATE TRIGGER IF NOT EXISTS notes_au AFTER UPDATE ON notes BEGIN
  INSERT INTO notes_fts(notes_fts, rowid, title, body, labels) VALUES('delete', old.rowid, old.title, old.body, old.labels);
  INSERT INTO notes_fts(rowid, title, body, labels) VALUES (new.rowid, new.title, new.body, new.labels);
END;
