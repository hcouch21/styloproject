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

import getpass
import os
import pickle
import sys

from optparse import OptionParser

class StyloCLI(object):
    plugin_manager = None

    def __init__(self):
        self.plugin_manager = PluginManager()
    
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
        
        # Enable/disable plugins specified on the command line
        if options.plugins:
            for plugin_name in options.plugins.split(","):
                if plugin_name.startswith("-"):
                    self.plugin_manager.remove_plugin(plugin_name[1:])
                else:
                    self.plugin_manager.load_plugin(plugin_name)

        # Set up the corpus
        if options.corpus:
            for c in Corpus.get_all_corpora():
                if c.name == options.corpus:
                    state.corpus = c
                    if not state.corpus.uses_encryption:
                        state.corpus.load()
                    elif state.corpus.uses_encryption and state.options.key:
                        state.corpus.load(state.options.key)
                    else:
                        pw = getpass.getpass("Key: ")
                        while len(pw) not in [16,  24,  32]:
                            print "Key must be 16, 24, or 32 characters long"
                            pw = getpass.getpass("Key: ")

                        print "Key accepted"
                        state.options.key = pw
                        state.corpus.load(state.options.key)
                    break

            # If the specified corpus doesn't exist
            if state.corpus is None:
                print >> sys.stderr, "Could not find corpus with name: %s" % \
                                        options.corpus
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
                print >> sys.stderr, "Could not find file or path: %s" % \
                                        options.input

        # Set needed linguistic features
        if options.features is not None:
            pass

        # List features
        if options.list_features:
            self.plugin_manager.fire_event(Events.LISTFEATURES, state)
            
            for feature in state.available_features:
                print feature

            sys.exit(0)
        # Train
        elif options.train:
            state.training = True
            self.plugin_manager.fire_event(Events.TRAINSTART, state)
            self.plugin_manager.fire_event(Events.TRAINSTOP, state)
        # Encrypt
        elif options.encrypt:
            if not state.options.key:
                pw = getpass.getpass("Key: ")
                while len(pw) not in [16,  24,  32]:
                    print "Key must be 16, 24, or 32 characters long"
                    pw = getpass.getpass("Key: ")
                
                print "Key accepted"
                state.options.key = pw
            
            state.corpus.compress()
            state.corpus.encrypt(state.options.key)
            sys.exit(0)
        # Decrypt
        elif options.decrypt:
            sys.exit(0)
        # Classify
        else:
            self.plugin_manager.fire_event(Events.EXTRACTSTART, state)
            self.plugin_manager.fire_event(Events.EXTRACTSTOP, state)
            self.plugin_manager.fire_event(Events.CLASSIFYSTART, state)
            self.plugin_manager.fire_event(Events.CLASSIFYSTOP, state)

            # Output human readable
            if not options.pickle:
                for sample in state.extracted:
                    features = sample.feature_results.keys()
                    features.sort()

                    if not options.output:
                        print "Sample: %s" % sample.name
                        print "================"
                        
                        for feature_result in features:
                            print sample.feature_results[feature_result]
                    else:
                        with open(options.output, "a") as f:
                            f.write("Sample: %s\n" % sample.name)
                            f.write("================\n")
                            
                            for feature_result in features:
                                f.write(str(sample.feature_results[feature_result]))
                                f.write("\n");
            # Output pickled (serialized)
            else:
                feature_results = []
                for sample in state.extracted :
                    feature_results.extend(sample.feature_results.values())

                if not options.output:
                    print pickle.dumps(feature_results)
                else:
                    with open(options.output, "wb") as f:
                        pickle.dump(feature_results, f);
        
        state.corpus.save()

if __name__ == "__main__":
    # Set CWD to location of this script
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    
    parser = OptionParser()
    parser.add_option("-c", "--corpus", help="Specify a corpus")
    parser.add_option("-f", "--features", help="Specify a list of features to use (semicolon delimited)")
    parser.add_option("-i", "--input", help="Path to input directory or file")
    parser.add_option("-l", "--list-features", action="store_true", help="Lists all available features")
    parser.add_option("-t", "--train", action="store_true", help="Train Stylo against specified corpus")
    parser.add_option("-p", "--pickle", action="store_true", help="Output pickled version of the results")
    parser.add_option("-P", "--plugins", help="Specify plugins to enable/disable")
    parser.add_option("-e", "--encrypt", action="store_true", help="Encrypt the specified corpus.")
    parser.add_option("-d", "--decrypt", action="store_true", help="Decrypt the specified corpus.")
    parser.add_option("-k", "--key", help="Key to use for encryption or decryption of corpus.")
    parser.add_option("-o", "--output", help="Specify the file or folder to output to.")

    (options, args) = parser.parse_args()

    cli = StyloCLI()
    cli.parse_arguments(args, options)
