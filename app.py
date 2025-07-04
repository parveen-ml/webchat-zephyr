import streamlit as st
from scraper import fetch_website_content
from model_interface import query_model

st.set_page_config(page_title="Web Scraper Chatbot", layout="centered")

st.title("🔎 Website Scraper Chatbot")
st.markdown("Enter a website URL below. The bot will scrape the content and then you can chat about the website.")

# Session states for website content and chat history
if "site_text" not in st.session_state:
    st.session_state.site_text = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input for URL
url = st.text_input("🌐 Enter Website URL:", placeholder="https://example.com")

# Button to scrape content
if st.button("🚀 Scrape Website"):
    with st.spinner("Scraping website..."):
        site_text = fetch_website_content(url)
        if not site_text or site_text.startswith("Error"):
            st.error(site_text)
            st.session_state.site_text = ""
        else:
            st.success("✅ Website scraped! You can now chat.")
            st.session_state.site_text = site_text
            st.session_state.chat_history = []  # Reset chat history when new site is scraped

# Only show chat interface if site is loaded
if st.session_state.site_text:
    st.subheader("💬 Chat with the Website Bot")

    # Input for user message
    user_message = st.text_input("You:", placeholder="Ask something about the website...")

    if user_message:
        # Append user message
        st.session_state.chat_history.append({"role": "user", "content": user_message})

        # Create prompt for model
        prompt = (
            f"Based on the following website content, answer the user's question in 1–2 lines. "
            f"Be helpful even if the question is casual.\n\n"
            f"Website Content:\n{st.session_state.site_text[:1500]}\n\n"
            f"User Question: {user_message}\n"
            f"Answer:"
        )

        with st.spinner("Generating response..."):
            response = query_model(prompt)

        # Append bot response
        st.session_state.chat_history.append({"role": "bot", "content": response.strip()})

    # Display chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"🧑 **You**: {msg['content']}")
        else:
            st.markdown(f"🤖 **Bot**: {msg['content']}")
