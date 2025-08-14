import unittest

from textnode import TextNode, TextType
from utilities import split_nodes_delimiter, split_nodes_image, split_nodes_link, extract_markdown_images, extract_markdown_links, text_to_textnodes, markdown_to_blocks, block_to_text_lines


class TestUtilities(unittest.TestCase):
    def test_eq(self):
        #print("running Utilities test 1")
        text = TextNode("This text is **very** bold.", TextType.TEXT)
        test_nodes = [
            TextNode("This text is ", TextType.TEXT),
            TextNode("very", TextType.BOLD),
            TextNode(" bold.", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([text], "**", TextType.BOLD), test_nodes)

    def test_eq2(self):
        #print("running Utilities test 2")
        text = TextNode("This text is quite _unique_.", TextType.TEXT)
        test_nodes = [
            TextNode("This text is quite ", TextType.TEXT),
            TextNode("unique", TextType.ITALIC),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([text], "_", TextType.ITALIC), test_nodes)

    def test_eq3(self):
        #print("running Utilities test 3")
        text = TextNode("`Blocks of code` seem like a real **burden**.", TextType.TEXT)
        test_nodes = [
            TextNode("Blocks of code", TextType.CODE),
            TextNode(" seem like a real **burden**.", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([text], "`", TextType.CODE), test_nodes)

    def test_eq4(self):
        #print("running Utilities test 4")
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
        #print("running Utilities test 6")
        text = TextNode("**BALLS**", TextType.TEXT)
        test_nodes = [
            TextNode("BALLS", TextType.BOLD),
        ]
        self.assertEqual(split_nodes_delimiter([text], "**", TextType.BOLD), test_nodes)

    def test_exception(self):
        #print("running Utilities test 5")
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

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_markdown_to_blocks(self):
        #print("Running markdown_to_blocks test 1")
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks2(self):
        #print("Running markdown_to_blocks test 1")
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
And so is this one

1. Analyze a problem
2. Come up with a plan
3. Break it into steps
4. Create a function plan for each step
5. Implement the solution

- This is a list
- with items

'10 PRINT HAHAHA
20 GOTO 10'
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\nAnd so is this one",
                "1. Analyze a problem\n2. Come up with a plan\n3. Break it into steps\n4. Create a function plan for each step\n5. Implement the solution",
                "- This is a list\n- with items",
                "'10 PRINT HAHAHA\n20 GOTO 10'",
            ],
        )

    def test_blocks_to_text(self):
        print("Running blocks_to_text test 1")
        block1 = "This is **bolded** paragraph"
        block2 = """This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
And so is this one"""

        block3 = """1. Analyze a problem
2. Come up with a plan
3. Break it into steps
4. Create a function plan for each step
5. Implement the solution"""

        block4 = """- This is a list
- with items"""

        block5 = """```
10 PRINT 'HAHAHA'
20 GOTO 10
```"""

        self.assertEqual(
            block_to_text_lines(block1),
            ["This is **bolded** paragraph"],
        )
        self.assertEqual(
            block_to_text_lines(block2),
            [
                "This is another paragraph with _italic_ text and `code` here",
                "This is the same paragraph on a new line",
                "And so is this one",
            ]
        )
        self.assertEqual(
            block_to_text_lines(block3),
            [
                "Analyze a problem",
                "Come up with a plan",
                "Break it into steps",
                "Create a function plan for each step",
                "Implement the solution",
            ]
        )
        self.assertEqual(
            block_to_text_lines(block4),
            [
                "This is a list",
                "with items",
            ]
        )
        self.assertEqual(
            block_to_text_lines(block5),
            [
                "10 PRINT 'HAHAHA'",
                "20 GOTO 10",
            ],
        )

if __name__ == "__main__":
    unittest.main()

