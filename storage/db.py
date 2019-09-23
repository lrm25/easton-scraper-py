from datetime import datetime
import os

from data.easton_class import easton_class_sort, EastonClass

DB_VERSION = 1

IDX_DB_VERSION = 0
IDX_GYM_NAME = 1
IDX_CLASS_ID = 2
IDX_NAME = 3
IDX_DATE = 4
IDX_START_TIME = 5
IDX_END_TIME = 6
IDX_INSTRUCTOR = 7
IDX_SORTABLE_START_TIME = 8
IDX_SORTABLE_END_TIME = 9


def write(easton_class):

    f = open("storage/db/{}_{}.db".format(easton_class.get_gym_name(), easton_class.get_id()), "w")
    f.write("{}{}".format(DB_VERSION, os.linesep))
    f.write("{}{}".format(easton_class.get_gym_name(), os.linesep))
    f.write("{}{}".format(easton_class.get_id(), os.linesep))
    f.write("{}{}".format(easton_class.get_name(), os.linesep))
    f.write("{}{}".format(easton_class.get_date(), os.linesep))
    f.write("{}{}".format(easton_class.get_start_time(), os.linesep))
    f.write("{}{}".format(easton_class.get_end_time(), os.linesep))
    f.write("{}{}".format(easton_class.get_instructor(), os.linesep))
    f.write("{}{}".format(easton_class.get_sortable_start_time(), os.linesep))
    f.write("{}{}".format(easton_class.get_sortable_end_time(), os.linesep))

    f.close()


def load(class_day_list):
    print("*****")
    print(class_day_list)
    easton_classes = []
    for db_file in os.listdir("storage/db"):
        with open("storage/db/{}".format(db_file), "r") as f:
            lines = f.readlines()
            if lines[IDX_DB_VERSION].strip() == str(DB_VERSION):
                if lines[IDX_CLASS_ID].strip() not in class_day_list:
                    continue

                easton_class = EastonClass(lines[IDX_GYM_NAME].strip(),
                                           lines[IDX_CLASS_ID].strip(),
                                           lines[IDX_NAME].strip(),
                                           lines[IDX_DATE].strip(),
                                           lines[IDX_START_TIME].strip(),
                                           lines[IDX_END_TIME].strip())
                easton_class.set_instructor(lines[IDX_INSTRUCTOR].strip())
                easton_class.set_sortable_start_time(datetime.strptime(lines[IDX_SORTABLE_START_TIME].strip(),
                                                                       "%Y-%m-%d %H:%M:%S"))
                easton_class.set_sortable_end_time(datetime.strptime(lines[IDX_SORTABLE_END_TIME].strip(),
                                                                     "%Y-%m-%d %H:%M:%S"))
                easton_classes.append(easton_class)
    easton_classes.sort(key=easton_class_sort())
    for ec in easton_classes:
        print("{}, {}, {}, {}, {}, {}".format(ec.get_gym_id(), ec.get_name(), ec.get_date(), ec.get_start_time(),
                                              ec.get_end_time(), ec.get_instructor()))
