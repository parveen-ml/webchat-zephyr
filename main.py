from scraper import fetch_website_content
from model_interface import query_model

def main():
    print("🔗 Enter a website URL to scrape:")
    url = input("> ")

    print("\n⏳ Scraping website...")
    site_text = fetch_website_content(url)

    if not site_text or site_text.startswith("Error"):
        print(site_text)
        return

    print("\n✅ Website content loaded. Start chatting!\n(Type 'exit' to quit)\n")

    while True:
        user_input = input("🧑 You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        
        prompt = (
            f"Using the information below, answer the user's question briefly in 1-2 lines.\n\n"
            f"Website Content:\n{site_text[:1500]}\n\n"
            f"User Question: {user_input}\n"
            f"Answer:"
        )

        response = query_model(prompt)
        print(f"🤖 Bot: {response.strip()}\n")

if __name__ == "__main__":
    main()
