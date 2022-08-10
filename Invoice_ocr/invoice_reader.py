import pdfplumber



def get_text(source_document):
    l = []
    txt_l = []
    invoice_lines = []
    txt =""
    with pdfplumber.open(source_document) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            # table = page.extract_table()
            # tables = page.extract_tables()
            # words = page.extract_words()
            # print(words)
            # for i in words:
            #     l.append(i["text"])
            # l.extend(words)
            txt_l.extend(text.splitlines())
            # print(text.)
            # print(table)
            # print(tables)
            # print(words)

       
        
        for text_line in txt_l:
            if text_line[0]!="(":
                invoice_lines.append(text_line)

        

        for lines in invoice_lines:
            txt=txt+lines+"\n"

        

    return txt

        

