from fpdf import FPDF
import os

in_dir = "C:\code\mini_project\save_toefl\output_texts"  # 請替換為您的目錄路徑
out_dir = "C:\code\mini_project\save_toefl\output_pdfs"  # 請替換為您的目錄路徑
txt_files = [f for f in os.listdir(in_dir) if f.endswith('.txt')]

from fpdf import FPDF

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_page()
        # 使用支援 Unicode 的字型
        self.add_font('msjh', '', r'C:\Windows\Fonts\msjh.ttc', uni=True)  # 用微軟正黑體
        self.set_font('msjh', '', 14)



def txt_to_pdf(input_path, output_path):
    pdf = PDF()
    with open(input_path, 'r', encoding='utf-8') as file:
        for line in file:
            pdf.cell(0, 10, line.strip(), ln=True)

    pdf.output(output_path)


for text_file in txt_files:
    input_path = os.path.join(in_dir, text_file)
    output_path = os.path.join(out_dir, text_file.replace('.txt', '.pdf'))
    txt_to_pdf(input_path, output_path)

