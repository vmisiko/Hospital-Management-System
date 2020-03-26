from imports import *
        
class ScreenLabaratorist(Screen):
    calendar = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(ScreenLabaratorist, self).__init__(**kwargs)
        Clock.schedule_once(lambda *args: self.create_calendar())

    def create_calendar(self):
        self.cal = CalendarWidget()
        self.calendar.add_widget(self.cal)

    def blood_bank(self):
        layout = Factory.Manage_Blood()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def blood_donor(self):
        layout = Factory.Manage_Donor()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def profile(self):
        layout = Factory.Manage_Profile()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def lab_dashboard(self):
        layout = Factory.Labdashboard()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

class Labdashboard(BoxLayout):
    calendar = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(Labdashboard, self).__init__(**kwargs)
        Clock.schedule_once(lambda *args: self.create_calendar())

    def create_calendar(self):
        self.cal = CalendarWidget()
        self.calendar.add_widget(self.cal)
