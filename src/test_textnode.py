import unittest

from textnode import (
    TextNode,
    text_node_to_html_node,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
    text_type_text,
)

from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq_without_url(self):
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node1, node2)

    def test_eq_with_url(self):
        node1 = TextNode("This is a text node", "bold", "https://zikkas.dev")
        node2 = TextNode("This is a text node", "bold", "https://zikkas.dev")
        self.assertEqual(node1, node2)

    def test_not_eq_without_url(self):
        node1 = TextNode("This is a text node", "old")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node1, node2)

    def test_not_eq_with_url(self):
        node1 = TextNode("This is a text nod", "bold", "https://zikkas.dev")
        node2 = TextNode("This is a text node", "bold", "https://zikkas.dev")
        self.assertNotEqual(node1, node2)

    def test_repr_without_url(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(node.__repr__(), "TextNode(This is a text node, bold, None)")

    def test_repr_with_url(self):
        node = TextNode("This is a text node", "bold", "https://zikkas.dev")
        self.assertEqual(
            node.__repr__(), "TextNode(This is a text node, bold, https://zikkas.dev)"
        )

    def test_text_type_node_to_leafnode(self):
        node = TextNode("This is a test node", text_type_text)
        self.assertEqual(
            text_node_to_html_node(node).__repr__(),
            LeafNode(None, "This is a test node").__repr__(),
        )

    def test_bold_type_node_to_leafnode(self):
        node = TextNode("This is a test node", text_type_bold)
        self.assertEqual(
            text_node_to_html_node(node).__repr__(),
            LeafNode("b", "This is a test node").__repr__(),
        )

    def test_code_type_node_to_leafnode(self):
        node = TextNode("This is a test node", text_type_code)
        self.assertEqual(
            text_node_to_html_node(node).__repr__(),
            LeafNode("code", "This is a test node").__repr__(),
        )

    def test_italic_type_node_to_leafnode(self):
        node = TextNode("This is a test node", text_type_italic)
        self.assertEqual(
            text_node_to_html_node(node).__repr__(),
            LeafNode("i", "This is a test node").__repr__(),
        )

    def test_image_type_node_to_leafnode(self):
        node = TextNode("This is a test image", text_type_image, "https://hello")
        self.assertEqual(
            text_node_to_html_node(node).__repsr__(),
            LeafNode(
                "img", None, {"src": "https://hello", "alt": "This is a test image"}
            ).__repr__(),
        )

    def test_link_type_node_to_leafnode(self):
        node = TextNode("This is a test link", text_type_link, "https://hello")
        self.assertEqual(
            text_node_to_html_node(node).__repr__(),
            LeafNode("a", "This is a test link", {"href": "https://hello"}).__repr__(),
        )

    def test_other_type_node_to_leafnode(self):
        node = TextNode("This is a test node", "something")
        with self.assertRaisesRegex(ValueError, "invalid text type: something"):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()
