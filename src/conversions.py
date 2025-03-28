import re
from enum import Enum

from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

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

def markdown_to_blocks(markdown): # Turns raw markdown into blocks that can be converted to TextNodes
    split_lines = markdown.split("\n\n")
    stripped_lines = []
    for line in split_lines:
        stripped_lines.append(line.strip())
        if stripped_lines[-1] == "":
            stripped_lines.pop()
    return stripped_lines

def block_to_block_type(block): # Checks what kind of markdown block is the input
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    lines = block.split("\n")

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if is_ordered_list(block):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def is_ordered_list(block): # Helper function used for the above
    lines = block.split("\n")
    expected_number = 1
    for line in lines:
        if not line.startswith(f"{expected_number}. "):
            return False
        expected_number += 1
    return True

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent = ParentNode("div", [])
    for block in blocks:
        type = block_to_block_type(block)
        match type:
            case BlockType.PARAGRAPH:
                p_node = ParentNode("p", [])
                text_nodes = text_to_textnode(block)
                html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
                p_node.children = html_nodes
                parent.children.append(p_node)
            case BlockType.HEADING:
                head_amount = block.count("#", 0, 6)
                h_node = ParentNode(f"h{head_amount}", [])
                heading_content = block.lstrip("#").lstrip()
                text_nodes = text_to_textnode(heading_content)
                html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
                h_node.children = html_nodes
                parent.children.append(h_node)
            case BlockType.CODE:
                pre_node = ParentNode("pre", [])
                lines = block.strip().split("\n")
                code_content = block
                if lines[0].startswith("```") and lines[-1].startswith("```"):
                    code_lines = lines[1:-1]
                    code_content = "\n".join(code_lines)
                c_text_node = TextNode(code_content, TextType.CODE_TEXT)
                c_node = text_node_to_html_node(c_text_node)
                pre_node.children = [c_node]
                parent.children.append(pre_node)
            case BlockType.QUOTE:
                q_node = ParentNode("blockquote", [])
                text_nodes = text_to_textnode(block)
                html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
                q_node.children = html_nodes
                parent.children.append(q_node)
            case BlockType.UNORDERED_LIST:
                ul_node = ParentNode("ul", [])
                list_items = [item.strip()[2:] for item in block.split("\n") if item.strip().startswith("- ")]
                for item in list_items:
                    li_node = ParentNode("li", [])
                    text_nodes = text_to_textnode(item)
                    html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
                    li_node.children = html_nodes
                    ul_node.children.append(li_node)
                parent.children.append(ul_node)
            case BlockType.ORDERED_LIST:
                ol_node = ParentNode("ol", [])
                list_items = []
                for item in block.split("\n"):
                    match = re.match(r'^\s*\d+\.\s+(.*)', item)
                    if match:
                        list_items.append(match.group(1))
                for item in list_items:
                    li_node = ParentNode("li", [])
                    text_nodes = text_to_textnode(item)
                    html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
                    li_node.children = html_nodes
                    ol_node.children.append(li_node)
                parent.children.append(ol_node)
    return parent
