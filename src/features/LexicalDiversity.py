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
    """Calculates the lexical diversity of a sample
    _short_name -- Short name of feature
    _long_name -- Long name of feature
    _description -- Description of feature

    """
    _short_name = "LexicalDiversity"
    _long_name = "Lexical Diversity"
    _description = "Measures the diversity of the words in the sample."

    def extract(self, sample):
        """ Extract the lexical diversity of the sample
            Defined as 1 - ( sum(n * (n-1)) / (N * (N*1)) )
        sample -- Sample to analyze

        """
        result = FeatureResult(self._short_name)
    
        words = self._get_words(sample)
    
        unique_words = set(words)
        num_words = len(words)
        word_accum = 0

        # calculate sum(n * (n-1))
        for word in unique_words :
            word_freq = len([ i for i in words if i == word ])
            word_accum += word_freq * (word_freq - 1)

        result.value = 1 - (float(word_accum) / float((num_words * 
                                                (num_words - 1))))

        return [result]
