import unittest

from textnode import TextNode, TextType
from utilities import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link


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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_then_images(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and an ![image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        new_nodes_2 = split_nodes_image(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes_2,
        )

    def test_split_delimiter_then_links(self):
        node = TextNode(
            "This is text with a very **exciting** [link](https://i.imgur.com/zjjcJKZ.png)!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes_2 = split_nodes_link(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a very ", TextType.TEXT),
                TextNode("exciting", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("!", TextType.TEXT),
                
            ],
            new_nodes_2,
        )

if __name__ == "__main__":
    unittest.main()

