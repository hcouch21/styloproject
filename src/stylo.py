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

from Domain import *
from PlugInManager import *
from PlugInInterface import *

import os
import sys

from optparse import OptionParser

class StyloCLI(object):
    plugin_manager = None

    def __init__(self):
        self.plugin_manager = PluginManager()
        self.plugin_manager.load_plugin("ConsoleNotifier")
        self.plugin_manager.load_plugin("FeatureExtractor")
        self.plugin_manager.load_plugin("WekaAdaptor")
    
    def analyze(self):
        pass

    def train(self):
        pass
        
    def parse_arguments(self, args, options):
        """Sets Stylo up based on the command line arguments/options

        args -- Arguments from the command line
        options -- Options from the command line

        """
        state = RunState()
        state.options = options

        # Set up the corpus
        if options.corpus:
            for c in Corpus.get_all_corpora():
                if c.name == options.corpus:
                    state.corpus = c
                    state.corpus.load()
                    break

            # If the specified corpus doesn't exist
            if state.corpus is None:
                print "Could not find corpus with name: %s" % options.corpus
                sys.exit(1)

        # Set up the input file
        if options.input:
            if os.path.exists(options.input):
                # Directory
                if os.path.isdir(options.input):
                    raise NotImplementedError()
                # File
                else:
                    state.to_extract = []
                    state.to_extract.append(Sample(options.input))
            else:
                print "Could not find file or path: %s" % options.input

        # Set needed linguistic features
        if options.features is not None:
            pass

        # List features
        if options.list_features:
            self.plugin_manager.fire_event(Hooks.LISTFEATURES, state)
            
            for feature in state.available_features:
                print feature

            sys.exit(0)
        # Train
        elif options.train:
            state.training = True
            self.plugin_manager.fire_event(Hooks.TRAINSTART, state)
            self.plugin_manager.fire_event(Hooks.TRAINSTOP, state)
        # Classify
        else:
            self.plugin_manager.fire_event(Hooks.EXTRACTSTART, state)
            self.plugin_manager.fire_event(Hooks.EXTRACTSTOP, state)
            self.plugin_manager.fire_event(Hooks.CLASSIFYSTART, state)
            self.plugin_manager.fire_event(Hooks.CLASSIFYSTOP, state)

            # Output human readable
            if not options.pickle:
                for sample in state.extracted:
                    print "Sample: %s" % sample.name
                    print "================"

                    features = sample.feature_results.keys()
                    features.sort()

                    for feature_result in features:
                        print sample.feature_results[feature_result]
            # Output pickled (serialized)
            else:
                raise NotImplementedError()

if __name__ == "__main__":
    # Set CWD to location of this script
    os.chdir(os.path.dirname(__file__))
    
    parser = OptionParser()
    parser.add_option("-c", "--corpus", help="Specify a corpus")
    parser.add_option("-f", "--features", help="Specify a list of features to use (semicolon delimited)")
    parser.add_option("-i", "--input", help="Path to input directory or file")
    parser.add_option("-l", "--list-features", action="store_true", help="Lists all available features")
    parser.add_option("-t", "--train", action="store_true", help="Train Stylo against specified corpus")
    parser.add_option("-p", "--pickle", action="store_true", help="Output pickled version of the results")

    (options, args) = parser.parse_args()

    cli = StyloCLI()
    cli.parse_arguments(args, options)
