import unittest

from blocktype import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        block = "#### This is a heading"
        block2 = "## So is this"
        block3 = "###### This too"
        block4 = "#This isn't"
        block5 = """# And neither
is this one"""
        type = block_to_block_type(block)
        type2 = block_to_block_type(block2)
        type3 = block_to_block_type(block3)
        type4 = block_to_block_type(block4)
        type5 = block_to_block_type(block5)
        self.assertEqual(type, BlockType.HEADING)
        self.assertEqual(type2, BlockType.HEADING)
        self.assertEqual(type3, BlockType.HEADING)
        self.assertEqual(type4, BlockType.PARAGRAPH)
        self.assertEqual(type5, BlockType.PARAGRAPH)


    def test_code(self):
        block = """```
This is a multi-line block of code
None of the things in here like
#, `, **, or _ should be rendered
when this is converted to HTML.
```"""
        type = block_to_block_type(block)
        self.assertEqual(type, BlockType.CODE)
    
    def test_quote(self):
        block = """>Roses are red
>Violets are blue
>This poem is stupid
>And so are you"""
        type = block_to_block_type(block)
        self.assertEqual(type, BlockType.QUOTE)

    def test_unordered_list(self):
        block = """- unit tests
- forgetting the double equals in comparisons
- forgetting to close parentheses
- forgetting to update function names when I copy and reuse code"""
        type = block_to_block_type(block)
        self.assertEqual(type, BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = """1. Learn programming
2. ???
3. Profit
4. Take over world"""
        type = block_to_block_type(block)
        self.assertEqual(type, BlockType.ORDERED_LIST)

    def test_paragraph_1(self):
        block = """#NotMyStarwars is known to be a lame hashtag, but people still use it.
Primarily manbabies and other deplorables."""
        type = block_to_block_type(block)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_paragraph_2(self):
        block = """- Listen, you just can't sit there and do that, okay?
People will start to notice and you'll be screwed.
Put the thing down already, will you?"""
        type = block_to_block_type(block)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_paragraph_3(self):
        block = """I'm not saying that you're an idiot but, look:
1. You definitely are
2. You should be ashamed of it
3. May God have mercy on your soul"""
        type = block_to_block_type(block)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_paragraph_4(self):
        block = """>I don't know how quotes work in Markdown.
you just need a carat on the first line, right?
And the rest will just work?
Anyone?
Bueller?"""
        type = block_to_block_type(block)
        self.assertEqual(type, BlockType.PARAGRAPH)
    


if __name__ == "__main__":
    unittest.main()
