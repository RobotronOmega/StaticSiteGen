class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        # tag: string representing the HTML tag name.
        self.tag = tag
        # value: string representing the value of the HTML tag (e.g. text in paragraph)
        self.value = value
        # chldren: list of HTMLNode objects that are children of the node
        self.children = children
        # props: dictionary representing attribute:value
        self.props = props

    def to_html(self):
        raise NotImplementedError("feature not implemented")

    def props_to_html(self):
        htmlcode = ""
        if self.props == None:
            return htmlcode
        for property in self.props:
            htmlcode += f'{property}="{self.props[property]}" '
        return htmlcode[:-1]
    
    def __eq__(self, other):
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True
        return False

    def __repr__(self):
        repr_string = f"HTMLNode( tag:'{self.tag}' value:'{self.value}'"
        if self.children:
            repr_string += " "
            for child in self.children:
                repr_string += f"children:['{child.tag}', '{child.value}'] "
            repr_string = repr_string[:-1]
        if self.props:
            repr_string += f" props:{self.props_to_html()}"
        repr_string += " )"
        return repr_string

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Leaf nodes MUST have a value!")
        if not self.tag:
            return self.value
        htmlcode = f"<{self.tag}"
        if self.props:
            htmlcode += f" {self.props_to_html()}"
        if self.tag == "img":
            htmlcode += " />"
        else:
            htmlcode += f">{self.value}</{self.tag}>"
        return htmlcode
    
class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode requires a tag!")
        if not self.children:
            raise ValueError("ParentNode requires children!")
        # first part of the tag before calling children
        htmlcode = f"<{self.tag}"
        if self.props:
            htmlcode += f" {self.props_to_html()}"
        htmlcode += ">"
        # iterate through the children
        for child in self.children:
            htmlcode += child.to_html()
        # last part of the tag after calling children
        htmlcode += f"</{self.tag}>"
        return htmlcode