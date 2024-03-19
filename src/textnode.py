from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

TEXT_TYPES = {
    text_type_text: lambda node: LeafNode(None, node.text),
    text_type_bold: lambda node: LeafNode("b", node.text),
    text_type_italic: lambda node: LeafNode("i", node.text),
    text_type_code: lambda node: LeafNode("code", node.text),
    text_type_link: lambda node: LeafNode("a", node.text, {"href": node.url}),
    text_type_image: lambda node: LeafNode(
        "img", None, {"src": node.url, "alt": node.text}
    ),
}


class TextNode:
    def __init__(self, text: str, text_type: str, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, __value: object) -> bool:
        return (
            self.text == __value.text
            and self.text_type == __value.text_type
            and self.url == __value.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    try:
        return TEXT_TYPES[text_node.text_type](text_node)
    except:
        raise ValueError(f"invalid text type: {text_node.text_type}")
