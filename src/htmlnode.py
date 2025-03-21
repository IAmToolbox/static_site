class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        props_string = ""
        for prop in self.props:
            props_string = f"{props_string} {prop}: {self.props[prop]}"
        return props_string
    
    def __eq__(self, other):
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("node requires value")
        if self.tag == None:
            return str(self.value)
        return f"<{self.tag}>{self.value}</{self.tag}>"

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