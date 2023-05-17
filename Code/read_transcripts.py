from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter # converts pdf to text
from pdfminer.layout import LAParams  # used to set the pdf layout (size, page format etc) information  required for text analysis as a parameter
from pdfminer.pdfpage import PDFPage  # extract the pages from the pdf file
import pdfminer.high_level as pdf_high_level
import pdfminer.layout as pdf_layout
import subprocess
from pdfminer.high_level import extract_pages
import re #regular expression (a sequence of characters that forms a search pattern)-> check whether a string matches a regular expression
from io import StringIO # creates a string buffer (STRING module- in memory-like file like an object)
import os

import try_extracting_prose


##Disable the warnings
import warnings
warnings.filterwarnings('ignore')



def convert_pdf_to_txt(file, old_file_path):
    
    # ## extract the pages from the pdf file:
    # fp = open(old_file_path, 'rb')

    # ## initiate the Interpreter class as a text reader:
    # rsrcmgr = PDFResourceManager()  # initiate the resource manager class
    # retstr = StringIO()       # creates a string buffer
    # laparams = LAParams()     # initiate the layout class
    # device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    
    # interpreter = PDFPageInterpreter(rsrcmgr, device)
    # password = ""
    # maxpages = 0
    # caching = True
    # pagenos=set() # comma separated list of page numbers to parse

    # ##  loop through all the pages running the interpreter:
    # for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
    #     interpreter.process_page(page)  # # receive the object for the page.

    # ## get all the output
    # text = retstr.getvalue()   

    # # tidy things up
    # fp.close()
    # device.close()
    # retstr.close()
    pages = extract_pages(old_file_path)

    text = try_extracting_prose.show_ltitem_hierarchy(pages, '')
    
    return text
#######################################################################################################################################################
path = os.getcwd()
files = os.listdir(path +'\Transcripts')


for file in files:
    print(f'Doing {file} ...')
    name = os.path.splitext(file)[0]
    old_file_path = path+'\\Transcripts\\'+file
    new_file_path = f'Txt_Transcripts'

    complete_name = os.path.join(new_file_path, name + '.txt')
    output_file = open(complete_name, 'w')

    document = convert_pdf_to_txt(file, old_file_path)

    output_file.write(document)
    output_file.close()

print('Done Read')