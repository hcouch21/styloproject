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
#    along with Stylo.  If not, see <http://www.gnu.org/licenses

try:
    import Crypto
except:
    print "PyCrypto not installed, corpus encryption is not available"

def Corpus(object):
    """Stores data about a corpus"""

    name = None
    authors = None
    uses_encryption = False
    path = None
    
    def __init__(self, path):
        pass

    def load(self, path, password):
        pass

    def save(self, password):
        pass

    def _encrypt(self, password):
        pass

    def _decrypt(self, password):
        pass

def Sample(object):
    """Stores data and state of a sample document"""

    feature_results = None

def FeatureResult(object):
    """Stores the value after a linguistic feature is extracted
    name -- The name of the feature this result belongs to
    value -- The actual extracted value
    weight -- The weight of the feature in authorship prediction

    """

    name = None
    value = None
    weight = None

    def __init__(self, name):
        """Creates a feature result

        name -- Name of the feature this result belongs to
        """
        
        self.name = name