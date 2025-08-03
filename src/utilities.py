import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            print(f"{node.text} {node.text.count(delimiter)}")
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
    return re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

            
