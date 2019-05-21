import os
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
# From PDFInterpreter import both PDFResourceManager and PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
# Import this to raise exception whenever text extraction from PDF is not allowed
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.converter import PDFPageAggregator

import pandas as pd

base_path = "C:\\Users\\Jack.McKew1\\Documents\\Programming Jobs\\Hackathon"

file_list = []

for (dirpath,dirnames,filenames) in os.walk(base_path):
    for name in filenames:
        if name.endswith('.pdf'):
            name = dirpath + "\\" + name
            file_list.append(name)

print(file_list)

my_file = os.path.join(base_path + "/" + "testPDF.pdf")
log_file = os.path.join(base_path + "/" + "pdf_log.txt")



# ALS = ('ES','EB','EM')
# NMI = ('RN')
# MGT = ('-W','-S','VE')
# SGS = ('SE','PR')

# checklist = {'ALS' : ALS, 'NMI': NMI, MGT: 'MGT','SGS':SGS}
# prefix_list = {'AlS': ALS, 'NMI' : NMI, 'SGS':SGS}
# suffix_list = {'MGT':MGT}

def parsePDF(filename):
	global checklist, prefix_list, suffix_list
	password = ""
	extracted_text = ""
	fp = open(filename, "rb")
	parser = PDFParser(fp)
	document = PDFDocument(parser, password)
	if not document.is_extractable:
		raise PDFTextExtractionNotAllowed

	rsrcmgr = PDFResourceManager()

	laparams = LAParams()

	device = PDFPageAggregator(rsrcmgr, laparams=laparams)

	interpreter = PDFPageInterpreter(rsrcmgr, device)


	# def prefix_check(string,num_char,df,page_num):
	# 	for company,strings in prefix_list.items():
	# 		for tag in strings:
	# 			if(tag == string[:num_char]):
	# 				new_row = pd.Series({'Company':company,'Found Text': string,'Page Number':int(page_num),'Filename':filename})
	# 				df = df.append(new_row,ignore_index=True)
	# 	return df


	# def suffix_check(string,num_char,df,page_num):
	# 	for company,strings in suffix_list.items():
	# 		for tag in strings:
	# 			if(tag == string[-num_char:]):
	# 				new_row = pd.Series({'Company':company,'Found Text': string,'Page Number':int(page_num),'Filename':filename})
	# 				df = df.append(new_row,ignore_index=True)
	# 	return df

	findings_df = pd.DataFrame()
	for page_num,page in enumerate(PDFPage.create_pages(document)):
		interpreter.process_page(page)
		layout = device.get_result()
		for lt_obj in layout:
			if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
				lt_list = lt_obj.get_text().split()
                print(lt_list)
				# for company,strings in checklist.items():
				# 	for tag in strings:
				# 		for string in lt_list:
				# 			if tag in string:
				# 				findings_df = prefix_check(string,2,findings_df,page_num)
				# 				findings_df = suffix_check(string,2,findings_df,page_num)
	return findings_df
			
	fp.close()

output_df = pd.DataFrame()
for filename in file_list:
	output_df = output_df.append(parsePDF(filename))
	print(output_df)

# print (extracted_text.encode("utf-8"))
			
# with open(log_file, "w") as my_log:
# 	my_log.write(extracted_text.encode("utf-8"))
# print("Done !!")