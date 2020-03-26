from imports import *
from Management_prescription import *

class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''
    selected_row = NumericProperty(0)

    def get_nodes(self):
        nodes = self.get_selectable_nodes()
        if self.nodes_order_reversed:
            nodes = nodes[::-1]
        if not nodes:
            return None, None

        selected = self.selected_nodes
        if not selected:    # nothing selected, select the first
            self.select_node(nodes[0])
            self.selected_row = 0
            return None, None

        if len(nodes) == 1:     # the only selectable node is selected already
            return None, None

        last = nodes.index(selected[-1])
        self.clear_selection()
        return last, nodes

    def select_next(self):
        ''' Select next row '''
        last, nodes = self.get_nodes()
        if not nodes:
            return

        if last == len(nodes) - 1:
            self.select_node(nodes[0])
            self.selected_row = nodes[0]
        else:
            self.select_node(nodes[last + 1])
            self.selected_row = nodes[last + 1]

    def select_previous(self):
        ''' Select previous row '''
        last, nodes = self.get_nodes()
        if not nodes:
            return

        if not last:
            self.select_node(nodes[-1])
            self.selected_row = nodes[-1]
        else:
            self.select_node(nodes[last - 1])
            self.selected_row = nodes[last - 1]

    def select_current(self):
        ''' Select current row '''
        last, nodes = self.get_nodes()
        if not nodes:
            return

        self.select_node(nodes[self.selected_row])


class SelectableButton(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        

    def on_press(self,*args):
        select_patient = Manage_Prescription()
        select_patient.man_selected_patient()
        
class EditStatePopup(Popup):
    patient_id: ObjectProperty(None)
    patient_name:ObjectProperty(None)
    patient_email:ObjectProperty(None)
    patient_address:ObjectProperty(None)
    patient_fon:ObjectProperty(None)
    patient_sex:ObjectProperty(None)
    patient_dob:ObjectProperty(None)
    patient_age:ObjectProperty(None)
    patient_blood:ObjectProperty(None)
    

    def __init__(self, obj, **kwargs):
        super(EditStatePopup, self).__init__(**kwargs)
        self.obj = obj
        self.editpatient()

    def editpatient(self):
        
        c.execute("SELECT ID ,NAME , EMAIL, ADDRESS, PHONE, SEX , DOB, AGE, BLOOD FROM Patients  WHERE ID=?", (self.obj,))
        self.row_data = c.fetchone()

        self.patient_id.text=str(self.row_data[0])
        self.patient_name.text = self.row_data[1]
        self.patient_email.text = self.row_data[2]
        self.patient_address.text= self.row_data[3]
        self.patient_fon.text= str(self.row_data[4])
        self.patient_sex.text =  self.row_data[5]
        self.patient_dob.text = str(self.row_data[6])
        self.patient_age.text = str(self.row_data[7])
        self.patient_blood.text= self.row_data[8]
        
    def update(self):

        patient_id = self.patient_id.text
        name = self.patient_name.text
        email = self.patient_email.text
        address = self.patient_address.text
        fon = self.patient_fon.text
        sex = self.patient_sex.text
        dob = self.patient_dob.text
        age = self.patient_age.text
        blood = self.patient_blood.text
        
        c.execute(" UPDATE Patients SET ID =?, NAME=? , EMAIL=?, ADDRESS = ?, PHONE = ?, SEX = ? , DOB = ?, AGE = ?, BLOOD = ? WHERE ID =?",
                   (patient_id, name, email, address,fon, sex ,dob,age, blood, patient_id,))
        con.commit()
        callback = Patient_list()
        try:
            callback.refresh()
        except:
            print("popup_refresh error")

class Add_patient(GridLayout):
    patient_id: ObjectProperty(None)
    patient_name:ObjectProperty(None)
    patient_email:ObjectProperty(None)
    patient_address:ObjectProperty(None)
    patient_fon:ObjectProperty(None)
    patient_sex:ObjectProperty(None)
    patient_dob:ObjectProperty(None)
    patient_age:ObjectProperty(None)
    patient_blood:ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(Add_patient, self).__init__(**kwargs)
        self.create_table_patients()
        self.buildLists()
        
    def buildLists(self):
        c. execute("SELECT Class FROM classes")
        result = c.fetchall()
         
         
        self.pickType = [str(t[0]) for t in result]
        
    def regenerate(self):
        self.gen_patient_id()
    
    def gen_patient_id(self):
        gen = random.randint(500, 50000)
        c.execute("SELECT * FROM Patients WHERE ID = ?",(gen,))
        results = c.fetchall()
        
        if results:
            return self.regenerate()
        else:
            self.patient_id.text = str(gen)
            
                 
         
    def create_table_patients(self):
        try:
            c.execute("CREATE TABLE IF NOT EXISTS Patients (ID INT,NAME TEXT , EMAIL TEXT,ADDRESS TEXT,PHONE INT,SEX TEXT, DOB TEXT, AGE TEXT,BLOOD TEXT)")
            con.commit()
        except:
            print("Error")
            
    

    def insert_patients(self, **kwargs):
        patient_id = self.patient_id.text
        name = self.patient_name.text
        email = self.patient_email.text
        address = self.patient_address.text
        fon = self.patient_fon.text
        sex = self.patient_sex.text
        dob = self.patient_dob.text
        age = self.patient_age.text
        blood = self.patient_blood.text
        
        try:
            c.execute("INSERT INTO Patients(ID ,NAME , EMAIL,ADDRESS,PHONE,SEX , DOB, AGE,BLOOD) VALUES (?,?,?,?,?,?,?,?,?) " ,(patient_id,name,email,address,fon,sex,dob,age,blood) )
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
        if self.patient_name.text and self.patient_email.text and self.patient_address.text and self.patient_fon.text and self.patient_sex.text and self.patient_dob.text and self.patient_age.text and self.patient_blood.text:
            return self.insert_patients()
        else:
            return self.empty_popup()

    def empty_popup(self):
        self.content = Label(text=' All fields must be Filled correctly!!!')
        self.popup = Popup(title='Warning!!!!', content=self.content, size_hint=(.4, .3))
        self.popup.open()
        

class Patient_list(GridLayout):
    total_col_headings = NumericProperty(0)
    data_items = ListProperty([("?", "?", "?" ,"?", "?", "?" ,"?", "?", "?")])
    real_change = ObjectProperty(None)
    contoller = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(Patient_list, self).__init__(**kwargs)
        self.get_table_column_headings()
        self.get_Patients()
    
    def adding_patient(self):
        layout = Factory.Add_patient()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def patient_list(self):
        layout = Factory.Return_patientList()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        
    def man_selected_patient(self):
        
        layout = Factory.Selected_patient()
        
        self.ids['manage_selected'].clear_widgets()
        self.ids['manage_selected'].add_widget(layout)
        print("pressed")

    def get_table_column_headings(self):
        
        try:
            
            c.execute("PRAGMA table_info(Patients)")
            col_headings = c.fetchall()
            self.total_col_headings = 6
        except lite.Error:
            print('not connected')

    def get_Patients(self):
        
        
        c.execute("SELECT ID ,NAME , AGE ,SEX , BLOOD ,DOB FROM Patients ")
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
            self.get_Patients()
    
    def realtime_search(self):
        search = self.real_change.text
        
        search +='%'
        c.execute("SELECT ID ,NAME , AGE ,SEX , BLOOD ,DOB FROM Patients WHERE NAME LIKE ?  ", (search,))
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
        popup = EditStatePopup(self.row_data)
        popup.open()

    def refresh(self):
        
        call = App.get_running_app().root.screen_doctor.patient()
        return call()
        print('yes refreshed')
        