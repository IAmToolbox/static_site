# My own unit test file for conversion functions

import unittest

from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from conversions import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnode

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
    
    def test_delimiter_nothing(self):
        nodes = split_nodes_delimiter([TextNode("I'm actually a normal text block", TextType.NORMAL_TEXT)], "**", TextType.BOLD_TEXT)
        self.assertEqual(nodes, [TextNode("I'm actually a normal text block", TextType.NORMAL_TEXT)])
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
    
    def test_no_link(self):
        matches = extract_markdown_links("I actually don't have any links...")
        self.assertEqual([], matches)
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.NORMAL_TEXT),
            TextNode("image", TextType.IMAGE_TEXT, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.NORMAL_TEXT),
            TextNode(
                "second image", TextType.IMAGE_TEXT, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("This is text with a link ", TextType.NORMAL_TEXT),
            TextNode("to boot dev", TextType.LINK_TEXT, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL_TEXT),
            TextNode(
                "to youtube", TextType.LINK_TEXT, "https://www.youtube.com/@bootdotdev"
            ),
        ],
        new_nodes,
        )
    
    def test_text_processing(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnode(text)
        self.assertListEqual(
        [
        TextNode("This is ", TextType.NORMAL_TEXT),
        TextNode("text", TextType.BOLD_TEXT),
        TextNode(" with an ", TextType.NORMAL_TEXT),
        TextNode("italic", TextType.ITALIC_TEXT),
        TextNode(" word and a ", TextType.NORMAL_TEXT),
        TextNode("code block", TextType.CODE_TEXT),
        TextNode(" and an ", TextType.NORMAL_TEXT),
        TextNode("obi wan image", TextType.IMAGE_TEXT, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.NORMAL_TEXT),
        TextNode("link", TextType.LINK_TEXT, "https://boot.dev"),
        ],
        nodes,
        )

if __name__ == "__main__":
    unittest.main()