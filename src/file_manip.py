# Functions that can manipulate files and directories

import os
import shutil

from conversions import *

def copy_directory(source, destination):
    items = os.listdir(source)

    for item in items:
        source_path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
            print(f"Copied file: {source_path} to {dest_path}")
        else:
            if not os.path.exists(dest_path):
                os.mkdir(dest_path)
                print(f"Created directory: {dest_path}")
            copy_directory(source_path, dest_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md_file = open(from_path)
    md_file_contents = md_file.read()
    md_file.close()

    template_file = open(template_path)
    template_file_content = template_file.read()
    template_file.close()

    main_node = markdown_to_html_node(md_file_contents)
    main_node_html = main_node.to_html()
    page_title = extract_title(md_file_contents)
    template_file_content = template_file_content.replace("{{ Title }}", page_title)
    template_file_content = template_file_content.replace("{{ Content }}", main_node_html)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    index = open(dest_path, "w")
    index.write(template_file_content)
    index.close()

