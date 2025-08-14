from enum import Enum
from re import match, search
from textnode import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    # BlockType.HEADING check: 1-6 # followed by a space
    if (
        block.startswith("# ") or
        block.startswith("## ") or
        block.startswith("### ") or
        block.startswith("#### ") or
        block.startswith("##### ") or
        block.startswith("###### ")
    ) and "\n" not in block:
        return BlockType.HEADING
    # BlockType.CODE check: ``` at the beginning and end on their own line`
    #print(block)
    #print(block.startswith("```\n"))
    #print(block.endswith("\n```"))
    if (
        block.startswith("```\n") and
        block.endswith("\n```")
    ):
        return BlockType.CODE
    # split block lines for the rest of the tests
    split_lines = block.split("\n")
    # initialize booleans for three types
    is_quote = True
    is_u_list = True
    is_o_list = True
    # iterate over all the lines
    for i in range(len(split_lines)):
        # BlockType.QUOTE check: > and no space
        if not split_lines[i].startswith(">") or split_lines[i].startswith("> "):
            is_quote = False
        # BlockType.UNORDERED_LIST check: - and space
        if not split_lines[i].startswith("- "):
            is_u_list = False
        # BlockType.ORDERED_LIST heck: #. with a space, iterating from 1
        if not split_lines[i].startswith(f"{i + 1}. "):
            is_o_list = False
    # return the correct value if one of the variables remained True
    if is_quote:
        return BlockType.QUOTE
    if is_u_list:
        return BlockType.UNORDERED_LIST
    if is_o_list:
        return BlockType.ORDERED_LIST
    # otherwise, return BlockType.PARAGRAPH
    return BlockType.PARAGRAPH
    

