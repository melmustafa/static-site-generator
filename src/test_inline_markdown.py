import unittest

from inline_markdown import split_nodes_delimiter

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_empty_node_split_delimiter(self):
        node = TextNode("", "text")
        self.assertEqual(split_nodes_delimiter([node], "*", "bold"), [])

    def test_split_delimiter(self):
        nodes = []
        nodes.append(TextNode("This is a test node", "something"))
        nodes.append(TextNode("This is text with a **bolded** word", "text"))
        nodes.append(TextNode("This is a **test** node", "bold"))
        self.assertEqual(
            split_nodes_delimiter(nodes, "**", "bold"),
            [
                TextNode("This is a test node", "something"),
                TextNode("This is text with a ", "text"),
                TextNode("bolded", "bold"),
                TextNode(" word", "text"),
                TextNode("This is a **test** node", "bold"),
            ],
        )

    def test_split_delimiter_with_special_node(self):
        node = TextNode("This is text with a **bolded word**", "text")
        self.assertEqual(
            split_nodes_delimiter([node], "**", "bold"),
            [
                TextNode("This is text with a ", "text"),
                TextNode("bolded word", "bold"),
            ],
        )
