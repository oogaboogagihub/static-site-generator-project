from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        
        split_nodes = node.text.split(delimiter)
        if len(split_nodes) % 2 == 0:
            raise ValueError("Invalid markdown syntax")
        
        for index, split_node in enumerate(split_nodes):
            if split_node == "":
                continue
            
            if index % 2 == 0:
                new_nodes.append(TextNode(split_node, TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_node, text_type))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    # make sure input is a text node
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        end_marker = 0

        for match in re.finditer(r"!\[([^\]]+)\]\(([^)]+)\)", node.text):
            # if text before a match exists, append it as a new text node
            if node.text[end_marker:match.start()] != "":
                new_nodes.append(TextNode(node.text[end_marker:match.start()], TextType.TEXT))
            
            #create and append image node
            new_nodes.append(TextNode(match.group(1), TextType.IMAGE, match.group(2)))

            #set end marker
            end_marker = match.end()

        # extra text gets added as a new text node
        if node.text[end_marker:] != "":
            new_nodes.append(TextNode(node.text[end_marker:], TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    # make sure input is a text node
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        end_marker = 0

        for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", node.text):
            # if text before a match exists, append it as a new text node
            if node.text[end_marker:match.start()] != "":
                new_nodes.append(TextNode(node.text[end_marker:match.start()], TextType.TEXT))
            
            #create and append link node
            new_nodes.append(TextNode(match.group(1), TextType.LINK, match.group(2)))

            #set end marker
            end_marker = match.end()

        # extra text gets added as a new text node
        if node.text[end_marker:] != "":
            new_nodes.append(TextNode(node.text[end_marker:], TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    # initialize raw text as a text node
    nodes = [TextNode(text, TextType.TEXT)]

    # check image formatting first to prevent collisions with link formatting
    nodes = split_nodes_image(nodes)

    # check link formatting to prevent collisions with text formatting
    nodes = split_nodes_link(nodes)

    # split remaining nodes by each format delimiter
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes