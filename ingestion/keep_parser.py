import os
import json
import re
from typing import Dict, Any, List
from bs4 import BeautifulSoup
from database.db_manager import DBManager

class KeepParser:
    def __init__(self):
        self.db_manager = DBManager()
        # Regex to find URLs in text
        self.url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    def parse_directory(self, directory_path: str):
        """Iterates over files in a directory and parses HTML or JSON Keep exports."""
        if not os.path.exists(directory_path):
            print(f"Directory not found: {directory_path}")
            return

        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if filename.endswith('.json'):
                self._parse_json_note(file_path)
            elif filename.endswith('.html'):
                self._parse_html_note(file_path)

    def _parse_json_note(self, file_path: str):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"Error parsing JSON: {file_path}")
                return
        
        title = data.get('title', '')
        
        # Determine body text (could be list items or textContent)
        body = data.get('textContent', '')
        if 'listContent' in data:
            list_items = [item.get('text', '') for item in data['listContent']]
            body += '\n'.join(list_items)
            
        labels = [label.get('name', '') for label in data.get('labels', [])]
        
        # Try finding URLs in annotations or in the text body
        links = self.url_pattern.findall(body)
        for annotation in data.get('annotations', []):
            if 'url' in annotation:
                links.append(annotation['url'])
                
        # Deduplicate links
        links = list(set(links))
        
        note_data = {
            'title': title,
            'body': body,
            'labels': labels,
            'links': links
        }
        
        # Filter out empty notes without links
        if not body.strip() and not title.strip() and not links:
            return

        self.db_manager.insert_note(note_data)
        print(f"Imported JSON note: {title or 'Untitled'}")

    def _parse_html_note(self, file_path: str):
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        # Standard Google Keep Takeout HTML structure
        title_elem = soup.find('div', class_='title')
        title = title_elem.text.strip() if title_elem else ''
        
        content_elem = soup.find('div', class_='content')
        body = content_elem.text.strip() if content_elem else ''
        
        labels_elem = soup.find('div', class_='labels')
        labels = []
        if labels_elem:
            labels = [span.text.strip() for span in labels_elem.find_all('span')]
            
        # Extract links from anchor tags and from raw text
        links = self.url_pattern.findall(body)
        if content_elem:
            for a_tag in content_elem.find_all('a'):
                href = a_tag.get('href')
                if href:
                    links.append(href)
                    
        # Deduplicate links
        links = list(set(links))
        
        note_data = {
            'title': title,
            'body': body,
            'labels': labels,
            'links': links
        }
        
        # Filter out empty notes without links
        if not body.strip() and not title.strip() and not links:
            return

        self.db_manager.insert_note(note_data)
        print(f"Imported HTML note: {title or 'Untitled'}")

if __name__ == '__main__':
    parser = KeepParser()
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    print(f"Starting import from {data_dir}...")
    parser.parse_directory(data_dir)
    print("Import complete.")
