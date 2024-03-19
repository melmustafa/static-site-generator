from textnode import TextNode

from inline_markdown import extract_markdown_images


def main():
    text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
    extract_markdown_images(text)


if __name__ == "__main__":
    main()
