# My own unit test file for text nodes

import unittest

from textnode import TextType, TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)
    
    def test_difference(self):
        node = TextNode("I'm Dummy", TextType.NORMAL_TEXT)
        node2 = TextNode("I'm Fletcher Kane", TextType.NORMAL_TEXT)
        self.assertNotEqual(node, node2)
    
    def test_eq_has_url(self):
        node = TextNode("I have a link", TextType.LINK_TEXT, "https://www.boot.dev/lessons/0abc7ce4-3855-4624-9f2d-7e566690fee1")
        node2 = TextNode("I have a link", TextType.LINK_TEXT, "https://www.boot.dev/lessons/0abc7ce4-3855-4624-9f2d-7e566690fee1")
        self.assertEqual(node, node2)
    
    def test_difference_url(self):
        node = TextNode("I definitely have a link trust me", TextType.LINK_TEXT)
        node2 = TextNode("I definitely have a link trust me", TextType.LINK_TEXT, "https://docs.python.org/3/reference/datamodel.html#object.__eq__")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()