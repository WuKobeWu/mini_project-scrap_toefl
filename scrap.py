import os
import requests
from bs4 import BeautifulSoup

# ==== 1. 基本設定 ====
base_url = "https://toefl.kmf.com/read/ets/new-order/11/0"
save_folder = "C:\code\mini_project\save_toefl\output_texts"

# 建立儲存資料夾
os.makedirs(save_folder, exist_ok=True)

# ==== 2. 爬首頁，找到所有連結 ====
response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'html.parser')

# 找出所有按鈕連結（根據網站結構調整）
link_elements = soup.find_all('a', class_='practice-title js-practice-title')
for link in link_elements:
    print(link.get('href'))

# 提取連結網址
links = [link.get('href') for link in link_elements]
links = links[:1]

# # 如果網址是相對路徑，補上完整網址
full_links = ["https://toefl.kmf.com/" + link for link in links]

print(f"找到 {len(full_links)} 個連結！")

# ==== 3. def the type of class to copy ====
# CLASS_TO_COPY = ["question-title", "section", "options-sn"]
# def get_text_in_page():
#     for class_name in CLASS_TO_COPY:
#         question_elements = soup.find_all(class_=class_name)
#         for element in question_elements:
#             print(element.get_text(strip=True))
#     return 0

def get_article_in_page(soup):
    # 使用 CSS 選擇器選取 class 為 'article-box js-article-box' 的第一個元素
    article_element = soup.select_one("li.article-box.js-article-box")
    if article_element:
        return article_element.get_text(separator="\n", strip=True)

class question_button:
    def __init__(self, soup):
        self.class_q = "question-link"
        self.hrefs = []
        self.current = 0
        self.max_num_of_q = 10
        buttons = soup.find_all("a", class_=self.class_q)
        self.hrefs = [b.get("href") for b in buttons ]
        self.hrefs = self.hrefs[:self.max_num_of_q] 
        for h in self.hrefs:
            print(h)
    def exist_next_question(self):
        if self.current >= self.max_num_of_q:
            return None
        self.current += 1
        return True



def get_question_in_page(soup):
    CLASS_TO_COPY = ["question-title", "section", "normal"]
    texts = []
    for class_name in CLASS_TO_COPY:
        elements = soup.select(f".{class_name}")
        for element in elements:
            text = element.get_text(separator=' ', strip=True)
            texts.append(text)
        texts.append("\n")
    for text in texts:
        print(text)
    return texts



# ==== 3. 逐個進去，抓題目內容 ====
for idx, link in enumerate(full_links, start=1):
    page_resp = requests.get(link)
    page_soup = BeautifulSoup(page_resp.text, 'html.parser')

    # 找到所有題目內容（根據網站結構調整）
    texts = []
    qb = question_button(page_soup)
    texts += get_article_in_page(page_soup)
    while (qb.exist_next_question()):
        texts += f"question {qb.current}"
        texts += get_question_in_page(page_soup)
    print(texts)
    # 儲存成 txt 檔
    save_path = os.path.join(save_folder, f"page_{idx}.txt")
    with open(save_path, 'w', encoding='utf-8') as f:
        for text in texts:
            f.write(text + '\n')

    print(f"第 {idx} 個頁面: {link} 完成")



    # # 把所有題目文字合併
    # questions_text = '\n\n'.join(q.get_text(strip=True) for q in question_elements)

    # # 儲存成 txt 檔
    # save_path = os.path.join(save_folder, f"page_{idx}.txt")
    # with open(save_path, 'w', encoding='utf-8') as f:
    #     f.write(questions_text)

    print(f"第 {idx} 個頁面儲存完成！")

print("✅ 全部完成！")
