import os
import win32print
import win32api

# PDF 檔案資料夾
pdf_folder = r"C:\code\mini_project\save_toefl\output_pdfs"

# 找出所有 pdf 檔案
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

selected_pdfs = []
target_tpo = ["5", "6", "7", "8", "9"]
target_passages = ["1", "2"]


for f in pdf_files:
    parts = f.replace('.pdf', '').split('_')
    if len(parts) >= 3:
        tpo_number = parts[1]
        passage_part = parts[3]
        if tpo_number in target_tpo and passage_part in target_passages:
            selected_pdfs.append(f)
print(selected_pdfs)


# 指定印表機（預設印表機就不用設）
printer_name = win32print.GetDefaultPrinter()

# 批次列印
for pdf_file in selected_pdfs:
    full_path = os.path.join(pdf_folder, pdf_file)
    print(f"Printing: {full_path}")
    win32api.ShellExecute(
        0,
        "print",
        full_path,
        None,
        ".",
        0
    )
