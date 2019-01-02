import unittest
import jmespand

class RootTests(unittest.TestCase):

    def test_load_single_raw_doc(self):
        d = {"Value": 42, "Hello": "World"}
        root = jmespand.create_root(d)
        ret = root._merged()
        self.assertEqual(d, ret)

    def test_load_single_doc_with_meta(self):
        d = {"Value": 42, "Hello": "World"}
        root = jmespand.create_root()
        root.add(d, meta={"test":42})
        ret = root._merged()
        self.assertEqual(d, ret)
        self.assertEqual(42, ret["Value"]._meta["test"])
        self.assertEqual(42, ret["Hello"]._meta["test"])

    def test_load_multi_doc_with_meta(self):
        d = {"Value": 42, "Hello": "World"}
        root = jmespand.create_root()
        root.add(d, meta={"test":42})
        root.add({"Hello": "World"}, meta={"test":43})
        ret = root._merged()
        self.assertEqual(d, ret)
        self.assertEqual(42, ret["Value"]._meta["test"])
        self.assertEqual(43, ret["Hello"]._meta["test"])

    def test_expand_multi_doc_with_meta(self):
        d = {"Value": 42, "Hello": "World"}
        root = jmespand.create_root()
        root.add(d, meta={"test":42})
        root.add({"Hello": "World"}, meta={"test":43})
        ret = root.expanded()
        self.assertEqual(d, ret)
        self.assertEqual(int, type(ret["Value"]))
        self.assertEqual(str, type(ret["Hello"]))

    def test_expand_single_doc(self):
        d = {"Value": 42, "Hello": "{Value}"}
        root = jmespand.create_root(d)
        ret = root.expanded()
        self.assertEqual({"Value": 42, "Hello": '42'}, ret)

    def test_expand_nested(self):
        d = {"Value": "{Hello.World}", "Hello":{"World":42}}
        root = jmespand.create_root(d)
        ret = root.expanded()
        self.assertEqual({"Value": '42', "Hello": {"World":42}}, ret)

    def test_expand_array(self):
        d = {"Value": "{Hello[1]}", "Hello":[42, 43]}
        root = jmespand.create_root(d)
        ret = root.expanded()
        self.assertEqual({"Value": '43', "Hello": [42, 43]}, ret)

    def test_expand_self(self):
        d = {"Value": 42, "Hello": "{Hello}"}
        root = jmespand.create_root(d)
        with self.assertRaises(ValueError): # Expects to throw ValueError when cyclic reference found
            ret = root.expanded()

    def test_expand_cycles(self):
        d = {"Value": "{Hello}", "Hello": "{World}", "World": "{Value}"}
        root = jmespand.create_root(d)
        with self.assertRaises(ValueError): # Expects to throw ValueError when cyclic reference found
            ret = root.expanded()

    def test_expand_undefined(self):
        d = {"Value": "{Hello}"}
        root = jmespand.create_root(d)
        with self.assertRaises(KeyError): # Expects to throw KeyError when not found
            ret = root.expanded()

    def test_expand_with_scope(self):
        d = {"Value": "{X}", "Hello": "{Y}", "World": "{Value}", "Value2": "{Value}", "Test": "{Value2}"}
        root = jmespand.create_root(d)
        parms = {"X": 42, "Y": 43, "Value2": 3}
        ret = root.expanded(parms)
        self.assertEqual({"Value": "42", "Hello": "43", "World": "42", "Value2": "42", "Test": "3"}, ret)
            