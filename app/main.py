import streamlit as st
import os
import sys
import re

# Ensure the database package can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DBManager

st.set_page_config(page_title="PAKRS - Personal AI Knowledge Retrieval System", layout="wide", page_icon="🧠")

@st.cache_resource
def get_db():
    return DBManager()

db = get_db()

def get_youtube_id(url):
    """Extract YouTube video ID from URL."""
    match = re.search(r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})', url)
    return match.group(1) if match else None

st.title("🧠 PAKRS")
st.markdown("### Personal AI Knowledge Retrieval System")
st.markdown("---")

# Search Bar
search_query = st.text_input("🔍 Search your notes", placeholder="e.g. transformers, recipe, interior design...")

if search_query:
    results = db.search_notes(search_query)
    
    if len(results) == 0:
        st.warning("No results found. Try using fewer or different keywords.")
    else:
        st.success(f"Found {len(results)} results")
        
        for row in results:
            with st.container(border=True):
                st.subheader(f"📄 {row['title'] or 'Untitled Note'}")
                
                # Show labels if they exist
                if row['labels']:
                    tags_html = " ".join([f"<span style='background-color: #4f4f4f; color: white; padding: 2px 8px; border-radius: 10px; font-size: 12px; margin-right: 5px;'>{tag}</span>" for tag in row['labels'].split(',')])
                    st.markdown(tags_html, unsafe_allow_html=True)
                    st.write("") # padding
                
                # Show the body
                if row['body']:
                    st.markdown(f"<div style='font-size: 14px; color: #d0d0d0;'>{row['body']}</div>", unsafe_allow_html=True)
                else:
                    st.caption("No text content.")
                    
                # Fetch links for this note
                links = db.get_links_for_note(row['id'])
                if links:
                    st.write("")
                    st.markdown("**🔗 Attached Links:**")
                    
                    # Create columns for links to show thumbnails side-by-side
                    cols = st.columns(min(len(links), 4)) 
                    
                    for i, link in enumerate(links):
                        col = cols[i % 4]
                        with col:
                            url = link['url']
                            platform = link['platform']
                            
                            if platform == 'youtube':
                                yt_id = get_youtube_id(url)
                                if yt_id:
                                    img_url = f"https://img.youtube.com/vi/{yt_id}/mqdefault.jpg"
                                    st.markdown(f"[![YouTube Thumbnail]({img_url})]({url})")
                                else:
                                    st.markdown(f"🎥 [YouTube Video]({url})")
                            elif platform == 'instagram':
                                ig_img = "https://placehold.co/320x180/E1306C/FFFFFF?text=Instagram+Post&font=Montserrat"
                                st.markdown(f"[![Instagram Thumbnail]({ig_img})]({url})")
                            else:
                                web_img = "https://placehold.co/320x180/4f4f4f/FFFFFF?text=Web+Link&font=Montserrat"
                                st.markdown(f"[![Web Thumbnail]({web_img})]({url})")
            st.write("") # Spacer between notes
else:
    # If no search, show stats
    with db.get_connection() as conn:
        cursor = conn.cursor()
        note_count = cursor.execute("SELECT count(*) FROM notes").fetchone()[0]
        link_count = cursor.execute("SELECT count(*) FROM links").fetchone()[0]
    
    st.info(f"Database currently holds **{note_count} notes** and **{link_count} links**.")
    st.write("Enter a keyword above to start searching!")
