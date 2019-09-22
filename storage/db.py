from datetime import datetime
import os

from data.easton_class import easton_class_sort, EastonClass

DB_VERSION = 1

def write(easton_class):

    f = open("storage/db/{}.db".format(easton_class.get_id()), "w")
    f.write("{}{}".format(DB_VERSION, os.linesep))
    f.write("{}{}".format(easton_class.get_id(), os.linesep))
    f.write("{}{}".format(easton_class.get_name(), os.linesep))
    f.write("{}{}".format(easton_class.get_start_time(), os.linesep))
    f.write("{}{}".format(easton_class.get_end_time(), os.linesep))
    f.write("{}{}".format(easton_class.get_instructor(), os.linesep))
    f.write("{}{}".format(easton_class.get_sortable_start_time(), os.linesep))
    f.write("{}{}".format(easton_class.get_sortable_end_time(), os.linesep))

    f.close()

def load():
    print("*****")
    easton_classes = []
    for db_file in os.listdir("storage/db"):
        with open("storage/db/{}".format(db_file), "r") as f:
            lines = f.readlines()
            if lines[0].strip() == str(DB_VERSION):
                easton_class = EastonClass(lines[1].strip(),
                                           lines[2].strip(),
                                           lines[3].strip(),
                                           lines[4].strip())
                easton_class.set_instructor(lines[5].strip())
                easton_class.set_sortable_start_time(datetime.strptime(lines[6].strip(), "%Y-%m-%d %H:%M:%S"))
                easton_class.set_sortable_end_time(datetime.strptime(lines[7].strip(), "%Y-%m-%d %H:%M:%S"))
                easton_classes.append(easton_class)
    easton_classes.sort(key=easton_class_sort())
    for ec in easton_classes:
        print("{}, {}, {}, {}, {}".format(ec.get_id(), ec.get_name(), ec.get_start_time(),
                                          ec.get_end_time(), ec.get_instructor()))