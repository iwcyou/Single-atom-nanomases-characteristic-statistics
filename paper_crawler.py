import requests
from bs4 import BeautifulSoup
import csv
import time

# 输入你的搜索关键词
search_query = "machine learning"
google_scholar_url = "https://scholar.google.com/scholar"

# 模拟浏览器的请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

def get_scholar_results(query, num_pages=1):
    results = []
    for page in range(num_pages):
        params = {
            "q": query,
            "start": page * 10
        }
        response = requests.get(google_scholar_url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Failed to fetch page {page + 1}. Status code: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select(".gs_r.gs_or.gs_scl")

        for article in articles:
            title_tag = article.select_one(".gs_rt a")
            title = title_tag.text if title_tag else "No title available"
            link = title_tag["href"] if title_tag else "No link available"
            snippet = article.select_one(".gs_rs").text if article.select_one(".gs_rs") else "No snippet available"
            pdf_link_tag = article.select_one(".gs_or_ggsm a")
            pdf_link = pdf_link_tag["href"] if pdf_link_tag else "No PDF link available"

            results.append({
                "title": title,
                "link": link,
                "snippet": snippet,
                "pdf_link": pdf_link
            })
        time.sleep(2)  # 避免被 Google 封锁
    return results

# 保存结果到 CSV 文件
def save_results_to_csv(results, filename="scholar_results.csv"):
    with open(filename, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "link", "snippet", "pdf_link"])
        writer.writeheader()
        for result in results:
            writer.writerow(result)

if __name__ == "__main__":
    query = search_query
    num_pages = 3  # 定义抓取的页数
    results = get_scholar_results(query, num_pages=num_pages)
    save_results_to_csv(results)
    print(f"Saved {len(results)} results to 'scholar_results.csv'.")
