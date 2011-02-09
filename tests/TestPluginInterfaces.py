import unittest

import os
import imp

class  PluginInterfacesTestCase(unittest.TestCase):
    #def setUp(self):
    #    self.foo = PluginInterfaces()
    #

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def test_pluginInterfaces(self):
        #assert x != y;
        #self.assertEqual(x, y, "Msg");
        #self.fail("TODO: Write test")

        plugins = os.listdir("src/plugins/")
        plugins.remove("__init__.py")

        for pi_name in plugins:
            mod = imp.load_source(pi_name, "src/plugins/%s/%s.py" % (pi_name, pi_name))
            pi = getattr(mod, pi_name)()

            # Test that each method is implemented that is required by the interface
            #  Can't do that now as we need a corpus to use for tests so just fail
            self.fail(pi.__class__.__bases__)

if __name__ == '__main__':
    unittest.main()

