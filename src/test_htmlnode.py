import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        print("running HTMLNode test 1")
        childnode = HTMLNode("b", "HTML")
        node = HTMLNode("p", "This is an HTML node", [childnode])
        node2 = HTMLNode("p", "This is an HTML node", [childnode])
        self.assertEqual(node, node2)

    def test_eq2(self):
        print("running HTMLNode test 2")
        node1 = HTMLNode("img", None, None, {"src":"https://www.python.org/static/img/python-logo.png", "alt":"This is a slice of grapefruit.",})
        node2 = HTMLNode("img", None, None, {"src":"https://www.python.org/static/img/python-logo.png", "alt":"This is a slice of grapefruit.",})
        self.assertEqual(node1, node2)

    def test_noteq(self):
        print("running HTMLNode test 3")
        node = HTMLNode(None, "This is some text")
        node2 = HTMLNode("p", "This is some text")
        self.assertNotEqual(node, node2)

    def test_eq3(self):
        print("running HTMLNode test 4")
        node2 = HTMLNode("a", "This is a link.", None, {"href":"https://google.com", "target":"_blank"})
        testtext = 'href="https://google.com" target="_blank"'
        self.assertEqual(testtext, node2.props_to_html())

    def test_empty_attribute(self):
        print("running HTMLNode test 5")
        node = HTMLNode("p" "This is some text")
        self.assertIsNone(node.props)

    def test_exception(self):
        print("running HTMLNode test 6")
        node = HTMLNode("p", "This is some text.")
        with self.assertRaises(NotImplementedError):
            node.to_html()
    
    def test_leaf_to_html_p(self):
        print("running LeafNode test 1")
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_exception(self):
        print("running LeafNode test 2")
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_leaf_to_html_a(self):
        print("running LeafNode test 3")
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_a2(self):
        print("running LeafNode test 4")
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com", "target":"_blank",})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">Click me!</a>')

    def test_to_html_with_children(self):
        print("running ParentNode test 1")
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        print("running ParentNode test 2")
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren_props(self):
        print("running ParentNode test 3")
        text_node = LeafNode(None, " text")
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node, text_node], {"id": "testspan"})
        parent_node = ParentNode("div", [child_node])
        
        self.assertEqual(
            parent_node.to_html(),
            '<div><span id="testspan"><b>grandchild</b> text</span></div>',
        )
    
    def test_to_html_with_grandchildren_exception(self):
        print("running ParentNode test 4")
        text_node = LeafNode(None, " text")
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node, text_node], {"id": "testspan"})
        parent_node = ParentNode("div", None)
        
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_grandchildren_nested(self):
        print("running ParentNode test 5")
        text_node = LeafNode(None, " text")
        text_node_2 = LeafNode(None, " text 2")
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node_2 = LeafNode("i", "grandchild 2")
        child_node = ParentNode("span", [grandchild_node, text_node], {"id": "testspan"})
        child_node_2 = ParentNode("span", [grandchild_node_2, text_node_2], {"id":"testspan2"})
        parent_node = ParentNode("div", [child_node, child_node_2])
        
        self.assertEqual(
            parent_node.to_html(),
            '<div><span id="testspan"><b>grandchild</b> text</span><span id="testspan2"><i>grandchild 2</i> text 2</span></div>',
        )


if __name__ == "__main__":
    unittest.main()