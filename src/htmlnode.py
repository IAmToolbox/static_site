from textnode import TextType, TextNode

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        props_string = ""
        for prop in self.props:
            props_string = f"{props_string} {prop}=\"{self.props[prop]}\""
        return props_string
    
    def __eq__(self, other):
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self):
        if self.value == None:
            print(f"Problem node: {self.tag}, props: {self.props}")
            raise ValueError("node requires value")
        if self.tag == None:
            return str(self.value)
        return f"<{self.tag}>{self.value}</{self.tag}>"

class ImageNode(LeafNode):
    def __init__(self, src, alt=""):
        super().__init__("img", None)
        self.props = {"src": src, "alt": alt}
    
    def to_html(self):
        return f"<{self.tag}{self.props_to_html()} />"

class LinkNode(LeafNode):
    def __init__(self, href, text=""):
        super().__init__("a", None)
        self.props = {"href": href, "text": text}
    
    def to_html(self):
        return f"<{self.tag}{self.props_to_html()} />"

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("node requires tag")
        if self.children == None:
            raise ValueError("node requires children")
        children_data = ""
        for node in self.children:
            children_data = f"{children_data}{node.to_html()}"
        return f"<{self.tag}>{children_data}</{self.tag}>"

