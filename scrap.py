import os
import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString

LINK_HEAD = "https://toefl.kmf.com/"
SAVE_FOLDER = "C:\code\mini_project\save_toefl\output_texts"

def get_links(idx):
    # ==== 1. 基本設定 ====
    BASE_URL = f"https://toefl.kmf.com/read/ets/new-order/{idx}/0"

    # 建立儲存資料夾
    os.makedirs(SAVE_FOLDER, exist_ok=True)

    # ==== 2. 爬首頁，找到所有連結 ====
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找出所有按鈕連結（根據網站結構調整）
    link_elements = soup.find_all('a', class_='practice-title js-practice-title')
    for link in link_elements:
        print(link.get('href'))

    # 提取連結網址
    links = [link.get('href') for link in link_elements]
    # links = links[:1]

    # # 如果網址是相對路徑，補上完整網址
    full_links = [LINK_HEAD + link for link in links]

    print(f"找到 {len(full_links)} 個連結！")
    return full_links


def get_article_in_page(soup):
    # 使用 CSS 選擇器選取 class 為 'article-box js-article-box' 的第一個元素
    article_element = soup.select_one("li.article-box.js-article-box")
    if article_element:
        # print(article_element.get_text(separator=" ", strip=True))
        return [article_element.get_text(separator=" ", strip=True)]

class question_button:
    def __init__(self, link):
        self.class_q = "question-link"
        self.hrefs = []
        self.current = 0
        self.max_num_of_q = 10
        self.href = link
        page_resp = requests.get(self.href)
        self.page_soup = BeautifulSoup(page_resp.text, 'html.parser')
        buttons = self.page_soup.find_all( class_=self.class_q)
        self.hrefs = [b.get("href") for b in buttons ]
        self.hrefs = self.hrefs[:self.max_num_of_q] 

    def exist_next_question(self):
        if self.current >= self.max_num_of_q:
            return None
        self.href = LINK_HEAD + self.hrefs[self.current]
        print(f"link {self.current+1}:", self.href)
        page_resp = requests.get(self.href)
        self.page_soup = BeautifulSoup(page_resp.text, 'html.parser')
        self.current += 1
        return True



def get_question_in_page(soup):
    CLASS_TO_COPY = ["question-title", "normal", "insert-article"]
    BOX_ARTICLE = "article-box js-article-box"
    texts = []
    for class_name in CLASS_TO_COPY:
        elements = soup.select(f".{class_name}")
        
        for element in elements:
            text = element.get_text(separator=' ', strip=True)
            texts.append(text)
        if class_name == "insert-article" and elements:
            for i_tag in soup.find_all('i', class_='insert-button js-insert-button js-mocks-scroll'):
                i_tag.replace_with(NavigableString('[]'))
            element_article_box = soup.select_one("li.article-box.js-article-box")
            text = element_article_box.get_text(separator=' ', strip=True)
            texts.append(text)
    texts.append("\n")
    # for text in texts:
    #     print(text)
    return texts

def txt_to_pdf():
    pass

# ==== 3. 逐個進去，抓題目內容 ====
if __name__ == "__main__":
    for i in range(11,0, -1):
        print(f"this is set number {56-5*i} - {60-5*i}")
        full_links = get_links(i)
        for idx, link in enumerate(full_links, start=1):
            tpo = 60-5*i - (idx-1) // 3
            passage = (idx-1) % 3 + 1
            print(f"tpo {tpo} passage {passage}")

            # 找到所有題目內容（根據網站結構調整）
            texts = []
            qb = question_button(link)
            texts += get_article_in_page(qb.page_soup)
            while (qb.exist_next_question()):
                texts += [f"question {qb.current}"]
                texts += get_question_in_page(qb.page_soup)
            # 儲存成 txt 檔
            save_path = os.path.join(SAVE_FOLDER, f"tpo_{tpo}_passage_{passage}.txt")
            with open(save_path, 'w', encoding='utf-8') as f:
                for text in texts:
                    f.write(text + '\n')

            print(f"第 {idx} 個頁面: {link} 完成")

        print("✅ 全部完成！")
