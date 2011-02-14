#!/usr/bin/python

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

from PluginManager import *
from FeatureFactory import *

import sys

from optparse import OptionParser

class StyloCLI(object):
    def __init__(self):
        p = PluginManager()
        p.load_plugin("FeatureExtractor")
        p.load_plugin("OrangeAdaptor")
    
    def analyze(self):
        pass

    def train(self):
        pass

    def parse_arguments(self, args, options):
        corpus = None
        sample = None

        if options.corpus:
            corpus = options.corpus
        
        if options.list_features:
            # BAD - We need a new hook "ListFeature" and this would go in there
            for feature in FeatureFactory.get_installed_features():
                print FeatureFactory.get_feature(feature).get_long_name()

            sys.exit(0)

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-c", "--corpus", help="Specify a corpus")
    parser.add_option("-f", "--features", help="Specify a list of features to use (semicolon delimited)")
    parser.add_option("-i", "--input", help="Path to input directory or file")
    parser.add_option("-l", "--list-features", action="store_true", help="Lists all available features")

    (options, args) = parser.parse_args()

    cli = StyloCLI()
    cli.parse_arguments(args, options)