import sys

def load_paths():
    paths = ['../ui/','../data/','../storage']
    print(paths)
    for path in paths:
        sys.path.insert(0, path)
    print(sys.path)
