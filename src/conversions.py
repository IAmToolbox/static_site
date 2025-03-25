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
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(node)
            continue
        current_text_slices = node.text.split(delimiter)
        '''
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
        '''
        for i, slice in enumerate(current_text_slices):
            if i % 2 == 0:
                new_nodes.append(TextNode(slice, TextType.NORMAL_TEXT))
            else:
                new_nodes.append(TextNode(slice, text_type))
    return new_nodes

def split_nodes_image(old_nodes): # Takes a list of TextNodes and splits off the images from them
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(node)
            continue
        text_copy = node.text
        images = extract_markdown_images(node.text)
        if images == []:
            new_nodes.append(node)
            continue
        position = 0
        for alt_text, image_url in images:
            image_markdown = f"![{alt_text}]({image_url})"
            start_index = text_copy.find(image_markdown, position)
            if start_index > position:
                new_nodes.append(TextNode(text_copy[position:start_index], TextType.NORMAL_TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE_TEXT, image_url))
            position = start_index + len(image_markdown)
        if position < len(text_copy):
            new_nodes.append(TextNode(text_copy[position:], TextType.NORMAL_TEXT))
    return new_nodes

def split_nodes_link(old_nodes): # Same as the above function but for links
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(node)
            continue
        text_copy = node.text
        links = extract_markdown_links(node.text)
        if links == []:
            new_nodes.append(node)
            continue
        position = 0
        for link_text, link_url in links:
            link_markdown = f"[{link_text}]({link_url})"
            start_index = text_copy.find(link_markdown, position)
            if start_index > position:
                new_nodes.append(TextNode(text_copy[position:start_index], TextType.NORMAL_TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK_TEXT, link_url))
            position = start_index + len(link_markdown)
        if position < len(text_copy):
            new_nodes.append(TextNode(text_copy[position:], TextType.NORMAL_TEXT))
    return new_nodes

def extract_markdown_images(text): # Extracts elements needed to build an image node from a markdown text string. Uses the re module
    extracted_images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted_images

def extract_markdown_links(text): # Like the function above but with links instead of images
    extracted_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted_links

def text_to_textnode(text): # Uses every function in this file to turn markdown text into usable TextNode objects
    base_node = TextNode(text, TextType.NORMAL_TEXT)
    node_list = [base_node]
    # COMMENCE THE PROCESSING HERE
    node_list = split_nodes_image(node_list)
    node_list = split_nodes_link(node_list)
    node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD_TEXT)
    node_list = split_nodes_delimiter(node_list, "_", TextType.ITALIC_TEXT)
    node_list = split_nodes_delimiter(node_list, "`", TextType.CODE_TEXT)
    return node_list