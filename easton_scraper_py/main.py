import sys

from ui import terminal


#
# main function
#
def main():
    try:
        terminal.parse(sys.argv[1:])
    except TypeError as err:
        print(err)


#
# if this module is called, run the main function (duh)
#
if __name__ == "__main__":
    main()

