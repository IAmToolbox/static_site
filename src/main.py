# Static Site Generator: My third guided project from boot.dev

import os
import shutil

from file_manip import copy_directory, generate_page

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")

    copy_directory("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

main()