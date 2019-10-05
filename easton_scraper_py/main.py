import sys

from ui import terminal


#
# main function
#
def main():
    try:
        # we use argparse, so we don't need to pass the command line params in
        terminal.parse()
    except TypeError as err:
        print(err)


#
# if this module is called, run the main function (duh)
#
if __name__ == "__main__":
    main()

