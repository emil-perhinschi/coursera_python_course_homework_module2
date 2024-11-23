#!/usr/bin/env python

import os, sys, argparse


def read_files_in_folder(root_path: str, min_size: int):
    all_files = {} 
    for root, directories, files in os.walk(root_path):
        for _file in files:
            # print(f"File found: {root}/{_file}")
            full_path = os.path.join(root, _file)
            file_size = os.path.getsize(full_path)
            if file_size >= min_size:
                all_files[full_path] = file_size
        
    return all_files

def main():
    argparser = argparse.ArgumentParser(prog="file_finder")
    argparser.add_argument("folder", type=str, help = "Folder to look at")
    argparser.add_argument("-v", "--verbose", help="Verbose execution", action="store_true")
    argparser.add_argument("-c", "--count",  help = "How many files to list")
    argparser.add_argument("-s", "--size",   help = "Show only files larger than this in megabytes")
    args = argparser.parse_args()

    if args.folder and args.verbose:
        print(f"Folder is {args.folder}")

    min_size = 0
    if args.size is not None and int(args.size) > 0:
        min_size = int(args.size) * 1024 * 1024 # supplied size is in megabytes, os.path.getsize returns bytes

    all_files = read_files_in_folder(args.folder, min_size)
    files_count = len(all_files.keys())
    if args.verbose:
        print(f"Files count:{files_count}")

    sorted_file_list = []
    shown_files = 1
    if args.count is not None and int(args.count) > 0:
        for _file_path, _size in sorted(all_files.items(), key=lambda x:x[1], reverse=True):
            print(f"{shown_files} {_size/(1024*1024)} {_file_path}")
            if shown_files >= int(args.count):
                break

            shown_files += 1
main()


"""
example how to test the results using `find`

``` 
find /media/emilper/DATA2023/Documents/ -type f -size +100M | wc -l
```

"""
