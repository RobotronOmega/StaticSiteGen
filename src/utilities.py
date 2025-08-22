import re
from textnode import TextNode, TextType, text_node_to_html_node
from blocktype import BlockType, block_to_block_type
from htmlnode import HTMLNode, LeafNode, ParentNode
import os, shutil

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    #print(f"splitting on {delimiter} for {text_type}...")
    new_nodes = []
    for node in old_nodes:
        # Only split TEXT nodes
        if node.text_type == TextType.TEXT:
            #print(f"{node.text} '{delimiter}': {node.text.count(delimiter)}")
            # check if delimiters are in matched pairs (% 2 != 0)
            if (node.text.count(delimiter) % 2) != 0:
                raise Exception(f"Invalid Markdown syntax, unmatched '{delimiter}'(s)")
            split_text = node.text.split(delimiter)
            #print(split_text)
            for i in range(len(split_text)):
               # print(f"split_text[{i}] : {split_text[i]}")
                if i % 2 != 0:
                    new_nodes.append(TextNode(split_text[i], text_type))
                elif i % 2 == 0 and split_text[i] != "":
                    new_nodes.append(TextNode(split_text[i], TextType.TEXT))
        else:
            new_nodes.append(node)
    #print(new_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    #print("\n\n")
    new_nodes = []
    for node in old_nodes:
        # Only split TEXT nodes
        if node.text_type == TextType.TEXT:
            # Step 1: extract image alt text / links
            images = extract_markdown_images(node.text)
            if images == "":
                new_nodes.append(node)
            else:
                # check if delimiters are in matched pairs (% 2 != 0) and that there's a !
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
        # Only split TEXT nodes
        if node.text_type == TextType.TEXT:
            # Step 1: extract image alt text / links
            links = extract_markdown_links(node.text)
            # if there are no links, there's no link to split, append it like it is
            if links == "":
                new_nodes.append(node)
            # Else, continue
            else:
                # Step 1.5: set text_to_split variable to the node's text value
                text_to_split = node.text
                # Step 2: iterate through the image pairs
                for link_pair in links:
                    #print(text_to_split)
                    #print(f"[{link_pair[0]}]({link_pair[1]})")
                    # Step 3: split the text on the image pair text block only once
                    split_text = text_to_split.split(f"[{link_pair[0]}]({link_pair[1]})", maxsplit=1)
                    print(split_text)
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
        if block != "":
            blocks_to_return.append(block)
        #print(f"@@\n{block}")
        #print("@@")
    return blocks_to_return

def block_to_text_node(block):
    #print(block)
    #print(block_to_block_type(block))
    block_type = block_to_block_type(block)
    split_blocks = block.split("\n")
    block_list = []
    match (block_type):
        case BlockType.HEADING:
            for sblock in split_blocks:
                sblocktext = sblock.lstrip("#")
                sblocktext = sblocktext.strip()
                block_list.append(sblocktext)
        case BlockType.CODE:
            block_text = block.lstrip("```\n")
            block_text = block_text.rstrip("```")
            block_list.append(block_text)
        case BlockType.QUOTE:
            quote = ""
            for sblock in split_blocks:
                 sblock = sblock.lstrip(">")
                 sblock = sblock.lstrip()
                 quote += sblock + " "
            block_list.append(quote[:-1])
        case BlockType.UNORDERED_LIST:
            for sblock in split_blocks:
                block_list.append( sblock.lstrip("- ") )
        case BlockType.ORDERED_LIST:
            number = 1
            for sblock in split_blocks:
                block_list.append( sblock.lstrip(f"{number}. ") )
                number += 1
        case BlockType.PARAGRAPH:
            paragraph = ""
            for sblock in split_blocks:
                paragraph += sblock + " "
            block_list.append(paragraph[:-1])
    return block_list

def markdown_to_html_node(markdown):
    parent_div = ParentNode("div", [])
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match (block_type):
            case BlockType.HEADING:
                if block.startswith("# "):
                    block_node = ParentNode("h1", [])
                elif block.startswith("## "):
                    block_node = ParentNode("h2", [])
                elif block.startswith("### "):
                    block_node = ParentNode("h3", [])
                elif block.startswith("#### "):
                    block_node = ParentNode("h4", [])
                elif block.startswith("##### "):
                    block_node = ParentNode("h5", [])
                else:
                    block_node = ParentNode("h6", [])
                block_text = block_to_text_node(block)[0]
                #print(f"HEADING:\n{block_text}")
                block_nodes = text_to_textnodes(block_text)
                #print(block_nodes)
                for node in block_nodes:
                    block_node.children.append(text_node_to_html_node(node))
            case BlockType.CODE:
                block_text = block_to_text_node(block)[0]
                code_node = LeafNode("code", block_text)
                block_node = ParentNode("pre", [code_node])
            case BlockType.QUOTE:
                block_text = block_to_text_node(block)[0]
                #print(f"QUOTE:\n{block_text}")
                block_nodes = text_to_textnodes(block_text)
                #print(block_nodes)
                block_node = ParentNode("blockquote", [])
                for node in block_nodes:
                    block_node.children.append(text_node_to_html_node(node))
            case BlockType.UNORDERED_LIST:
                block_node = ParentNode("ul", [])
                list_text = block_to_text_node(block)
                #print(f"UNORDERED LIST:\n")
                for item in list_text:
                    #print(item)
                    item_nodes = text_to_textnodes(item)
                    print(item_nodes)
                    item_html = ParentNode("li", [])
                    for node in item_nodes:
                        item_html.children.append(text_node_to_html_node(node))
                    block_node.children.append(item_html)
            case BlockType.ORDERED_LIST:
                block_node = ParentNode("ol", [])
                list_text = block_to_text_node(block)
                #print("ORDERED LIST:\n")
                for item in list_text:
                    #print(item)
                    item_nodes = text_to_textnodes(item)
                    print(item_nodes)
                    item_html = ParentNode("li", [])
                    for node in item_nodes:
                        item_html.children.append(text_node_to_html_node(node))
                    block_node.children.append(item_html)
            case BlockType.PARAGRAPH:
                block_node = ParentNode("p", [])
                block_text = block_to_text_node(block)[0]
                #print(f"PARAGRAPH:\n{block_text}")
                block_nodes = text_to_textnodes(block_text)
                #print(block_nodes)
                for node in block_nodes:
                    block_node.children.append(text_node_to_html_node(node))
        parent_div.children.append(block_node)
    #print(parent_div)
    return parent_div

def extract_title(markdown):
    markdown_strip = markdown.lstrip()
    title = re.findall(r"^# (.*)\n", markdown_strip)
    if title == None:
        raise Exception("Markdown file must contain a top-tier header")
    return title[0]

def generate_page(from_path, template_path, dest_path):
    print(f"Generating {dest_path} from {from_path} using {template_path}")
    # Read Markdown file to variable
    with open(from_path, 'r') as file:
        markdown = file.read()
    # Read template file to variable
    with open(template_path, 'r') as file:
        template = file.read()
    # Extract Title from markdown header
    title = extract_title(markdown)
    #print(title)
    # Convert markdown to html code
    content = markdown_to_html_node(markdown).to_html()
    #print(content)
    # Inject Title and Content into the template file
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    #print(template)
    # Verify path to destination and creeate if not present
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    # Write the templage file out to the destination
    with open(dest_path, 'w') as file:
        file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dir_path_dest):
    real_content = os.path.realpath(dir_path_content)
    real_dest = os.path.realpath(dir_path_dest)
    content_list = os.listdir(real_content)
    print(content_list)
    for item in content_list:
        real_item = os.path.join(real_content, item)
        if os.path.isfile(real_item):
            real_item_dest = f"{os.path.splitext(os.path.join(real_dest, item))[0]}.html"
            generate_page(real_item, template_path, real_item_dest)
        elif os.path.isdir(real_item):
            generate_pages_recursive(real_item, template_path, os.path.join(real_dest, item))

    
    