# My own unit test file for conversion functions

import unittest

from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from conversions import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestConversions(unittest.TestCase):
    def test_delimiter_bold(self):
        nodes = split_nodes_delimiter([TextNode("I'm writing something with **bold** letters", TextType.NORMAL_TEXT)], "**", TextType.BOLD_TEXT)
        self.assertEqual(nodes, [TextNode("I'm writing something with ", TextType.NORMAL_TEXT), TextNode("bold", TextType.BOLD_TEXT), TextNode(" letters", TextType.NORMAL_TEXT)])

    def test_delimiter_italic(self):
        nodes = split_nodes_delimiter([TextNode("Call me the _Tower of Pisa_ the way my text leans on one side", TextType.NORMAL_TEXT)], "_", TextType.ITALIC_TEXT)
        self.assertEqual(nodes, [TextNode("Call me the ", TextType.NORMAL_TEXT), TextNode("Tower of Pisa", TextType.ITALIC_TEXT), TextNode(" the way my text leans on one side", TextType.NORMAL_TEXT)])
    
    def test_delimiter_code(self):
        nodes = split_nodes_delimiter([TextNode("Nerds be like `print(\"Yo Mama\")`", TextType.NORMAL_TEXT)], "`", TextType.CODE_TEXT)
        self.assertEqual(nodes, [TextNode("Nerds be like ", TextType.NORMAL_TEXT), TextNode("print(\"Yo Mama\")", TextType.CODE_TEXT), TextNode("", TextType.NORMAL_TEXT)])
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

if __name__ == "__main__":
    unittest.main()