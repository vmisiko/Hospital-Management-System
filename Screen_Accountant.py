from imports import *


class ScreenAccountant(Screen):
    calendar = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(ScreenAccountant, self).__init__(**kwargs)
        Clock.schedule_once(lambda *args: self.create_calendar())

    def create_calendar(self):
        self.cal = CalendarWidget()
        self.calendar.add_widget(self.cal)
        
    def account_dashboard(self):
        layout = Factory.Accountantdashboard()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    
    def profile(self):
        layout = Factory.Manage_Profile()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)




class Accountantdashboard(BoxLayout):
    calendar = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(Accountantdashboard, self).__init__(**kwargs)
        Clock.schedule_once(lambda *args: self.create_calendar())

    def create_calendar(self):
        self.cal = CalendarWidget()
        self.calendar.add_widget(self.cal)

    
