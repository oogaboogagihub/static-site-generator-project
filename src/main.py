from textnode import TextNode
from generate_page import generate_page, generate_pages_recursive

import os, shutil

def main():
    # reset public to contents of static
    rm_dir("./public")
    copy_dir("./static", "./public")

    # generate page
    from_path = "./content/"
    template_path = "./template.html"
    dest_path = "./public/"
    generate_pages_recursive(from_path, template_path, dest_path)

def rm_dir(destination):
    # make sure destination doesn't already exist
    if os.path.exists(destination):
        shutil.rmtree(destination)
        print(f"Removing folder: {destination}")

def copy_dir(source, destination):
    # create an empty destination folder if it doesn't exist
    if not os.path.exists(destination):
        os.mkdir(destination)
        print(f"Created folder: {destination}")

    # check each file in source folder
    for item in os.listdir(source):
        # calculate item paths
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        # if item is a file, copy it. if it's a folder, make it and recurse
        if os.path.isfile(source_path):
            shutil.copy(src=source_path, dst=destination_path)
            print(f"Copied file:\n from: {source_path}\n to: {destination_path}")
        else:
            os.mkdir(destination_path)
            print(f"Created folder: {destination_path}")
            copy_dir(source_path, destination_path)

main()