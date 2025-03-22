import re

from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode

def text_node_to_html_node(text_node): # Converts TextNode objects into HTMLNode ones, specifically LeafNode objects
    match text_node.text_type:
        case TextType.NORMAL_TEXT:
            return LeafNode(value=text_node.text)
        case TextType.BOLD_TEXT:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC_TEXT:
            return LeafNode("i", text_node.text)
        case TextType.CODE_TEXT:
            return LeafNode("code", text_node.text)
        case TextType.LINK_TEXT:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE_TEXT:
            return LeafNode("img", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("invalid text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type): # Takes a list of TextNodes and splits them into more TextNodes based on a delimiter
    new_nodes = []
    current_text_slices = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(node)
            continue
        match delimiter:
            case "**":
                current_text_slices.extend(node.text.split(delimiter))
                for i in range(len(current_text_slices)):
                    if i % 2 == 0 or i == 0:
                        new_nodes.append(TextNode(current_text_slices[i], TextType.NORMAL_TEXT))
                    else:
                        new_nodes.append(TextNode(current_text_slices[i], text_type))
            case ("_"):
                current_text_slices.extend(node.text.split(delimiter))
                for i in range(len(current_text_slices)):
                    if i % 2 == 0 or i == 0:
                        new_nodes.append(TextNode(current_text_slices[i], TextType.NORMAL_TEXT))
                    else:
                        new_nodes.append(TextNode(current_text_slices[i], text_type))
            case "`":
                current_text_slices.extend(node.text.split(delimiter))
                for i in range(len(current_text_slices)):
                    if i % 2 == 0 or i == 0:
                        new_nodes.append(TextNode(current_text_slices[i], TextType.NORMAL_TEXT))
                    else:
                        new_nodes.append(TextNode(current_text_slices[i], text_type))
            case _:
                raise Exception("invalid markdown syntax")
    return new_nodes

def extract_markdown_images(text): # Extracts elements needed to build an image node from a markdown text string. Uses the re module
    extracted_images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted_images

def extract_markdown_links(text): # Like the function above but with links instead of images
    extracted_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted_links