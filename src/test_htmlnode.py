# My own unit test file for HTML nodes

import unittest

from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from conversions import text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_eq_simple(self):
        node = HTMLNode("h1", "I'm a header")
        node2 = HTMLNode("h1", "I'm a header")
        self.assertEqual(node, node2)
    
    def test_eq_complicated(self):
        node = HTMLNode("p", "I'm a block of text", None, {"href": "https://docs.python.org/3/library/unittest.html"})
        node2 = HTMLNode("p", "I'm a block of text", None, {"href": "https://docs.python.org/3/library/unittest.html"})
        self.assertEqual(node, node2)
    
    def test_different(self):
        node = HTMLNode("h1", "I'm also a header")
        node2 = HTMLNode("p", "I'm not so ...yeah")
        self.assertNotEqual(node, node2)
    
    def test_leaf_eq(self):
        node = LeafNode("p", "I'm a leaf node")
        node2 = LeafNode("p", "I'm a leaf node")
        self.assertEqual(node, node2)
    
    def test_leaf_no_value(self):
        node = LeafNode("p")
        self.assertRaises(ValueError)
    
    def test_leaf_to_html(self):
        node = LeafNode("p", "I love being a paragraph of text")
        self.assertEqual(node.to_html(), "<p>I love being a paragraph of text</p>")
    
    def test_leaf_no_tag(self):
        node = LeafNode(value="I'm raw text data")
        self.assertEqual(node.to_html(), "I'm raw text data")
    
    def test_parent_eq(self):
        node = ParentNode("h1", [LeafNode("p", "I have a parent")])
        node2 = ParentNode("h1", [LeafNode("p", "I have a parent")])
        self.assertEqual(node, node2)
    
    def test_to_html_with_children(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_with_grandchildren(self):
        grandchild = LeafNode("b", "grandchild")
        child = ParentNode("span", [grandchild])
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><span><b>grandchild</b></span></div>")
    
    def test_parent_no_children(self):
        node = ParentNode("p")
        self.assertRaises(ValueError)
    
    def test_parent_no_tag(self):
        node = ParentNode(children=[LeafNode("p", "My parent has no tag...")])
        self.assertRaises(ValueError)
    
    def test_basic_conversion(self):
        node = TextNode("I'm a text node", TextType.NORMAL_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "I'm a text node")

if __name__ == "__main__":
    unittest.main()