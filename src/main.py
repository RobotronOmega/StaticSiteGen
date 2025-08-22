from textnode import TextNode
from textnode import TextType
from htmlnode import HTMLNode
from pathlib import Path
from utilities import generate_pages_recursive
import os, shutil, sys

def main():
    basepath = sys.argv[1]
    copy_directories("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


# copy_directories: copies one directory to another, deleting the former to ensure a clean copy.
def copy_directories(source, dest):
    realsource = os.path.realpath(source)
    realdest = os.path.realpath(dest)
    #print(f"source: {realsource}")
    #print(f"destination: {realdest}")
    if os.path.exists(realdest):
        shutil.rmtree(realdest)
    os.mkdir(realdest)
    sourcelist = os.listdir(realsource)
    #print(f"{sourcelist}")
    for item in sourcelist:
        realitem = os.path.join(realsource, item)
        #print(realitem)
        #print(f"isfile: {os.path.isfile(realitem)}  isdir: {os.path.isdir(realitem)}")
        if os.path.isfile(realitem):
            shutil.copy(realitem, realdest)
            #print(f"Copied {item} to {realdest}")
        elif os.path.isdir(realitem):
            itemsourcedir = os.path.join(realsource, item)
            itemdestdir = os.path.join(realdest, item)
            os.mkdir(itemdestdir)
            #print(f"Created directory {itemdestdir}")
            copy_directories(itemsourcedir, itemdestdir)
        else:
            pass
    

main()
