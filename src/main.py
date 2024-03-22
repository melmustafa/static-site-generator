import os.path
from shutil import copy, rmtree


def copy_directory(src: str, dst: str) -> None:
    os.mkdir(dst)
    files = os.listdir(src)
    for file in files:
        src_path =os.path.join(src, file)
        dst_path = os.path.join(dst, file)
        if os.path.isfile(src_path):
            copy(src_path, dst_path)
        else: 
            copy_directory(src_path, dst_path)

def main():
    source_path = "static"
    destination_path = "public"
    if not os.path.exists(source_path):
        print("No static directory was found")
        exit(0)
    if os.path.exists(destination_path):
        rmtree(destination_path)
    copy_directory(source_path, destination_path)


if __name__ == "__main__":
    main()

















