import requests
from serpapi import GoogleSearch
import anthropic

def extract_keywords(text, client):
    messages = [
                {"role": "system", "content": "You are an AI assistant that extracts relevant keywords from text and return keywords concisely in csv format"},
                {"role": "user", "content": f"Please extract relevant keywords from the following content:{text}"}
            ]
    response = client.messages.create(
        model="claude-3-opus,sonnet, or haiku",  
        messages=messages,
        max_tokens=100,
    )
    keywords = response["message"]["content"].strip().split(",")
    return [keyword.strip() for keyword in keywords]

def perform_google_search(query, num_results):
    params = {
        "q": query,
        "api_key": "API-KEY",
        "num": num_results,
        "google_domain": "google.com",
        "gl": "us",
        "hl": "en",
        "niche": "lighting"
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    # Process the search results
    for result in results["organic_results"]:
        url = result["link"]
        try:
            response = requests.get(url)
            content = response.text

            # Feed the content to the Claude model using the Messages API
            claude = anthropic.Client(api_key="api key")
          
            response = extract_keywords(content, claude)
            keywords = response
            print(f"URL: {url}")
            print(f"Keywords: {keywords}")
            print("---")
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving content from {url}: {e}")
            print("---")

# Example usage
search_query = "led lighting"
num_results = 5
perform_google_search(search_query, num_results)
