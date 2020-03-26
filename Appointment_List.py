from imports import *
from Management_prescription import *


class SelectableButton1(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(SelectableButton1, self).__init__(**kwargs)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton1, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton1, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        

    def on_press(self,*args):
        select_patient = Manage_Prescription()
        select_patient.man_selected_patient()
        
class EditAppointmentPopup(Popup):
    appointment_id:ObjectProperty(None)
    appointment_doctor:ObjectProperty(None)
    appointment_patient:ObjectProperty(None)
    appointment_date:ObjectProperty(None)
    

    def __init__(self, obj, **kwargs):
        super(EditAppointmentPopup, self).__init__(**kwargs)
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



class Appointment(GridLayout):
    total_col_headings = NumericProperty(0)
    data_items = ListProperty([("?", "?", "?" ,"?", "?", "?" ,"?", "?", "?")])
    real_change = ObjectProperty(None)
    contoller = ObjectProperty(None)
    rv_id = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Appointment, self).__init__(**kwargs)
        self.get_table_column_headings()
        self.get_appointments()
        
    def adding_appointement(self):
        layout = Factory.Add_appointment()
        self.manage_appointment.clear_widgets()
        self.manage_appointment.add_widget(layout)

    def appointment_list(self):
        layout = Factory.Return_appointmentList()
        self.manage_appointment.clear_widgets()
        self.manage_appointment.add_widget(layout)

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

        print("yes refreshed")
    def realtime_select(self):
        search = self.real_change.text
        
        if search:
            return self.realtime_search()
        else:
            self.get_appointments()
    
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
        popup = EditAppointmentPopup(self.row_data)
        popup.open()
        print('ok got it')

    def refresh(self):
        
        self.rv_id.refresh_from_data()
        self.get_appointments()


class Add_appointment(GridLayout):
    appointment_id:ObjectProperty(None)
    appointment_doctor:ObjectProperty(None)
    appointment_patient:ObjectProperty(None)
    appointment_date:ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(Add_appointment, self).__init__(**kwargs)
        self.create_table_appointments()
        self.buildLists()
        
    def buildLists(self):
        c. execute("SELECT Name FROM Doctor ")
        result = c.fetchall()
        self.pickType = [str(t[0]) for t in result]
        if result:
            return self.pickType
        else:
            pass
    
   
                 
         
    def create_table_appointments(self):
        try:
            c.execute("CREATE TABLE IF NOT EXISTS Appointments (ID INT ,NAME TEXT , DOCTOR TEXT, DATE TEXT)")
            con.commit()
        except:
            print("Error")
            
    

    def insert_appointment(self, **kwargs):
        patient_id = self.appointment_id.text
        name = self.appointment_patient.text
        doctor = self.appointment_doctor.text
        date = self.appointment_date.text
        
        try:
            c.execute("INSERT INTO Appointments(ID ,NAME , DOCTOR, DATE) VALUES (?,?,?,?) " ,(patient_id,name,doctor,date) )
            con.commit()
            self.save_succefull()
            
        except lite.Error:
            return self.save_popup()
    def save_popup(self):
        self.content = Label(text=' Data not saved!!!')
        self.popup = Popup(title='Error!!!!', content=self.content,
                           size_hint=(.4, .3))
        self.popup.open()
        
    def save_succefull(self):
        self.content = Label(text=' Registration Successfull!!!!')
        self.popup = Popup(title='Applause!!', content=self.content,
                           size_hint=(.4, .3))
        self.popup.open()

    def  validateif(self):
        if self.appointment_id.text and self.appointment_patient.text and self.appointment_doctor.text and self.appointment_date.text:
            return self.insert_appointment()
        else:
            return self.empty_popup()

    def empty_popup(self):
        self.content = Label(text=' All fields must be Filled correctly!!!')
        self.popup = Popup(title='Warning!!!!', content=self.content, size_hint=(.4, .3))
        self.popup.open()
        
    def realtime_appointment_id(self):
        search = self.appointment_id.text
        
        #search +='%'
        c.execute("SELECT NAME  FROM Patients WHERE ID = ?  ", (search,))
        rows = c.fetchone()
        if rows:
            self.appointment_patient.text = str(rows[0])
        else:
            #print('error')
            self.appointment_patient.text = ""
            
        print(rows)

    def refresh(self):

        call = Appointment().refresh()
        return call
        print('yes refreshed')




