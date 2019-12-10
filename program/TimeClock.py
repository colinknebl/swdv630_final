import time

class TimeClock:
    
    def __get_current_time(self):
        return time.time()

    current_time = property(__get_current_time, None, None)

    def __init__(self, pos):
        self.pos = pos

    def clock_in(self, employeeId, confirm=True):
        emp = self.pos.open_employees().get(id=employeeId)
        if emp:
            if confirm:
                user_input = input('Confirm %r clock in? (y/n) ' % (emp.name))
                if user_input == 'y':
                    emp.clock_in()
            else:
                emp.clock_in()
        

    def clock_out(self, employeeId, confirm=True):
        emp = self.pos.open_employees().get(id=employeeId)
        if emp:
            if confirm:
                user_input = input('Confirm %r clock out? (y/n) ' % (emp.name))
                if user_input == 'y':
                    emp.clock_out()
            else:
                emp.clock_out()

