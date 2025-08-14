import re
from textnode import TextNode, TextType
from blocktype import BlockType, block_to_block_type

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            #print(f"{node.text} '{delimiter}': {node.text.count(delimiter)}")
            # check if delimiters are in matched pairs (% 2 != 0)
            if (node.text.count(delimiter) % 2) != 0:
                raise Exception(f"Invalid Markdown syntax, unmatched '{delimiter}'(s)")
            split_text = node.text.split(delimiter)
            for i in range(len(split_text)):
                if i % 2 != 0:
                    new_nodes.append(TextNode(split_text[i], text_type))
                elif i % 2 == 0 and split_text[i] != "":
                    new_nodes.append(TextNode(split_text[i], TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"[^!]\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    #print("\n\n")
    new_nodes = []
    for node in old_nodes:
        bracket_count = (node.text.count('[') + node.text.count(']') + node.text.count('(') + node.text.count(')'))
        if (
            node.text_type == TextType.TEXT and
            bracket_count != 0
        ):
            # check if delimiters are in matched pairs (% 2 != 0) and that there's a !
            if (
                bracket_count % 4 != 0 and
                bracket_count != node.text.count('!') * 2
            ):
                raise Exception(f"Invalid Markdown syntax")
            # Step 1: extract image alt text / links
            images = extract_markdown_images(node.text)
            # Step 1.5: set text_to_split variable to the node's text value
            text_to_split = node.text
            # Step 2: iterate through the image pairs
            for image_pair in images:
                #print(text_to_split)
                #print(f"![{image_pair[0]}]({image_pair[1]})")
                # Step 3: split the text on the image pair text block only once
                split_text = text_to_split.split(f"![{image_pair[0]}]({image_pair[1]})", maxsplit=1)
                #print(split_text)
                # Step 4: if the leading split string isn't empty, add it to the list
                if split_text[0] != "":
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                # Step 5: Add the image link to the list
                new_nodes.append(TextNode(image_pair[0], TextType.IMAGE, image_pair[1]))
                # Step 6: set text_to_split to the rest of the split string
                text_to_split = split_text[1]
            # Step 7: once the links are entered, add the rest of the string at the end if not empty.
            if text_to_split != "":
                new_nodes.append(TextNode(text_to_split, TextType.TEXT))
        else:
            new_nodes.append(node)
    #print(new_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    #print("\n\n")
    new_nodes = []
    for node in old_nodes:
        bracket_count = (node.text.count('[') + node.text.count(']') + node.text.count('(') + node.text.count(')'))
        # If the node isn't a TEXT node or it has no links, append it like it is
        if (
            node.text_type == TextType.TEXT and
            bracket_count != 0
        ):
            # check if delimiters are in matched pairs (% 2 != 0) and that there's a !
            if (
                bracket_count % 4 != 0
            ):
                raise Exception(f"Invalid Markdown syntax")
            # Step 1: extract image alt text / links
            links = extract_markdown_links(node.text)
            # Step 1.5: set text_to_split variable to the node's text value
            text_to_split = node.text
            # Step 2: iterate through the image pairs
            for link_pair in links:
                #print(text_to_split)
                #print(f"[{link_pair[0]}]({link_pair[1]})")
                # Step 3: split the text on the image pair text block only once
                split_text = text_to_split.split(f"[{link_pair[0]}]({link_pair[1]})", maxsplit=1)
                #print(split_text)
                # Step 4: if the leading split string isn't empty, add it to the list
                if split_text[0] != "":
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                # Step 5: Add the link to the list
                new_nodes.append(TextNode(link_pair[0], TextType.LINK, link_pair[1]))
                # Step 6: set text_to_split to the rest of the split string
                text_to_split = split_text[1]
            # Step 7: once the links are entered, add the rest of the string at the end if not empty.
            if text_to_split != "":
                new_nodes.append(TextNode(text_to_split, TextType.TEXT))
        else:
            new_nodes.append(node)
    #print(new_nodes)
    return new_nodes

def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_image(new_nodes)
    return new_nodes
            
def markdown_to_blocks(markdown):
    split_markdown = markdown.split("\n\n")
    blocks_to_return = []
    for block in split_markdown:
        #print(f"@@\n{block}")
        #print("@@")
        block = block.strip()
        block = block.strip("\n")
        blocks_to_return.append(block)
        #print(f"@@\n{block}")
        #print("@@")
    return blocks_to_return

def block_to_text_lines(block):
    print(block)
    print(block_to_block_type(block))
    block_type = block_to_block_type(block)
    split_blocks = block.split("\n")
    block_list = []
    match (block_type):
        case BlockType.HEADING:
            for sblock in split_blocks:
                sblocktext = block.lstrip("#")
                sblocktext = block.strip()
                block_list.append(sblocktext)
            return block_list
        case BlockType.CODE:
            for sblock in split_blocks:
                if sblock != "```":
                    block_list.append(sblock)
            return block_list
        case BlockType.QUOTE:
            for sblock in split_blocks:
                block_list.append( sblock.lstrip(">") )
            return block_list
        case BlockType.UNORDERED_LIST:
            for sblock in split_blocks:
                block_list.append( sblock.lstrip("- ") )
            return block_list
        case BlockType.ORDERED_LIST:
            number = 1
            for sblock in split_blocks:
                block_list.append( sblock.lstrip(f"{number}. ") )
                number += 1
            return block_list
        case BlockType.PARAGRAPH:
            return split_blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
