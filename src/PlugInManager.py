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

import imp
import sys

from PlugInInterface import *

class PluginManager(object):
    _plug_ins = {}
    _events = {
        "StyloStart" : [],
        "StyloStop" : [],

        "ExtractStart" : [],
        "ExtractStop" : [],

        "FeatureStart" : [],
        "FeatureStop" : [],

        "ClassifyStart" : [],
        "ClassifyStop" : [],

        "TrainStart" : [],
        "TrainStop" : [],

        "ListFeatures" : [],
    }
    
    def __init__(self):
        self.load_plugins()
    
    def load_plugin(self, name):
        """Loads a plugin and registers it with a call to register

        name -- Name of the plugin to load (module name as well as class name)

        """
        
        # Check if plugin already loaded
        if name in self._plug_ins.keys():
            return

        mod = None

        try:
            mod = imp.load_source(name, "plugins/%s/%s.py" % (name, name))
            pi = getattr(mod, name)()
            pi.register(self._events)
            self._plug_ins[name] = pi
        # Couldn't load the plugin, probably because of import error
        except Exception as e:
            print >> sys.stderr, "Failed to load plugin %s." % name
            print >> sys.stderr, e

    def load_plugins(self):
        try:
            with open("enabled_plugins",  "r") as f:
                for line in f:
                    self.load_plugin(line.strip())
        # File doesn't exist, we have to create it
        except IOError:
            self.load_plugin("ConsoleNotifier")
            self.load_plugin("FeatureExtractor")
            self.load_plugin("WekaAdaptor")
            
            with open("enabled_plugins",  "w") as f:
                f.write("ConsoleNotifier\n")
                f.write("FeatureExtractor\n")
                f.write("WekaAdaptor\n")

    def remove_plugin(self, plugin):
        """Removes the specified plugin from callback list

        plugin -- Plugin object to remove

        """
        
        pi = None
        if plugin in self._plug_ins.keys():
            pi = self._plug_ins[plugin]
        
        if pi is not None:
            pi.unregister(self._events)
            del self._plug_ins[plugin]
            del pi

    def fire_event(self, event, state):
        """Fires the given event for each plugin which needs it

        event -- The event to fire
        state -- RunState object about the current state of Stylo

        """
        for plugin in self._events[event]:
            event_action = getattr(plugin, Events.functions[event])
            event_action(state, self)

    def __str__(self):
        rVal = ""

        for k in self._events.keys():
            rVal += "%s:\n" % k

            count = 0
            for p in self._events[k]:
                rVal += "%d) %s\n" % (count, p.__class__.__name__)

            rVal += "\n"

        return rVal
