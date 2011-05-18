#    This file is part of Stylo.
#
#    Stylo is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Stylo is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Stylo.  If not, see <http://www.gnu.org/licenses/>.

import os.path
import sys
import codecs

from DocumentParser import DocumentParser 
from Domain import Sample

class PlainTextParser(DocumentParser):
	def parse(self, path):
                # Directory
                if os.path.isdir(path):
			raise NotImplementedError()
                # File
                else:
        		with open(path, "r") as f:
            			sample = Sample(path, None, (f.read().decode('latin-1')).encode('utf-8'))
				return sample
