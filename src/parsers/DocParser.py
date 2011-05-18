#!/usr/bin/python/

from docx import *
from DocumentParser import DocumentParser
from Domain import Sample
import sys

class DocParser(DocumentParser):
	def parse(self, path):
		try:
			document = opendocx(path)
		except:
			print('Please supply a valid path to document parser.') 
			exit()
          
		paratextlist = getdocumenttext(document)
		newparatextlist = []
		for paratext in paratextlist:
			newparatextlist.append(paratext.encode("utf-8"))
		return Sample(path, None,"\n\n".join(newparatextlist))
