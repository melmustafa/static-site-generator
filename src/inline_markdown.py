import re

from textnode import (
    TextNode,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
    text_type_text,
)


def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: str) -> list:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        splits = node.text.split(delimiter)
        if len(splits) % 2 != 1:
            raise ValueError(
                f"Invalid markdown: no closing delimiter. Delimiter: {delimiter}"
            )
        for index in range(len(splits)):
            if len(splits[index]) == 0:
                continue
            type = text_type
            if index % 2 == 0:
                type = text_type_text
            node = TextNode(splits[index], type)
            new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text: str) -> list:
    regex = re.compile(r"!\[(.*?)\]\((.*?)\)")
    return regex.findall(text)


def split_nodes_image(old_nodes: list) -> list:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        text = node.text
        if text == "":
            continue
        images = extract_markdown_images(text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            text = text.split(f"![{image[0]}]({image[1]})")
            if text[0] != "":
                new_text_node = TextNode(text[0], text_type_text)
                new_nodes.append(new_text_node)
            new_image_node = TextNode(image[0], text_type_image, image[1])
            new_nodes.append(new_image_node)
            text = text[1]
        if text != "":
            new_text_node = TextNode(text, text_type_text)
            new_nodes.append(new_text_node)
    return new_nodes


def extract_markdown_links(text: str) -> list:
    regex = re.compile(r"\[(.*?)\]\((.*?)\)")
    return regex.findall(text)


def split_nodes_link(old_nodes: list) -> list:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        text = node.text
        if text == "":
            continue
        links = extract_markdown_links(text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            text = text.split(f"[{link[0]}]({link[1]})")
            if text[0] != "":
                new_text_node = TextNode(text[0], text_type_text)
                new_nodes.append(new_text_node)
            new_link_node = TextNode(link[0], text_type_link, link[1])
            new_nodes.append(new_link_node)
            text = text[1]
        if text != "":
            new_text_node = TextNode(text, text_type_text)
            new_nodes.append(new_text_node)
    return new_nodes


def text_to_textnodes(text: str) -> list:
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    return nodes
