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
import codecs

from subprocess import *

from cStringIO import StringIO

from Domain import FeatureResult
from PlugInInterface import *

class WekaAdaptor(PlugIn, ClassifyStart, TrainStart):
    """Adapter for the WEKA machine learning tool"""
    dependencies = None
    conflicts = None
    needs_vanilla_data = False
    modifies_data = False
    category = Categories.MACHINELEARNING
    
    _classify_algorithm = "weka.classifiers.bayes.NaiveBayes"
    _relevance_algorithm = "weka.attributeSelection.ReliefFAttributeEval"

    _train_header_prefix = "% stylo_features "
    
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
    
    def register(self, events):
        """Set up callbacks for events we want to know about"""

        events[Events.CLASSIFYSTART].append(self)
        events[Events.TRAINSTART].append(self)

    def unregister(self, events):
        """Remove us from the list of callbacks"""
        
        events[Events.CLASSIFYSTART].remove(self)
        events[Events.TRAINSTART].remove(self)

    def run_classify_start_action(self, state, manager):
        """Called when Stylo is in the classifying stage

        state -- Current state of Stylo
        manager -- Plugin manager (used if we want to fire new events)

        """

        # Verify that the same features are being used as when training
        with codecs.open(state.corpus.path + "stylo/training-weka.arff", "r", "utf-8") as f:
            # Read the first line
            comment = f.readline()[:-1]

            reject = False

            # Make sure it's a comment
            if not comment.startswith(self._train_header_prefix) :
                reject = True
            else :
                # Make sure the feature sets match
                current_features = state.features_to_extract
                current_features.sort()

                trained_features = (comment.split(" ")[2]).split(",")
                trained_features.sort()

                if len(current_features) != len(trained_features) :
                    reject = True
                else :
                    # Linear search to check feature equality
                    for i in range(len(current_features)) :
                        if current_features[i] != trained_features[i] :
                            reject = True
                            break

            # If the train file is not valid, throw an error and exit
            if reject :
                print "Error: Training file is not a valid Stylo training " + \
                        "file.\n       Please run Stylo training again or " + \
                        "classify using\n       the same feature set as " + \
                        "training set."
                sys.exit(1)
       
        # Parse out weights
        weka_results = Popen(["java", "-Dfile.encoding=utf-8", 
                            self._relevance_algorithm, "-i",
                            state.corpus.path + "stylo/training-weka.arff",
                            "-c", "first"],  stdout=PIPE).communicate()[0]
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

        # Use the list of features with weka weights as the full feature list
        sorted_feature_list = weka_weights.keys()
        sorted_feature_list.sort()

        # Extract info from samples
        data = ""
        for sample in state.extracted:
            data += "?,"

            # Sort list of feature results, and get count here so
            # we aren't continually calling len()
            feature_result_keys = sample.feature_results.keys()
            feature_result_keys.sort()
            num_result_keys = len(feature_result_keys)

            list_idx = 0
            feat_idx = 0
            
            # Loop through full list of featurs
            while list_idx < len(sorted_feature_list) :
                # If we're within the feature list of the sample..
                if feat_idx < num_result_keys :
                    sample_feature = feature_result_keys[feat_idx]
                    sorted_feature = sorted_feature_list[list_idx]

                    # If the two features are the same, then this sample
                    # includes this feature, so add it to the list
                    if sample_feature == sorted_feature :
                        feature = sample.feature_results[sample_feature]

                        data += "%s," % feature.value
                        list_idx += 1
                        feat_idx += 1

                        # Set weight
                        feature.weight = weka_weights[sample_feature]
                    # If sample feature is behind sorted feature alphabetically
                    # then this feature is not in the training set, so just 
                    # give it a weight of 0 and ignore it in the data
                    elif sample_feature < sorted_feature :

                        # Set weight
                        feature = sample.feature_results[sample_feature]
                        feature.weight = 0

                        feat_idx += 1
                    # If the sample feature is ahead of the sorted feature
                    # then this feature is not in the sample, so give it
                    # a value of 0 and move on
                    else :
                        data += "0,"
                        list_idx += 1
                # If we are past all features in the sample but are still not
                # at the end of the full feature list, just keep padding 0s
                else :
                    data += "0,"
                    list_idx += 1

            data = data[:-1]
            data += "\n"

        # Write attributes
        attribute_lines = ""
        for result in sorted_feature_list :
            attribute_lines += "@attribute \"%s\" numeric\n" % result.replace("\"", "\\\"")

        #attribute_lines = (attribute_lines.decode('latin-1')).encode('utf-8')

        # Write info to disk
        with codecs.open("classify_data.arff", "w", "utf-8") as f:
            f.write("@relation train_features\n\n")
            
            # Define the author attribute
            f.write("@attribute Author {")
            corpus_authors = ""
            for author in state.corpus.authors:
                corpus_authors += "%s, " % author.name
            
            corpus_authors = corpus_authors[:-2]
            f.write("%s}\n" % corpus_authors)
            
            f.write(attribute_lines.decode('utf-8'))
            f.write("\n")
            f.write("@data\n%s" % data)
            
        weka_results = Popen(["java", "-Xmx1g", "-Xms256m",
                          "-Dfile.encoding=utf-8", self._classify_algorithm,
                          "-t", state.corpus.path + "stylo/training-weka.arff",
                          "-T", "classify_data.arff", "-c", "first", "-p",
                          "0"],  stdout=PIPE).communicate()[0]
        
        if not state.options.no_clean:
            os.remove("classify_data.arff")

        # Classify each sample
        count = 0
        for example in state.extracted:
            author_result = FeatureResult("Author")
            author_result.value = weka_results.split("\n")[(-3 - count)].split()[2].split(":")[1]
            author_result.weight = weka_results.split("\n")[(-3 - count)].split()[3]
            example.feature_results["Author"] = author_result
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

        used_features = {}
        extractions = {}
        for author in state.corpus.authors :
            state.to_extract = author.samples

            manager.fire_event(Events.EXTRACTSTART, state)
            manager.fire_event(Events.EXTRACTSTOP, state)

            # Run through the extracted features and keep track of all
            # feature names used
            for sample in state.extracted :
                for name in sample.feature_results.keys() :
                    if name not in used_features :
                        used_features[name] = sample.feature_results[name]

            # Store off the extraction information so we can access it
            # in a second loop
            extractions[author.name] = state.extracted

        # Get a sorted list of all feature names in the corpus
        sorted_feature_list = used_features.keys()
        sorted_feature_list.sort()

        # Need to do optimized construction
        # so that it doesn't take 10 minutes to write the ARFF file
        # like it did when the NGram concatenation was first added..
        data = StringIO()
        for author in state.corpus.authors :
            for sample in extractions[author.name]:
                line = StringIO()
                line.write("%s," % author.name)

                # Get a sorted list feature result names for this sample
                feature_result_keys = sample.feature_results.keys()
                feature_result_keys.sort()
                # Store length of this so we don't have to call len() each time
                num_result_keys = len(feature_result_keys)

                list_idx = 0
                feat_idx = 0

                # Iterate through the full list of features
                while list_idx < len(sorted_feature_list) :
                    # If the two indices are the same, then this sample
                    # contains this feature set, so include its value
                    if feat_idx < num_result_keys and \
                            feature_result_keys[feat_idx] == \
                            sorted_feature_list[list_idx] :
                        line.write("%s," % sample.feature_results[
                                            feature_result_keys[feat_idx]
                                            ].value)
                        list_idx += 1
                        feat_idx += 1
                    # If the two indices are not the same, then this sample
                    # does not contain this feature set, so move on
                    else :
                        line.write("0,");
                        list_idx += 1
                        
                # Strip trailing comma
                data.write(line.getvalue()[:-1])
                data.write("\n")

        attribute_lines = ""

        for result in sorted_feature_list :
            attribute_lines += "@attribute \"%s\" numeric\n" % result.replace("\"", "\\\"")

        attribute_lines = (attribute_lines.decode('latin-1')).encode('utf-8')

        with codecs.open(state.corpus.path + "stylo/training-weka.arff", "w", "utf-8") as f:
            # Write a comment declaring the featureset used
            f.write(self._train_header_prefix);
            f.write("%s\n" % ",".join(state.features_to_extract));

            f.write("@relation orig_features\n\n")
            
            # Define the author attribute
            f.write("@attribute Author {")
            corpus_authors = ""
            for author in state.corpus.authors:
                corpus_authors += "%s, " % author.name
            
            corpus_authors = corpus_authors[:-2]
            f.write("%s}\n" % corpus_authors)
            
            f.write(attribute_lines.decode('utf-8'))
            f.write("\n")

            f.write("@data\n%s" % data.getvalue())
