import docx
doc = docx.Document('F1_Dashboard_Requirements.docx')
with open('requirements.md', 'w', encoding='utf-8') as f:
    for para in doc.paragraphs:
        f.write(para.text + '\n')
