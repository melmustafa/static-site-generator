import os
from shutil import copy, rmtree

from markdown_block import markdown_to_html


def copy_directory(src: str, dst: str) -> None:
    if not os.path.exists(src):
        print("No static directory was found")
        exit(0)
    if os.path.exists(dst):
        rmtree(dst)
    os.mkdir(dst)
    files = os.listdir(src)
    for file in files:
        src_path = os.path.join(src, file)
        dst_path = os.path.join(dst, file)
        if os.path.isfile(src_path):
            copy(src_path, dst_path)
        else:
            copy_directory(src_path, dst_path)


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    title_line = lines[0]
    title_line.lstrip(" ")
    if title_line[0] == "#" and title_line[1] != "#":
        return title_line.lstrip("# ")
    raise Exception("Invalid Markdown: all pages need a header")


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    source_file = open(from_path)
    markdown = source_file.read()
    source_file.close()
    title = extract_title(markdown)
    markdown = "\n".join(markdown.split("\n")[1:])
    template_file = open(template_path)
    html = template_file.read()
    template_file.close()
    html = html.replace("{{ Title }}", title)
    body = markdown_to_html(markdown).to_html()
    html = html.replace("{{ Content }}", body)
    dest_file = open(dest_path, "w")
    dest_file.write(html)
    dest_file.close()


def generate_pages_recursive(src: str, template_path: str, dst: str) -> None:
    files = os.listdir(src)
    for file in files:
        src_path = os.path.join(src, file)
        dst_path = os.path.join(dst, file)
        if file[-3:] == ".md":

            generate_page(src_path, template_path, dst_path[:-3] + ".html")
        elif os.path.isdir(src_path):
            os.mkdir(dst_path)
            generate_pages_recursive(src_path, template_path, dst_path)


def main():
    source_path = "static"
    destination_path = "public"
    copy_directory(source_path, destination_path)
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
