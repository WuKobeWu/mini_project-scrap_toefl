import os
import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString

LINK_HEAD = "https://toefl.kmf.com/"
SAVE_FOLDER = "C:\code\mini_project\save_toefl\write_texts"

def get_links_names(idx):
    # ==== 1. 基本設定 ====
    BASE_URL = f"https://toefl.kmf.com/write/ets/order/{idx}"

    # 建立儲存資料夾
    os.makedirs(SAVE_FOLDER, exist_ok=True)

    # ==== 2. 爬首頁，找到所有連結 ====
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找出所有按鈕連結（根據網站結構調整）
    link_elements = soup.find_all('a', class_='practice-title js-practice-title')

    # 提取連結網址
    links = [link.get('href') for link in link_elements]
    # # 如果網址是相對路徑，補上完整網址
    full_links = [LINK_HEAD + link for link in links]

    names = []
    for link in link_elements:
        name = link.get_text(separator=' ', strip=True).split(" ")
       
        name = name[1] +"_" + name[3]
        print(name)
        names.append(name)
    print(", ".join(names))

    print(f"找到 {len(full_links)} 個連結！")
    return full_links, names




def get_question_in_page(soup):
    CLASS_TO_COPY = ["content-read-main.js-translate-content", "item-article", "content-subject.js-translate-content"]
    texts = []
    for class_name in CLASS_TO_COPY:
        elements = soup.select(f".{class_name}")
        
        for element in elements:
            text = element.get_text(separator=' ', strip=True)
            texts.append(text)
            texts.append("\n")
    # for text in texts:
    #     print(text)
    return texts


# ==== 3. 逐個進去，抓題目內容 ====
if __name__ == "__main__":
    for i in range(11 ,0, -1):
        print(f"this is set number {56-5*i} - {60-5*i}")
        full_links, names = get_links_names(i)
        texts = []
        for link, name in zip(full_links, names):
            tpo = name.split("_")[0]
            passage = name.split("_")[1]
            print(f"tpo {tpo} passage {passage}")

            # 找到所有題目內容（根據網站結構調整）
            page_resp = requests.get(link)
            page_soup = BeautifulSoup(page_resp.text, 'html.parser')
            if passage == "2":
                texts += ["\n"]
            texts += get_question_in_page(page_soup)
            if passage == "2":
                # 儲存成 txt 檔
                save_path = os.path.join(SAVE_FOLDER, f"tpo_{tpo}.txt")
                with open(save_path, 'w', encoding='utf-8') as f:
                    for text in texts:
                        f.write(text)
                texts = []

            

        print("✅ 全部完成！")
