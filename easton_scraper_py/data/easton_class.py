

class EastonClass:

    def __init__(self, gym_name, id, name, date, start_time, end_time):
        self._id = id
        self._gym_name = gym_name
        self._name = name
        self._date = date
        self._start_time = start_time
        self._end_time = end_time
        self._instructor = ""
        self._sortable_start_time = ""
        self._sortable_end_time = ""
        self._cancelled = False
        self._description_link = ""
        self._description = ""

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

    def set_date(self, date):
        self._date = date

    def get_date(self):
        return self._date

    def get_gym_name(self):
        return self._gym_name

    def set_cancelled(self, cancelled):
        self._cancelled = cancelled

    def get_cancelled(self):
        return self._cancelled

    def set_description_link(self, description_link):
        self._description_link = description_link

    def get_description_link(self):
        return self._description_link

    def set_description(self, description):
        self._description = description

    def get_description(self):
        return self._description
