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
