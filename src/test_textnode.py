import unittest

from textnode import TextNode


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


if __name__ == "__main__":
    unittest.main()
