import streamlit as st
from few_shot_posts import PostDataset
from post_generator import generate_post
import streamlit.components.v1 as components
import base64
import os

# --- Helper Function to Load External HTML/CSS ---

def load_component_html(post_text, js_safe_text):
    """Loads HTML template, inserts CSS, and substitutes dynamic data."""
    
    html_path = os.path.join("static", "component.html")
    css_path = os.path.join("static", "component.css")
    
    # 1. Load the HTML structure
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            template = f.read()
    except FileNotFoundError:
        return f"<h1>Error: component.html not found at {html_path}</h1>"

    # 2. Load the CSS styles
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            css_styles = f.read()
    except FileNotFoundError:
        return f"<h1>Error: component.css not found at {css_path}</h1>"
    
    # 3. Create a unified, styled component by injecting CSS into a <style> tag
    styled_html = f"""
    <html>
    <head>
        <style>{css_styles}</style>
    </head>
    <body>
        {template}
    </body>
    </html>
    """
    
    # 4. Substitute dynamic variables in the HTML template
    # Removed logo substitution
    final_html = styled_html.replace("{{POST_CONTENT}}", post_text)
    
    # 5. Substitute JavaScript safe content for copy function
    final_html = final_html.replace("{{JS_SAFE_POST_TEXT}}", js_safe_text)

    return final_html

# --- Page Setup ---

# Page config
st.set_page_config(page_title="LinkedIn Post Generator", layout="wide")

# White background
st.markdown(
    """
    <style>
        .main {background-color: #ffffff;}
    </style>
    """,
    unsafe_allow_html=True
)

# Load dataset
fs = PostDataset()
tags = fs.get_tags()

# Options
length_options = ["Short", "Medium", "Long"]

# Multilingual Language Options
language_options = [
    "English", "Spanish", "Mandarin Chinese", "Hindi", "Arabic", 
    "Portuguese", "Bengali", "Russian", "French", "German",
    "Japanese", "Hinglish"
]

# Title
st.markdown("<h1 style='text-align: center; color: #0072b1;'>Creators' AI: Multilingual LinkedIn Post Generator</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Generate Posts in Your Language</h4>", unsafe_allow_html=True)
st.write("---")

# Removed logo loading section

# Two columns layout
col1, col2 = st.columns([1, 2])

# --- Column 1: Input Options ---
with col1:
    st.subheader("Post Options")
    selected_tag = st.selectbox("Topic", options=tags)
    selected_length = st.selectbox("Length", options=length_options)
    selected_language = st.selectbox("Language", options=language_options)

    if st.button("Generate Post"):
        with st.spinner('Generating your LinkedIn post...'):
            post = generate_post(selected_length, selected_language, selected_tag)
            # IMPORTANT: Strip leading/trailing whitespace (like extra newlines)
            st.session_state['generated_post'] = post.strip()

# --- Column 2: Generated Post Display ---
with col2:
    st.subheader("Generated Post")
    post = st.session_state.get("generated_post", None)

    if post:
        # Prepare the post for safe injection into the JavaScript clipboard function
        js_safe = post.replace("`", "\\`").replace("\\", "\\\\")

        # Load and render the external component (removed logo_base64 parameter)
        final_html = load_component_html(post, js_safe)
        
        components.html(final_html, height=450, scrolling=True)