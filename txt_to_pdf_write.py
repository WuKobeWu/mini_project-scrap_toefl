from fpdf import FPDF
import os

in_dir = r"C:\code\mini_project\save_toefl\write_texts"  # 請替換為您的目錄路徑
out_dir = r"C:\code\mini_project\save_toefl\write_pdfs"  # 請替換為您的目錄路徑
txt_files = [f for f in os.listdir(in_dir) if f.endswith('.txt')]

from fpdf import FPDF

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_page()
        # 使用支援 Unicode 的字型
        self.add_font('msjh', '', r'C:\Windows\Fonts\msjh.ttc')
        self.set_font('msjh', '', 14)


def txt_to_pdf(input_path, output_path):
    pdf = PDF()
    filename = os.path.basename(input_path)
    title = filename.replace('.txt', '')
    # 加上標題（大字體 + 置中）
    pdf.set_font('msjh', '', 18)
    pdf.cell(0, 10, title, ln=True, align='C')

    # 換回正文用的字體
    pdf.set_font('msjh', '', 14)

    # 加上間隔
    pdf.ln(5)

    with open(input_path, 'r', encoding='utf-8') as file:
        for line in file:
            pdf.multi_cell(0, 5, line, align='L')


    pdf.output(output_path)


for text_file in txt_files:
    input_path = os.path.join(in_dir, text_file)
    output_path = os.path.join(out_dir, text_file.replace('.txt', '.pdf'))
    txt_to_pdf(input_path, output_path)

