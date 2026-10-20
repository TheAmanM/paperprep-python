from operator import contains
from tabnanny import check
from turtle import width
from PyPDF2 import PdfReader, PageObject, PdfWriter

file_name = "5054_s19_qp_11.pdf"

""" def check_pages_theory():
    reader = PdfReader(file_name)
    pageKeys = {}
    questionIndex = 1
    contains_optional = False
    for i in range(reader.getNumPages()):
        if(i == 0):
            continue;
        # print(i + 1, reader.pages[i].extract_text())
        text = reader.pages[i].extract_text().replace('\n', ' ').replace(" ", "")
        contains_optional = text.find("Answer only one of the following two alternatives".replace(" ", "")) != -1 or contains_optional
        analysis = text[len(str(i + 1)):len(str(i + 1)) + 5]
        # print(f"{i + 1}: \"{analysis}\"")
        if(contains_optional != -1):
            if(text.find("EITHER") != -1):
                print(f"Question EITHER begins at page {i + 1}")
                pageKeys["E"] = i + 1
                questionIndex += 1
            elif(text.find("OR") != -1):
                print(f"Question OR begins at page {i + 1}")
                pageKeys["O"] = i + 1
                questionIndex += 1
        if analysis.startswith(str(questionIndex)):
            print(f"Question {questionIndex} begins at page {i + 1}")
            pageKeys[questionIndex] = i + 1
            questionIndex += 1 """

# checkPages()

""" def check_pages_mcq():
    reader = PdfReader(file_name)
    pageOne = reader.pages[1]
    print(f"artBox: {pageOne.artBox}")
    print(f"bleedBox: {pageOne.bleedBox}")
    print(f"cropBox: {pageOne.cropBox}")
    print(f"mediaBox: {pageOne.mediaBox}")
    print(f"trimBox: {pageOne.trimBox}") """

from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator

reader = PdfReader(file_name)
media_box = reader.pages[0].mediaBox
h, w = media_box.height, media_box.width
num_pages = reader.getNumPages()

# blank = PageObject.create_blank_page(None, w, h * num_pages)
writer = PdfWriter()
# writer.add_blank_page(w, h * num_pages)
blank = PageObject().create_blank_page(None, w, h * num_pages)

for i in range(len(reader.pages)):
    page = reader.pages[i]
    x_translation = 0
    y_translation = i * h
    blank.mergeScaledTranslatedPage(page, 1, x_translation, (h * (num_pages - 1)) - y_translation, False)

writer.add_page(blank)

with open("output.pdf", 'r+b') as output_pdf:
    # writer.write(output_pdf)
    # fp = open('output.pdf', 'r+b')
    fp = output_pdf
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pages = PDFPage.get_pages(fp)

    questionCounter = 1

    coords = []
    questions = []

    for page in pages:
        # print('Processing next page...')
        interpreter.process_page(page)
        layout = device.get_result()
        for lobj in layout:
            if isinstance(lobj, LTTextBox):
                x, y, text = lobj.bbox[0], lobj.bbox[3], lobj.get_text()
                if(text.replace("\n", "").find(f"{str(questionCounter)}  ") != -1 and text.replace("\n", "").find("Paper 1") == -1):
                    # print('At %r is text: "%s"' % ((x, y), text.replace("\n", "")[(len(str(questionCounter)) + 2):-1]))
                    questions.append(text.replace("\n", "")[(len(str(questionCounter)) + 2):-1])
                    if(questionCounter == 1):
                        coords.append(x)
                        coords.append(y)
                    else:
                        coords.append(page.mediabox[2] - x)
                        coords.append(y)
                        coords.append(x)
                        coords.append(y)

                    questionCounter += 1
    
    coords.append(media_box[2])
    coords.append(media_box[3])

    print(len(questions))
    print(len(coords))
    for looper in range(len(questions)):
        print(f"{coords[4 * looper]}, {coords[4 * looper + 1]}, {coords[4 * looper + 2]}, {coords[4 * looper + 3]}")
        print(f"{looper + 1}) {questions[looper]}")
        print("")
    


# check_pages_mcq()