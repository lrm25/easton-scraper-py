from datetime import date, datetime
import ast
import os

from data.easton_class import EastonClass

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
IDX_CANCELLED = 10
IDX_DESCRIPTION_LINK = 11


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
    f.write("{}{}".format(easton_class.get_cancelled(), os.linesep))
    f.write("{}{}".format(easton_class.get_description_link(), os.linesep))

    f.close()


def delete_classes_done_before_now():

    files_to_delete = []
    now = datetime.now()

    for db_file in os.listdir("storage/db"):
        full_name = "storage/db/{}".format(db_file)
        with open(full_name, "r") as f:
            lines = f.readlines()
            if lines[IDX_DB_VERSION].strip() == str(DB_VERSION):
                class_end_time = datetime.strptime(lines[IDX_SORTABLE_END_TIME].strip(), "%Y-%m-%d %H:%M:%S")
                if class_end_time < now:
                    files_to_delete.append(full_name)

    for file_to_delete in files_to_delete:
        os.remove(file_to_delete)


def load(class_day_list):
    print(class_day_list)
    easton_classes = []
    for db_file in os.listdir("storage/db"):
        with open("storage/db/{}".format(db_file), "r") as f:
            lines = f.readlines()
            if lines[IDX_DB_VERSION].strip() == str(DB_VERSION):
                print(lines[IDX_DATE])
                if lines[IDX_DATE].strip() not in class_day_list:
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
                easton_class.set_cancelled(ast.literal_eval(lines[IDX_CANCELLED]))
                easton_class.set_description_link(lines[IDX_DESCRIPTION_LINK])
                easton_classes.append(easton_class)
    return easton_classes


def get_class_description_link(gym_name, class_id):
    db_string = "{}_{}.db".format(gym_name, class_id)
    for db_file in os.listdir("storage/db"):
        if db_file.lower() == db_string:
            with open("storage/db/{}".format(db_file), "r") as f:
                lines = f.readlines()
                description_link = lines[IDX_DESCRIPTION_LINK]
                break
    return description_link
