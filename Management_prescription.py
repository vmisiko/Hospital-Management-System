from imports import *

class SelectableButton2(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton2, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton2, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        

    def on_press(self,*args):
        select_patient = Manage_Prescription()
        select_patient.man_selected_patient()
        
class EditPrescriptionPopup(Popup):
    
    appointment_id:ObjectProperty(None)
    appointment_doctor:ObjectProperty(None)
    appointment_patient:ObjectProperty(None)
    appointment_date:ObjectProperty(None)
    

    def __init__(self, obj, **kwargs):
        super(EditPrescriptionPopup, self).__init__(**kwargs)
        self.obj = obj
        self.editappointment()

    def editappointment(self):
        
        c.execute("SELECT ID ,NAME , DOCTOR, DATE FROM Appointments  WHERE ID=?", (self.obj,))
        self.row_data = c.fetchone()

        self.appointment_id.text=str(self.row_data[0])
        self.appointment_patient.text = self.row_data[1]
        self.appointment_doctor.text = self.row_data[2]
        self.appointment_date.text= self.row_data[3]
      
        
    def update(self):

        patient_id = self.appointment_id.text
        name = self.appointment_patient.text
        doctor = self.appointment_doctor.text
        date = self.appointment_date.text
        
        c.execute(" UPDATE Appointments SET ID =?, NAME=? , DOCTOR =?, DATE=? WHERE ID =?",
                   (patient_id, name, doctor,date,patient_id,))
        con.commit()
        callback = Appointment()
        try:
            callback.refresh()
        except:
            print("popup_refresh error")


   
class Doctor_dashboard(GridLayout):
    calendar = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(Doctor_dashboard, self).__init__(**kwargs)
        Clock.schedule_once(lambda *args: self.create_calendar())

    def create_calendar(self):
        self.cal = CalendarWidget()
        self.calendar.add_widget(self.cal)

class Manage_Prescription(GridLayout):
    total_col_headings = NumericProperty(0)
    data_items = ListProperty([("?", "?", "?" ,"?", "?", "?" ,"?", "?", "?")])
    real_change = ObjectProperty(None)

    
    #manage_selected:ObjectProperty(None)
    def __init__(self, **kwargs):
        super(Manage_Prescription, self).__init__(**kwargs)
        self.get_table_column_headings()
        self.get_appointments()
        #Clock.schedule_once(lambda *args: self.man_selected_patient())
    
    def adding_prescription(self):
        layout = Factory.Add_prescription()
        self.manage_prescription.clear_widgets()
        self.manage_prescription.add_widget(layout)
        
    def priscription_list(self):
        layout = Factory.Return_priscriptionList()
        self.manage_prescription.clear_widgets()
        self.manage_prescription.add_widget(layout)
        
    
    def man_selected_patient(self):
        
        layout = Factory.Selected_patient()
        
        self.ids['manage_selected'].clear_widgets()
        self.ids['manage_selected'].add_widget(layout)
        print("pressed")


    def get_table_column_headings(self):
        
        try:
            
            c.execute("PRAGMA table_info(Patients)")
            col_headings = c.fetchall()
            self.total_col_headings = 4
        except lite.Error:
            print('not connected')

    def get_appointments(self):
        
        
        c.execute("SELECT ID ,NAME , DOCTOR, DATE FROM Appointments ")
        rows = c.fetchall()

        # create list with db column, db primary key, and db column range
        data = []
        low = 0
        high = self.total_col_headings - 1

        for row in rows:
            for col in row:
                data.append([col, row[0], [low, high]])
            low += self.total_col_headings
            high += self.total_col_headings

        # create data_items
        self.data_items = [{'text': str(x[0]), 'Index': str(x[1]), 'range': x[2], 'selectable': True} for x in data]


        
    def realtime_select(self):
        search = self.real_change.text
        
        if search:
            return self.realtime_search()
        else:
            pass
    
    def realtime_search(self):
        search = self.real_change.text
        
        search +='%'
        c.execute("SELECT ID ,NAME , DOCTOR, DATE FROM Appointments WHERE NAME LIKE ?  ", (search,))
        rows = c.fetchall()

        # create list with db column, db primary key, and db column range
        data = []
        low = 0
        high = self.total_col_headings - 1

        for row in rows:
            for col in row:
                data.append([col, row[0], [low, high]])
            low += self.total_col_headings
            high += self.total_col_headings

        # create data_items
        self.data_items = [{'text': str(x[0]), 'Index': str(x[1]), 'range': x[2], 'selectable': True} for x in data]

       

    def popup_callback(self, instance):
        
        self.row_data  = self.data_items[instance.index]['Index']
        
        ''' Instantiate and Open Popup '''
        popup = EditPrescriptionPopup(self.row_data)
        popup.open()
        print('ok got it')

        
class Add_prescription(GridLayout):
    pass
class Return_priscriptionList(BoxLayout):
    pass