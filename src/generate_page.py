import os, shutil

from block_markdown import markdown_to_html_node


def extract_title(markdown):
    # check each line for a header markdown tag, returns the line without the tag
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No title found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # store source file in markdown
    try:
        with open(from_path) as file:
            markdown = file.read()
    except FileNotFoundError as e:
        raise Exception("Source file not found") from e
    
    # store template file in variable
    try:
        with open(template_path) as file:
            template = file.read()
    except FileNotFoundError as e:
        raise Exception("Template not found") from e
    
    # convert markdown to an html string
    html_string = markdown_to_html_node(markdown).to_html()

    title = extract_title(markdown)

    # replace the title and content sections of the template
    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html_string)

    # create the destination directory and write the file
    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, 'w') as file:
        file.write(page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # try to store a list of the content of the source directory
    try:
        files = os.listdir(dir_path_content)
    except FileNotFoundError as e:
        raise Exception("The source directory is not found") from e
    
    # create destination directory
    os.makedirs(dest_dir_path, exist_ok=True)

    # check each file in the directory, generate html if it's a markdown, recurse if it's a folder
    for item in files:
        item_path = os.path.join(dir_path_content, item)
        destination_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(item_path):
            dest_name, ext = os.path.splitext(destination_path)
            if ext == ".md":
                dest_html_filename = dest_name + ".html"
                generate_page(item_path, template_path, dest_html_filename)
            else:
                continue
        else:
            os.makedirs(destination_path, exist_ok=True)
            generate_pages_recursive(item_path, template_path, destination_path)