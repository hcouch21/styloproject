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

import sys

from plugins.FeatureExtractor.FeatureFactory import *
from PlugInInterface import *

class FeatureExtractor(PlugIn, ExtractStart, ListFeatures):
    def register(self, hooks):
        """Set up callbacks for events we want to know about"""

        hooks[Hooks.EXTRACTSTART].append(self)
        hooks[Hooks.LISTFEATURES].append(self)

    def unregister(self, hooks):
        """Remove us from the list of callbacks"""
        
        hooks[Hooks.EXTRACTSTART].remove(self)
        hooks[Hooks.LISTFEATURES].remove(self)
    
    def run_extract_start_action(self, state, manager):
        """Called when Stylo is in the extraction stage

        state -- Current state of Stylo
        manager -- Plugin manager (used if we want to fire new events)

        """

        # If no features specified, use them all
        if state.features_to_extract is None:
            state.features_to_extract = []

            for feature_name in FeatureFactory.get_installed_features():
                state.features_to_extract.append(feature_name)

        state.extracted = []

        while len(state.to_extract) != 0:
            sample = state.to_extract.pop(0)
            sample.feature_results = []
            
            for feature_name in state.features_to_extract:
                manager.fire_event(Hooks.FEATURESTART, state)

                state.current_feature = feature_name
                feature = FeatureFactory.get_feature(feature_name)
                sample.feature_results.extend(feature.extract(sample))

                manager.fire_event(Hooks.FEATURESTOP, state)

            state.extracted.append(sample)

        manager.fire_event(Hooks.EXTRACTSTOP, state)

    def run_list_features_action(self, state, manager):
        """Called when Stylo is in the list feature stage

        state -- Current state of Stylo
        manager -- Plugin manager (used if we want to fire new events)

        """

        for name in FeatureFactory.get_installed_features():
            feature = FeatureFactory.get_feature(name)
            print feature.get_long_name() + " (" \
		+ feature.get_short_name() + ")"
