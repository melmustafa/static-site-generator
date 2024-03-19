from textnode import TextNode, text_type_text


def split_nodes_delimiter(old_nodes, delimiter, text_type):
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
