def easton_class_sort():
    return lambda e : (e.get_sortable_start_time(), e.get_sortable_end_time())

class EastonClass:

    def __init__(self, id, name, start_time, end_time):
        self._id = id
        self._name = name
        self._start_time = start_time
        self._end_time = end_time
        self._instructor = ""
        self._sortable_start_time = ""
        self._sortable_end_time = ""

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_start_time(self):
        return self._start_time

    def get_end_time(self):
        return self._end_time

    def set_instructor(self, instructor):
        self._instructor = instructor

    def get_instructor(self):
        return self._instructor

    def set_sortable_start_time(self, sortable_start_time):
        self._sortable_start_time = sortable_start_time
    
    def get_sortable_start_time(self):
        return self._sortable_start_time
    
    def set_sortable_end_time(self, sortable_end_time):
        self._sortable_end_time = sortable_end_time
    
    def get_sortable_end_time(self):
        return self._sortable_end_time