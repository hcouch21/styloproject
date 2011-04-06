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

import ConfigParser

from Domain import FeatureResult
from LinguisticFeature import *

class PctWordGroups(LinguisticFeature):
    _short_name = "PctWordGroups"
    _long_name = "Percent Word Groups"
    _description = "Percentage of words per word group."
    
    _group_words = {}
    
    def __init__(self):
        config = ConfigParser.RawConfigParser()
        # Set options to case sensitive
        config.optionxform = str
        # Config files are named after module
        config.read("features/%s.config" % self._short_name)
        
        for group in config.options("WordGroups"):
            self._group_words[group] = config.get("WordGroups",  group).split(",")

    def extract(self, sample):
        group_counts = {}

        words = [x for x in sample.nltk_text if x.isalnum() and len(x) > 1]
        
        # Loop through all words
        for word in words:
            # Loop through all groups
            for group in self._group_words.keys():
                # If word is part of this group
                if word.lower() in self._group_words[group]:
                    if group in group_counts:
                        group_counts[group] += 1
                    else:
                        group_counts[group] = 1
                    
                    continue
        
        rVals = []
        for group in self._group_words:
            result = FeatureResult("%s%s" % (self._short_name,  group))
            if group in group_counts.keys():
                result.value = float(group_counts[group]) / float(len(words))
            else:
                result.value = 0.0
            
            rVals.append(result)

        return rVals
