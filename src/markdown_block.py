from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown: str) -> list:
    lines = markdown.split("\n")
    blocks = []
    block = ""
    for line in lines:
        if line == "" and block.lstrip("\n").rstrip("\n") != "":
            blocks.append(block.lstrip("\n").rstrip("\n"))
            block = ""
            continue
        else:
            block += line + "\n"
    return blocks


def block_to_block_type(markdown_block: str) -> str:
    lines = markdown_block.lstrip("\n ").rstrip("\n ").split("\n")
    if lines[0][0] == "#" and len(lines) == 1:
        return block_type_heading
    if lines[0][0] == ">":
        for index in range(1, len(lines)):
            if lines[index][0] != ">":
                return block_type_paragraph
        return block_type_quote
    if lines[0][:3] == lines[-1][-3:] == "```":
        return block_type_code
    if lines[0][0] == "*" or lines[0][0] == "-":
        for index in range(1, len(lines)):
            if lines[index][0] != "*" and lines[index][0] != "-":
                return block_type_paragraph
        return block_type_unordered_list
    block_type = block_type_ordered_list
    for index in range(1, len(lines) + 1):
        if f"{index}." != lines[index - 1].split(" ")[0]:
            block_type = block_type_paragraph
    return block_type


def text_to_children(text: str) -> list:
    children = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    return children


def quote_block_to_html(markdown: str) -> ParentNode:
    new_lines = []
    lines = markdown.split("\n")
    for line in lines:
        new_lines.append(line.lstrip(" >"))
    text = " ".join(new_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)


def unordered_list_block_to_html(markdown: str) -> ParentNode:
    nodes = []
    items = markdown.split("\n")
    for item in items:
        text = item[2:]
        node = ParentNode("li", text_to_children(text))
        nodes.append(node)
    return ParentNode("ul", nodes)


def ordered_list_block_to_html(markdown: str) -> ParentNode:
    nodes = []
    items = markdown.split("\n")
    for item in items:
        text = item.lstrip(" 1234567890. ")
        node = ParentNode("li", text_to_children(text))
        nodes.append(node)
    return ParentNode("ol", nodes)


def code_block_to_html(markdown: str) -> ParentNode:
    line = markdown.lstrip("` \n").rstrip(" `\n")
    children = text_to_children(line)
    code_node = ParentNode("code", children)
    return ParentNode("pre", [code_node])


def heading_block_to_html(markdown: str) -> ParentNode:
    count = 0
    for char in markdown:
        if char != "#":
            break
        if count == 6:
            break
        count += 1
    children = text_to_children(markdown.lstrip("# "))
    return ParentNode(f"h{count}", children)


def paragraph_block_to_html(markdown: str) -> ParentNode:
    text = " ".join(markdown.lstrip(" ").rstrip(" ").split("\n"))
    return ParentNode("p", text_to_children(text))


def markdown_to_html(document: str) -> ParentNode:
    blocks = markdown_to_blocks(document.lstrip("\n "))
    nodes = []
    for markdown in blocks:
        type = block_to_block_type(markdown)
        if type == block_type_code:
            node = code_block_to_html(markdown)
        elif type == block_type_ordered_list:
            node = ordered_list_block_to_html(markdown)
        elif type == block_type_unordered_list:
            node = unordered_list_block_to_html(markdown)
        elif type == block_type_heading:
            node = heading_block_to_html(markdown)
        elif type == block_type_quote:
            node = quote_block_to_html(markdown)
        else:
            node = paragraph_block_to_html(markdown)
        nodes.append(node)
    return ParentNode("div", nodes)
