import sys

from ui import terminal

def main():
    terminal.parse(sys.argv[1:])

if __name__ == "__main__":
    main()
