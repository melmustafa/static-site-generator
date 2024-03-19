import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_empty_htmlnode_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_htmlnode_to_html(self):
        node = HTMLNode("p", "Hello World!!!")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_empty_node_props_to_html(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_no_props_node_props_to_html(self):
        node = HTMLNode("p", "Hello World!!!")
        self.assertEqual(node.props_to_html(), "")

    def test_empty_props_node_props_to_html(self):
        node = HTMLNode("p", "Hello World!!!", None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html(self):
        node = HTMLNode(
            "a", "my personal site", None, {"href": "zikkas.dev", "target": "_blank"}
        )
        self.assertEqual(node.props_to_html(), ' href="zikkas.dev" target="_blank"')

    def test_repr_empty_node(self):
        node = HTMLNode()
        self.assertEqual(node.__repr__(), "HTMLNode(None, None, None, None)")

    def test_repr(self):
        node = HTMLNode(
            "a", "my personal site", None, {"href": "zikkas.dev", "target": "_blank"}
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(a, my personal site, None, {'href': 'zikkas.dev', 'target': '_blank'})",
        )

    def test_empty_leafnode(self):
        with self.assertRaisesRegex(ValueError, "Invalid HTML: value is required"):
            LeafNode()

    def test_no_tag_leafnode_without_props_to_html(self):
        node = LeafNode(None, "Hello World!!!")
        self.assertEqual(node.to_html(), "Hello World!!!")

    def test_leafnode_without_props_to_html(self):
        node = LeafNode("p", "Hello World!!!")
        self.assertEqual(node.to_html(), "<p>Hello World!!!</p>")

    def test_leafnode_with_props_to_html(self):
        node = LeafNode(
            "a", "my personal site", {"href": "zikkas.dev", "target": "_blank"}
        )
        self.assertEqual(
            node.to_html(), '<a href="zikkas.dev" target="_blank">my personal site</a>'
        )

    def test_empty_parentnode(self):
        with self.assertRaisesRegex(ValueError, "Invalid HTML: tag is required"):
            ParentNode()

    def test_empty_children_parentnode(self):
        with self.assertRaisesRegex(ValueError, "Invalid HTML: children is required"):
            ParentNode("ol")

    def test_empty_children_list_parentnode(self):
        with self.assertRaisesRegex(ValueError, "Invalid HTML: children is empty"):
            ParentNode("ol", [])

    def test_parentnode_with_leafnode_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_parentnode_with_leafnode_and_props_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"style": "text-align:right", "id": "paragraph"},
        )
        self.assertEqual(
            node.to_html(),
            '<p style="text-align:right" id="paragraph"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>',
        )

    def test_parentnode_with_mix_nodes_and_props_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                ParentNode(
                    "ol",
                    [
                        LeafNode("li", "Coffee"),
                        LeafNode("li", "Tea"),
                        LeafNode("li", "Milk"),
                    ],
                    {"start": 50},
                ),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"style": "text-align:right", "id": "paragraph"},
        )
        self.assertEqual(
            node.to_html(),
            '<p style="text-align:right" id="paragraph"><b>Bold text</b>Normal text<ol start="50"><li>Coffee</li><li>Tea</li><li>Milk</li></ol><i>italic text</i>Normal text</p>',
        )

    def test_parentnode_with_wrong_children_to_html(self):
        node = ParentNode(
            "p",
            [1, 2, 3],
        )
        with self.assertRaisesRegex(
            TypeError, "Invalid HTML: children type must be of LeafNode"
        ):
            node.to_html(),


if __name__ == "__main__":
    unittest.main()
