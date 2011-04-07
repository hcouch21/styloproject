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

class Complexity(LinguisticFeature):
    """Calculates the lexical diversity of a sample
    _short_name -- Short name of feature
    _long_name -- Long name of feature
    _description -- Description of feature

    """
    _short_name = "SampleComplexity"
    _long_name = "Sample Complexity"
    _description = "Measures the complexity of the sample."

    def extract(self, sample):
        """ Extract the complexity of the sample
            Defined as (num unique words) / (num words)
        sample -- Sample to analyze

        """
        words = self._get_words(sample)
    
        result = FeatureResult(self._short_name)
        result.value = float(len(set(words))) / float(len(words))

        return [result]
