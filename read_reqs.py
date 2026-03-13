import docx
doc = docx.Document('F1_Dashboard_Requirements.docx')
for para in doc.paragraphs:
    print(para.text)
