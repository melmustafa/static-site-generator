from textnode import TextNode

from inline_markdown import split_nodes_delimiter


def main():
    node = TextNode("This is a **text** node", "text")
    print(split_nodes_delimiter([node], "**", "bold"))


if __name__ == "__main__":
    main()
