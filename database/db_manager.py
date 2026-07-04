import sqlite3
import os
import uuid
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'pakrs.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')

class DBManager:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Initializes the database schema if it doesn't exist."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with self.get_connection() as conn:
            with open(SCHEMA_PATH, 'r') as f:
                conn.executescript(f.read())
            conn.commit()

    def insert_note(self, note_data: Dict[str, Any]) -> str:
        """Inserts a note and its associated links."""
        note_id = str(uuid.uuid4())
        title = note_data.get('title', '')
        body = note_data.get('body', '')
        labels = ','.join(note_data.get('labels', []))
        links = note_data.get('links', [])
        created_at = note_data.get('created_at', None)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Insert Note
            if created_at:
                cursor.execute('''
                    INSERT INTO notes (id, title, body, labels, created_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (note_id, title, body, labels, created_at))
            else:
                cursor.execute('''
                    INSERT INTO notes (id, title, body, labels)
                    VALUES (?, ?, ?, ?)
                ''', (note_id, title, body, labels))
            
            # Insert Links
            for url in links:
                link_id = str(uuid.uuid4())
                platform = self._determine_platform(url)
                cursor.execute('''
                    INSERT INTO links (id, note_id, platform, url)
                    VALUES (?, ?, ?, ?)
                ''', (link_id, note_id, platform, url))
                
            conn.commit()
        return note_id

    def _determine_platform(self, url: str) -> str:
        """Heuristic to determine the platform from URL."""
        url_lower = url.lower()
        if 'youtube.com' in url_lower or 'youtu.be' in url_lower:
            return 'youtube'
        elif 'instagram.com' in url_lower:
            return 'instagram'
        else:
            return 'web'
            
    def search_notes(self, query: str) -> List[Dict[str, Any]]:
        """Perform exact keyword search using FTS5."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Format query for better FTS wildcard matching
            fts_query = query.strip()
            if not fts_query.endswith('*'):
                fts_query += '*'
                
            cursor.execute('''
                SELECT n.id, n.title, n.body, n.labels, n.created_at,
                       snippet(notes_fts, -1, '<mark style="background-color: #ffd166; color: black; border-radius: 3px; padding: 0 2px;">', '</mark>', '...', 25) as search_snippet
                FROM notes_fts f
                JOIN notes n ON f.rowid = n.rowid
                WHERE notes_fts MATCH ?
                ORDER BY n.created_at DESC
            ''', (fts_query,))
            return [dict(row) for row in cursor.fetchall()]

    def get_all_notes(self) -> List[Dict[str, Any]]:
        """Fetch all notes sorted by created_at DESC."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, title, body, labels, created_at
                FROM notes
                ORDER BY created_at DESC
            ''')
            return [dict(row) for row in cursor.fetchall()]

    def get_links_for_note(self, note_id: str) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM links WHERE note_id = ?', (note_id,))
            return [dict(row) for row in cursor.fetchall()]

    def get_all_links_map(self) -> Dict[str, List[Dict[str, Any]]]:
        """Fetch all links and group by note_id to prevent N+1 queries."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM links')
            links_map = {}
            for row in cursor.fetchall():
                d = dict(row)
                links_map.setdefault(d['note_id'], []).append(d)
            return links_map

    def get_all_labels(self) -> List[str]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT labels FROM notes WHERE labels != ""')
            all_labels = set()
            for row in cursor.fetchall():
                for label in row['labels'].split(','):
                    if label.strip():
                        all_labels.add(label.strip())
            return sorted(list(all_labels))

    def get_all_platforms(self) -> List[str]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT platform FROM links WHERE platform != ""')
            return sorted([row['platform'] for row in cursor.fetchall()])
