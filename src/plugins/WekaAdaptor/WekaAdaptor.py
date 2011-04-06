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
import os
import sys

from subprocess import *

from Domain import FeatureResult
from PlugInInterface import *

class WekaAdaptor(PlugIn, ClassifyStart, TrainStart):
    _classify_algorithm = "weka.classifiers.bayes.NaiveBayes"
    _relevance_algorithm = "weka.attributeSelection.ReliefFAttributeEval"
    
    def __init__(self):
        config = ConfigParser.RawConfigParser()
        config.read("plugins/WekaAdaptor/WekaAdaptor.config")
        
        # Maybe use: java -cp <classpath> instead?
        
        # Modify CLASSPATH if needed
        if config.getboolean("Weka",  "append_classpath"):
            if "CLASSPATH" in os.environ.keys():
                os.environ["CLASSPATH"] += config.get("Weka",  "classpath")
            else:
                os.environ["CLASSPATH"] = config.get("Weka",  "classpath")
        
        # Test if we can find Weka
        weka_error = Popen(["java",  "weka.core.SystemInfo"],  stdout=PIPE,  stderr=PIPE).communicate()[1]
        if weka_error:
            print "Could not find Weka, make sure its in your CLASSPATH"
            sys.exit(1)
        
        if config.has_option("Weka",  "classify_algorithm"):
            self._classify_algorithm = config.get("Weka",  "classify_algorithm")
        
        if config.has_option("Weka",  "relevance_algorithm"):
            self._relevance_algorithm = config.get("Weka",  "relevance_algorithm")
    
    def register(self, hooks):
        """Set up callbacks for events we want to know about"""

        hooks[Hooks.CLASSIFYSTART].append(self)
        hooks[Hooks.TRAINSTART].append(self)

    def unregister(self, hooks):
        """Remove us from the list of callbacks"""
        
        hooks[Hooks.CLASSIFYSTART].remove(self)
        hooks[Hooks.TRAINSTART].remove(self)

    def run_classify_start_action(self, state, manager):
        """Called when Stylo is in the classifying stage

        state -- Current state of Stylo
        manager -- Plugin manager (used if we want to fire new events)

        """
        
        # Parse out weights
        weka_results = Popen(["java",  self._relevance_algorithm, "-i", state.corpus.path + "stylo/training-weka.arff", "-c", "first"],  stdout=PIPE).communicate()[0]
        weka_weights = {}
        start_weights = False
        for line in weka_results.split("\n"):
            if start_weights:
                columns = line.split()
                if len(columns) != 3:
                    break
                else:
                    weka_weights[columns[2]] = columns[0]
            else:
                if "ranked attributes" in line.lower():
                    start_weights = True

        # Extract info from samples
        data = ""
        for sample in state.extracted:
            data += "?,"
            for feature_result in sample.feature_results:
                data += "%s," % feature_result.value
                
                # Set weight
                feature_result.weight = weka_weights[feature_result.name]
            
            data = data[:-1]
            data += "\n"
            
        attribute_lines = ""

        for feature_result in state.extracted[0].feature_results:
            attr_type = "numeric"
            
            if type(feature_result.value) == int:
                attr_type = "integer"
            
            attribute_lines += "@attribute %s %s\n" % (feature_result.name,  attr_type)

        # Write info to disk
        with open("classify_data.arff", "w") as f:
            f.write("@relation train_features\n\n")
            
            # Define the author attribute
            f.write("@attribute Author {")
            corpus_authors = ""
            for author in state.corpus.authors:
                corpus_authors += "%s, " % author.name
            
            corpus_authors = corpus_authors[:-2]
            f.write("%s}\n" % corpus_authors)
            
            f.write("%s\n" % attribute_lines)
            f.write("@data\n%s" % data)
            
        weka_results = Popen(["java",  self._classify_algorithm, "-t", state.corpus.path + "stylo/training-weka.arff", "-T", "classify_data.arff", "-c", "first", "-p", "0"],  stdout=PIPE).communicate()[0]
        os.remove("classify_data.arff")

        # Classify each sample
        count = 0
        for example in state.extracted:
            author_result = FeatureResult("Author")
            author_result.value = weka_results.split("\n")[(-3 - count)].split()[2].split(":")[1]
            author_result.weight = weka_results.split("\n")[(-3 - count)].split()[3]
            example.feature_results.insert(0, author_result)
            count += 1

    def run_train_start_action(self, state, manager):
        """Called when Stylo is in the training stage

        state -- Current state of Stylo
        manager -- Plugin manager (used if we want to fire new events)

        """

        # If we're not in a training state exit
        if state.training is None or state.training != True:
            print "Error: Not a training state object"
            sys.exit(1)

        data = ""
        for author in state.corpus.authors:
            state.to_extract = author.samples

            manager.fire_event(Hooks.EXTRACTSTART, state)
            manager.fire_event(Hooks.EXTRACTSTOP, state)

            for sample in state.extracted:
                data += "%s," % author.name
                for feat_res in sample.feature_results:
                    data += "%s," % feat_res.value

                # Strip trailing comma
                data = data[:-1]
                data += "\n"

            attribute_lines = ""

            for feature_result in state.extracted[0].feature_results:
                attr_type = "numeric"
                
                if type(feature_result.value) == int:
                    attr_type = "integer"
                
                attribute_lines += "@attribute %s %s\n" % (feature_result.name,  attr_type)

        with open(state.corpus.path + "stylo/training-weka.arff", "w") as f:
            f.write("@relation orig_features\n\n")
            
            # Define the author attribute
            f.write("@attribute Author {")
            corpus_authors = ""
            for author in state.corpus.authors:
                corpus_authors += "%s, " % author.name
            
            corpus_authors = corpus_authors[:-2]
            f.write("%s}\n" % corpus_authors)
            
            f.write("%s\n" % attribute_lines)
            f.write("@data\n%s" % data)
