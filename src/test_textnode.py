import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        print("running TextNode test 1")
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        print("running TextNode test 2")
        node = TextNode("This is an image link", TextType.IMAGE, "https://www.python.org/static/img/python-logo.png")
        node2 = TextNode("This is an image link", TextType.IMAGE, "https://www.python.org/static/img/python-logo.png")
        self.assertEqual(node, node2)

    def test_noteq(self):
        print("running TextNode test 3")
        node = TextNode("This is some text", TextType.TEXT)
        node2 = TextNode("This is some text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_noteq2(self):
        print("running TextNode test 4")
        node = TextNode("This is a link...?", TextType.LINK)
        node2 = TextNode("This is a link...?", TextType.LINK, "https://google.com")
        self.assertNotEqual(node, node2)

    def test_empty_attribute(self):
        print("running TextNode test 5")
        node = TextNode("This is some text", TextType.TEXT)
        self.assertIsNone(node.url)

    def test_text(self):
        print("running text_node_to_html_node tests")
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a bold text node", TextType.BOLD)
        node3 = TextNode("This is some code", TextType.CODE)
        node4 = TextNode("This one won't work", None)
        node5 = TextNode("This is an image of a grapefruit", TextType.IMAGE, "grapefruit.jpg")
        html_node = text_node_to_html_node(node)
        html_node2 = text_node_to_html_node(node2)
        html_node3 = text_node_to_html_node(node3)
        html_node5 = text_node_to_html_node(node5)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node2.tag, "b")
        self.assertEqual(html_node2.value, "This is a bold text node")
        self.assertEqual(html_node3.tag, "code")
        self.assertEqual(html_node3.value, "This is some code")
        self.assertEqual(html_node5.tag, "img")
        self.assertEqual(html_node5.value, "")
        self.assertEqual(html_node5.props, {"src":"grapefruit.jpg", "alt":"This is an image of a grapefruit",})
        with self.assertRaises(ValueError):
            html_node4 = text_node_to_html_node(node4)


if __name__ == "__main__":
    unittest.main()
