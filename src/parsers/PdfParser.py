#!/usr/bin/python

import os
from pdfminer.pdfparser import PDFDocument, PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import sys
from DocumentParser import DocumentParser
from Domain import Sample
import StringIO

class PdfParser(DocumentParser):
    def parse(self, path):
		out = StringIO.StringIO()
		fp = None
        # Directory
		if os.path.isdir(path):
			raise NotImplementedError()
        # File
	       	else:
			fp = file(path)		
		rsrc = PDFResourceManager()
		codec = 'utf-8'
		laparams = LAParams()
		laparams.char_margin = 2.0
		laparams.line_margin = 2.0
		laparams.word_margin = 0.0
		device = TextConverter(rsrc, out, codec=codec, laparams=laparams)
		doc = PDFDocument()
		parser = PDFParser(fp)
		parser.set_document(doc)
		doc.set_parser(parser)
		doc.initialize()
		interpreter = PDFPageInterpreter(rsrc, device)
		for page in doc.get_pages():
			interpreter.process_page(page)
		device.close()
		sample = Sample(path, None, out.getvalue())
		out.close()
		return sample
