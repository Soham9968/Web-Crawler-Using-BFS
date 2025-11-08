import requests
from bs4 import BeautifulSoup
from collections import deque

# Function to fetch and parse a webpage
def fetch_page(url):
    try:
        res = requests.get(url, timeout=5)
        return BeautifulSoup(res.text, "html.parser")
    except:
        return None

# Breadth First Search Web Crawler
def bfs_web_crawler(start_url, max_pages=10):
    queue = deque([start_url])       # BFS queue
    visited = set()                  # To avoid revisits
    index = {}                       # Page Index (URL -> Title & Snippet)
    count = 0

    while queue and count < max_pages:
        url = queue.popleft()

        if url in visited:
            continue

        print(f"Crawling: {url}")
        soup = fetch_page(url)
        visited.add(url)

        if not soup:
            print("Failed to fetch page.")
            continue

        # Extract page title
        title = soup.title.string.strip() if soup.title else "No Title"

        # Extract text snippet for indexing
        text = soup.get_text().strip().replace("\n", " ")
        snippet = text[:150] + "..." if len(text) > 150 else text

        # Store in index
        index[url] = {"title": title, "snippet": snippet}

        count += 1

        # Extract and enqueue links
        for link in soup.find_all("a", href=True):
            new_url = link['href']
            if new_url.startswith("http") and new_url not in visited:
                queue.append(new_url)

    return index


# ------------ MAIN PROGRAM ------------
start = input("Enter starting URL (example: https://example.com): ")
maxp = int(input("Enter max pages to crawl: "))

print("\nStarting BFS Web Crawling...\n")
indexed_data = bfs_web_crawler(start, maxp)

print("\n✅ Crawling Completed!")
print("\n📂 Page Index:\n")

for url, data in indexed_data.items():
    print(f"URL: {url}")
    print(f"Title: {data['title']}")
    print(f"Snippet: {data['snippet']}\n")
