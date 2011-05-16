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

class AvgWordsPerParagraph(LinguisticFeature):
    """ Feature that calculates the average number of words per paragraph
        in the sample
    """
    _short_name = "AvgWordsPerParagraph"
    _long_name = "Average Number of Words per Paragraph"
    _description = "Average number of words per paragraph in the sample."

    def extract(self, sample):
        """ Divide the number of words in the sample by the
            number of paragraphs in the sample.
        sample -- Sample to extract from

        """
        paragraphs = [x.strip() for x in sample.plain_text.splitlines()
                        if len(x.strip()) > 0]

        result = FeatureResult(self._short_name)
        result.value = round(float(len(self._get_words(sample))) / \
                             float(len(paragraphs)), 2)

        return [result]

