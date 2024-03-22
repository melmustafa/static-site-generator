import unittest

from markdown_block import (block_to_block_type, block_type_code,
                            block_type_heading, block_type_ordered_list,
                            block_type_paragraph, block_type_quote,
                            block_type_unordered_list, markdown_to_blocks,
                            markdown_to_html)


class TestTextNode(unittest.TestCase):
    def test_empty_markdown_markdown_to_blocks(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_markdown_to_blocks_with_many_new_lines(self):
        markdown = """



# This is a heading




This is a paragraph of text. It has some **bold** and *italic* words inside of it.




* This is a list item
* This is another list item
"""
        self.assertEqual(
            markdown_to_blocks(markdown),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is a list item\n* This is another list item",
            ],
        )

    def test_markdown_to_blocks(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        self.assertEqual(
            markdown_to_blocks(markdown),
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_heading_type(self):
        markdown = """


        # This is a heading

        
        
        """
        self.assertEqual(block_to_block_type(markdown), block_type_heading)

    def test_block_to_paragraph_type_with_wrong_heading(self):
        markdown = """
# This is a heading
Hello World!!!
"""
        self.assertEqual(block_to_block_type(markdown), block_type_paragraph)

    def test_block_to_ordered_list_type(self):
        markdown = """


        1. This is a heading
2. Hello World!!!
3. Zika


"""
        self.assertEqual(block_to_block_type(markdown), block_type_ordered_list)

    def test_block_to_paragraph_type_with_ordered_list(self):
        markdown = """


        1. This is a heading
2. Hello World!!!
3. Zika
Something


"""
        self.assertEqual(block_to_block_type(markdown), block_type_paragraph)

    def test_block_to_unordered_list_type(self):
        markdown = """


        * This is a heading
* Hello World!!!
* Zika


"""
        self.assertEqual(block_to_block_type(markdown), block_type_unordered_list)

    def test_block_to_paragraph_type_with_unordered_list(self):
        markdown = """


        * This is a heading
* Hello World!!!
- Zika
Something


"""
        self.assertEqual(block_to_block_type(markdown), block_type_paragraph)

    def test_block_to_paragraph_type_with_code_like_marks(self):
        markdown = """


        ```This is a heading
Hello World!!!
Zika```
Something

"""
        self.assertEqual(block_to_block_type(markdown), block_type_paragraph)

    def test_block_to_code_type(self):
        markdown = """


        ```This is a heading
Hello World!!!
Zika
Something```


"""
        self.assertEqual(block_to_block_type(markdown), block_type_code)

    def test_block_to_paragraph_type_with_quote_like_marks(self):
        markdown = """


        > This is a heading
> Hello World!!!
> Zika
Something

"""
        self.assertEqual(block_to_block_type(markdown), block_type_paragraph)

    def test_block_to_quote_type(self):
        markdown = """


        > This is a heading
> Hello World!!!
> Zika
> Something


"""
        self.assertEqual(block_to_block_type(markdown), block_type_quote)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )


if __name__ == "__main__":
    unittest.main()



