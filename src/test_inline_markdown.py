import unittest

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_links,
    split_nodes_link,
    extract_markdown_images,
    split_nodes_image,
    text_to_textnodes,
)

from textnode import (
    TextNode,
    text_type_link,
    text_type_image,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
)


class TestTextNode(unittest.TestCase):
    def test_empty_node_split_delimiter(self):
        node = TextNode("", text_type_text)
        self.assertEqual(split_nodes_delimiter([node], "*", text_type_bold), [])

    def test_split_delimiter(self):
        nodes = []
        nodes.append(TextNode("This is a test node", "something"))
        nodes.append(TextNode("This is text with a **bolded** word", text_type_text))
        nodes.append(TextNode("This is a **test** node", text_type_bold))
        self.assertEqual(
            split_nodes_delimiter(nodes, "**", text_type_bold),
            [
                TextNode("This is a test node", "something"),
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
                TextNode("This is a **test** node", text_type_bold),
            ],
        )

    def test_split_delimiter_with_special_node(self):
        node = TextNode("This is text with a **bolded word**", text_type_text)
        self.assertEqual(
            split_nodes_delimiter([node], "**", text_type_bold),
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
            ],
        )

    def test_extract_markdown_links_empty_text(self):
        self.assertEqual(extract_markdown_links(""), [])

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("link", "https://www.example.com"),
                ("another", "https://www.example.com/another"),
            ],
        )

    def test_extract_markdown_links_no_links(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        self.assertEqual(
            extract_markdown_links(text),
            [],
        )

    def test_empty_node_split_nodes_link(self):
        self.assertEqual(split_nodes_link([TextNode("", text_type_text)]), [])

    def test_split_nodes_link(self):
        text1 = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        text2 = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        text3 = "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and [another](https://i.imgur.com/dfsdkjfd.png)"
        self.assertEqual(
            split_nodes_link(
                [
                    TextNode(text1, text_type_text),
                    TextNode(text2, text_type_text),
                    TextNode("my website", text_type_link, "zikkas.dev"),
                    TextNode(text3, text_type_text),
                ]
            ),
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link, "https://www.example.com"),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_link, "https://www.example.com/another"),
                TextNode(
                    "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)",
                    text_type_text,
                ),
                TextNode("my website", text_type_link, "zikkas.dev"),
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_link, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_link, "https://i.imgur.com/dfsdkjfd.png"),
            ],
        )

    def test_extract_markdown_images_empty_text(self):
        self.assertEqual(extract_markdown_images(""), [])

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("another", "https://i.imgur.com/dfsdkjfd.png"),
            ],
        )

    def test_extract_markdown_images_no_images(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.assertEqual(
            extract_markdown_images(text),
            [],
        )

    def test_extract_markdown_images_empty_text(self):
        self.assertEqual(extract_markdown_images(""), [])

    def test_empty_node_split_nodes_image(self):
        self.assertEqual(split_nodes_image([TextNode("", text_type_text)]), [])

    def test_split_nodes_image(self):
        text1 = "This is text with a ![link](https://www.example.com) and ![another](https://www.example.com/another)"
        text2 = "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and [another](https://i.imgur.com/dfsdkjfd.png)"
        text3 = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        self.assertEqual(
            split_nodes_image(
                [
                    TextNode(text1, text_type_text),
                    TextNode(text2, text_type_text),
                    TextNode("my website", text_type_code, "zikkas.dev"),
                    TextNode(text3, text_type_text),
                ]
            ),
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_image, "https://www.example.com"),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_image, "https://www.example.com/another"),
                TextNode(
                    "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and [another](https://i.imgur.com/dfsdkjfd.png)",
                    text_type_text,
                ),
                TextNode("my website", text_type_code, "zikkas.dev"),
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", text_type_text),
                TextNode(
                    "another", text_type_image, "https://i.imgur.com/dfsdkjfd.png"
                ),
            ],
        )

    def test_empty_text_text_to_textnodes(self):
        self.assertEqual(text_to_textnodes(""), [])

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
