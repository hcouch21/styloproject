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

from Domain import FeatureResult
from LinguisticFeature import *

class LexicalDiversity(LinguisticFeature):
    _short_name = "LexicalDiversity"
    _long_name = "Lexical Diversity"
    _description = "Measures the diversity of the words in the sample."

    def extract(self, sample):
        result = FeatureResult(self._short_name)
        
        # (Number of tokens) / (Number of unique tokens)
        result.value = float(len(sample.nltk_text)) / float(len(set(sample.nltk_text)))

        return [result]
