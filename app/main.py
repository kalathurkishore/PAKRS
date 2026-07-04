import streamlit as st
import os
import sys
import re
import math
import importlib
from datetime import datetime

# Ensure the database package can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Force reload the module to prevent Streamlit from caching old module definitions
if "database.db_manager" in sys.modules:
    importlib.reload(sys.modules["database.db_manager"])
from database.db_manager import DBManager

st.set_page_config(page_title="PAKRS - Personal AI Knowledge Retrieval System", layout="wide", page_icon="🧠")

db = DBManager()

def get_youtube_id(url):
    """Extract YouTube video ID from URL."""
    # Matches youtube.com/watch?v=, youtu.be/, youtube.com/embed/, youtube.com/shorts/
    match = re.search(r'(?:v=|/v/|youtu\.be/|/embed/|/shorts/)([^&?/\s]{11})', url)
    return match.group(1) if match else None

st.title("🧠 PAKRS")
st.markdown("### Personal AI Knowledge Retrieval System")
st.markdown("---")

# Search Bar
search_query = st.text_input("🔍 Search your notes", placeholder="e.g. transformers, recipe, interior design...")

# When search query changes, reset page
if "last_search_query" not in st.session_state:
    st.session_state.last_search_query = search_query

if search_query != st.session_state.last_search_query:
    st.session_state.page = 1
    st.session_state.last_search_query = search_query

# Sidebar Filters
st.sidebar.title("🗂️ Filters")
all_labels = db.get_all_labels()
all_platforms = db.get_all_platforms()

selected_labels = st.sidebar.multiselect("Filter by Tags", all_labels)
selected_platforms = st.sidebar.multiselect("Filter by Platform", all_platforms)

import sqlite3
import time

try:
    results = db.search_notes(search_query) if search_query else db.get_all_notes()
except sqlite3.DatabaseError:
    st.warning("Cloud database corruption detected. Rebuilding from portable SQL dump... Please wait.")
    
    if os.path.exists(db.db_path):
        try:
            os.remove(db.db_path)
        except Exception:
            pass
            
    dump_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'dump.sql')
    if os.path.exists(dump_path):
        with sqlite3.connect(db.db_path) as conn:
            with open(dump_path, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
        time.sleep(1)
        st.rerun()
    else:
        st.error("Error: Could not find SQL dump to rebuild the database.")
        results = []

# Apply Filters
if selected_labels or selected_platforms:
    links_map = db.get_all_links_map()
    filtered_results = []
    for row in results:
        if selected_labels:
            row_labels = [l.strip() for l in row['labels'].split(',')] if row['labels'] else []
            if not any(l in row_labels for l in selected_labels):
                continue
                
        if selected_platforms:
            row_links = links_map.get(row['id'], [])
            row_platforms = [link['platform'] for link in row_links]
            if not any(p in row_platforms for p in selected_platforms):
                continue
                
        filtered_results.append(row)
        
    results = filtered_results
if not search_query:
    with db.get_connection() as conn:
        cursor = conn.cursor()
        note_count = cursor.execute("SELECT count(*) FROM notes").fetchone()[0]
        link_count = cursor.execute("SELECT count(*) FROM links").fetchone()[0]
    
    st.info(f"Database currently holds **{note_count} notes** and **{link_count} links**.")

if len(results) == 0:
    st.warning("No notes found. Try using fewer or different keywords.")
else:
    if search_query:
        st.success(f"Found {len(results)} results")
        
    # Pagination Setup
    if "page" not in st.session_state:
        st.session_state.page = 1
        
    def reset_page():
        st.session_state.page = 1
        
    # Put pagination controls in a nice layout
    col1, col2 = st.columns([1, 4])
    with col1:
        page_size = st.selectbox("Items per page", options=[10, 20, 30, 40, 50], index=0, on_change=reset_page)
        
    total_pages = math.ceil(len(results) / page_size) if len(results) > 0 else 1
    
    # Ensure current page is valid
    if st.session_state.page > total_pages:
        st.session_state.page = total_pages
        
    start_idx = (st.session_state.page - 1) * page_size
    end_idx = start_idx + page_size
    page_results = results[start_idx:end_idx]
    
    for row in page_results:
        with st.container(border=True):
            st.subheader(f"📄 {row['title'] or 'Untitled Note'}")
            
            # Show date if it exists
            if row.get('created_at'):
                try:
                    # SQLite CURRENT_TIMESTAMP format is 'YYYY-MM-DD HH:MM:SS'
                    dt = datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S')
                    formatted_date = dt.strftime('%B %d, %Y at %I:%M %p')
                    st.caption(f"🕒 Saved on: {formatted_date}")
                except Exception:
                    st.caption(f"🕒 Saved on: {row['created_at']}")
            
            # Show labels if they exist
            if row['labels']:
                tags_html = " ".join([f"<span style='background-color: #4f4f4f; color: white; padding: 2px 8px; border-radius: 10px; font-size: 12px; margin-right: 5px;'>{tag}</span>" for tag in row['labels'].split(',')])
                st.markdown(tags_html, unsafe_allow_html=True)
                st.write("") # padding
            
            # Show the body
            if 'search_snippet' in row and row['search_snippet']:
                st.markdown(f"<div style='font-size: 14px; color: #d0d0d0;'>... {row['search_snippet']} ...</div>", unsafe_allow_html=True)
            elif row['body']:
                body_preview = row['body'][:300] + "..." if len(row['body']) > 300 else row['body']
                st.markdown(f"<div style='font-size: 14px; color: #d0d0d0;'>{body_preview}</div>", unsafe_allow_html=True)
            else:
                st.caption("No text content.")
                
            # Fetch links for this note
            links = db.get_links_for_note(row['id'])
            if links:
                st.write("")
                st.markdown("**🔗 Attached Links:**")
                
                # Create columns for links to show thumbnails side-by-side
                cols = st.columns(4) 
                
                for i, link in enumerate(links):
                    col = cols[i % 4]
                    with col:
                        url = link['url']
                        platform = link['platform']
                        
                        if platform == 'youtube':
                            yt_id = get_youtube_id(url)
                            if yt_id:
                                img_url = f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg"
                                st.markdown(f"[![YouTube]({img_url})]({url})")
                            else:
                                st.markdown(f"🎥 [YouTube Video]({url})")
                        elif platform == 'instagram':
                            st.markdown(f"📸 [Instagram Post]({url})")
                        else:
                            st.markdown(f"🌐 [Web Link]({url})")
                            
        st.write("") # Spacer between notes

    # Bottom pagination controls
    if total_pages > 1:
        st.markdown("---")
        pcol1, pcol2, pcol3 = st.columns([1, 2, 1])
        with pcol1:
            if st.button("Previous Page", disabled=st.session_state.page <= 1):
                st.session_state.page -= 1
                st.rerun()
        with pcol2:
            st.markdown(f"<div style='text-align: center; padding-top: 5px;'>Page {st.session_state.page} of {total_pages}</div>", unsafe_allow_html=True)
        with pcol3:
            if st.button("Next Page", disabled=st.session_state.page >= total_pages):
                st.session_state.page += 1
                st.rerun()
