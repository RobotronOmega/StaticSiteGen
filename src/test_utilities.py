import unittest

from textnode import TextNode, TextType
from utilities import split_nodes_delimiter, extract_markdown_images, extract_markdown_links


class TestUtilities(unittest.TestCase):
    def test_eq(self):
        print("running Utilities test 1")
        text = TextNode("This text is **very** bold.", TextType.TEXT)
        test_nodes = [
            TextNode("This text is ", TextType.TEXT),
            TextNode("very", TextType.BOLD),
            TextNode(" bold.", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([text], "**", TextType.BOLD), test_nodes)

    def test_eq2(self):
        print("running Utilities test 2")
        text = TextNode("This text is quite _unique_.", TextType.TEXT)
        test_nodes = [
            TextNode("This text is quite ", TextType.TEXT),
            TextNode("unique", TextType.ITALIC),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([text], "_", TextType.ITALIC), test_nodes)

    def test_eq3(self):
        print("running Utilities test 3")
        text = TextNode("`Blocks of code` seem like a real **burden**.", TextType.TEXT)
        test_nodes = [
            TextNode("Blocks of code", TextType.CODE),
            TextNode(" seem like a real **burden**.", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([text], "`", TextType.CODE), test_nodes)

    def test_eq4(self):
        print("running Utilities test 4")
        text = TextNode("This **text** is **very** bold.", TextType.TEXT)
        test_nodes = [
            TextNode("This ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" is ", TextType.TEXT),
            TextNode("very", TextType.BOLD),
            TextNode(" bold.", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([text], "**", TextType.BOLD), test_nodes)

    def test_eq5(self):
        print("running Utilities test 6")
        text = TextNode("**BALLS**", TextType.TEXT)
        test_nodes = [
            TextNode("BALLS", TextType.BOLD),
        ]
        self.assertEqual(split_nodes_delimiter([text], "**", TextType.BOLD), test_nodes)

    def test_exception(self):
        print("running Utilities test 5")
        text = TextNode("This **text** is **very bold.", TextType.TEXT)
        with self.assertRaises(Exception):
            answer = split_nodes_delimiter([text], "**", TextType.BOLD)
            #print(f"{answer[0]}\n{answer[1]}\n{answer[2]}")
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images2(self):
        matches = extract_markdown_images(
        "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"),("to youtube", "https://www.youtube.com/@bootdotdev")], matches)


if __name__ == "__main__":
    unittest.main()