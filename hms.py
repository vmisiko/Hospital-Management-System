
from imports import *
from Management_prescription import *
from  patientlist import *
from Appointment_List import *
from Screen_Accountant import *
from Screen_Labaratorist import *

class CustomDropDown(DropDown):
    pass



###################  Labaratorist ###################################
        
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

#################### Nurse ###############################################        
        
class ScreenNurse(Screen):
    state = BooleanProperty(False)
    calendar = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(ScreenNurse, self).__init__(**kwargs)
        Clock.schedule_once(lambda *args: self.create_calendar())
        
    def create_calendar(self):
        self.cal = CalendarWidget()
        self.calendar.add_widget(self.cal)

    def patient(self):
        layout = Factory.Patient_list()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
    def dashboard(self):
        layout = Factory.Doctor_dashboard()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def appointment_list(self):
        layout = Factory.Appointment()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        
    def prescription_list(self):
        layout = Factory.Manage_Prescription()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def allotment_list(self):
        layout = Factory.Bed_allotement()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
    def bed(self):
        layout = Factory.Manage_Bed()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        

    def blood_bank(self):
        layout = Factory.Manage_Blood()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def blood_donor(self):
        layout = Factory.Manage_Donor()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        
    def report_list(self):
        layout = Factory.Manage_Report()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def profile(self):
        layout = Factory.Manage_Profile()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def get_back_to_list(self):
        call = App.get_running_app().root.screen_nurse.patient()
        return call



################## reussable Classes ####################################
        
        
class Manage_Donor(GridLayout):
    def adding_donor(self):
        layout = Factory.Add_donor()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
        
    def return_donorList(self):
        layout = Factory.Return_donorList()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
class Add_donor(GridLayout):
    pass
class Return_donorList(BoxLayout):
    pass

class Manage_Bed(GridLayout):

    total_col_headings = NumericProperty(0)
    data_items = ListProperty([("?", "?", "?" ,"?", "?", "?" ,"?", "?", "?")])
    real_change = ObjectProperty(None)
    contoller = ObjectProperty(None)
    rv_id = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Manage_Bed, self).__init__(**kwargs)
        self.get_table_column_headings()
        self.get_beds()

    def adding_bed(self):
        layout = Factory.Add_bed()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)

    def return_bedList(self):
        layout = Factory.Return_bedList()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)

    def man_selected_patient(self):

        layout = Factory.Selected_patient()

        self.ids['manage_selected'].clear_widgets()
        self.ids['manage_selected'].add_widget(layout)
        print("pressed")

    def get_table_column_headings(self):

        try:

            c.execute("PRAGMA table_info(Beds)")
            col_headings = c.fetchall()
            self.total_col_headings = 3
        except lite.Error:
            print('not connected')

    def get_beds(self):

        c.execute("SELECT BED,ROOM, DESCRIPTION FROM Beds ")
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

        #print("yes refreshed")

    def realtime_select(self):
        search = self.real_change.text

        if search:
            return self.realtime_search()
        else:
            self.get_beds()

    def realtime_search(self):
        search = self.real_change.text

        search += '%'
        c.execute("SELECT BED,ROOM, DESCRIPTION FROM Beds WHERE ROOM LIKE ?  ", (search,))
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

        self.row_data = self.data_items[instance.index]['Index']

        ''' Instantiate and Open Popup '''
        popup = EditBedPopup(self.row_data)
        popup.open()
        print('ok got it')

    def refresh(self):

        self.rv_id.refresh_from_data()
        self.get_beds()


class Add_bed(GridLayout):
    bed_number=ObjectProperty(None)
    room_type= ObjectProperty(None)
    bed_description=ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Add_bed, self).__init__(**kwargs)
        self.create_table_beds()
        #self.buildLists()

    def buildLists(self):
        c.execute("SELECT Name FROM Doctor ")
        result = c.fetchall()
        self.pickType = [str(t[0]) for t in result]
        if result:
            return self.pickType
        else:
            pass

    def create_table_beds(self):
        try:
            c.execute("CREATE TABLE IF NOT EXISTS Beds (BED INT , ROOM TEXT , DESCRIPTION TEXT)")
            con.commit()
        except:
            print("Error")

    def insert_bed(self, **kwargs):
        bed = self.bed_number.text
        room = self.room_type.text
        description = self.bed_description.text

        try:
            c.execute("INSERT INTO Beds(BED,ROOM, DESCRIPTION) VALUES (?,?,?) ",
                      (bed, room,description, ))

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

    def validateif(self):
        if self.bed_number.text and self.room_type.text and self.bed_description.text:
            return self.insert_bed()
        else:
            return self.empty_popup()

    def empty_popup(self):
        self.content = Label(text=' All fields must be Filled correctly!!!')
        self.popup = Popup(title='Warning!!!!', content=self.content, size_hint=(.4, .3))
        self.popup.open()

    def realtime_bed_id(self):
        search = self.appointmen.text

        # search +='%'
        c.execute("SELECT NAME  FROM Patients WHERE ID = ?  ", (search,))
        rows = c.fetchone()
        if rows:
            self.appointment_patient.text = str(rows[0])
        else:
            # print('error')
            self.appointment_patient.text = ""

        print(rows)

    def refresh(self):

        call = Appointment().refresh()
        return call
        print('yes refreshed')


class SelectableButton_bed(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton_bed, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton_bed, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected


class EditBedPopup(Popup):
    bed_number = ObjectProperty(None)
    room_type = ObjectProperty(None)
    bed_description = ObjectProperty(None)

    def __init__(self, obj, **kwargs):
        super(EditBedPopup, self).__init__(**kwargs)
        self.obj = obj
        self.editbed()

    def editbed(self):

        c.execute("SELECT BED, ROOM,DESCRIPTION FROM Beds  WHERE BED=?",
                  (self.obj,))
        self.row_data = c.fetchone()

        self.bed_number.text = str(self.row_data[0])
        self.room_type.text = str(self.row_data[1])
        self.bed_description.text = str(self.row_data[2])



    def update(self):

        bed = self.bed_number.text
        room = self.room_type.text
        bed_description = self.bed_description.text

        c.execute(
            " UPDATE Beds SET BED=?, ROOM=?, DESCRIPTION =? WHERE BED =?",
            (bed, room, bed_description,bed ,))
        con.commit()
        callback = Manage_Bed()
        try:
            callback.refresh()
        except:
            print("popup_refresh error")


class Return_bedList(BoxLayout):
    pass


########################  Pharmascist ##########################################

 
class ScreenPharmascist(Screen):
    calendar = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(ScreenPharmascist, self).__init__(**kwargs)
        Clock.schedule_once(lambda *args: self.create_calendar())

    def create_calendar(self):
        self.cal = CalendarWidget()
        self.calendar.add_widget(self.cal)

    def medcategory(self):
        layout = Factory.Med_Category()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def med(self):
        layout = Factory.Manage_med()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def profile(self):
        layout = Factory.Manage_Profile()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def medprescription(self):
        layout = Factory.Manage_medprescription()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        
    def dashboard(self):
        layout = Factory.Pharmdashboard()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

############################### medicine cartegory #####################################

class Med_Category(GridLayout):
    total_col_headings = NumericProperty(0)
    data_items = ListProperty([("?", "?", "?", "?", "?", "?", "?", "?", "?")])
    real_change = ObjectProperty(None)
    contoller = ObjectProperty(None)
    rv_id = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Med_Category, self).__init__(**kwargs)
        self.get_table_column_headings()
        # self.create_table_patients()
        self.get_beds()


    def get_table_column_headings(self):

        try:

            c.execute("PRAGMA table_info(Medcategory)")
            col_headings = c.fetchall()
            print
            self.total_col_headings = len(col_headings)
        except lite.Error:
            print('not connected')

    def get_beds(self):

        c.execute("SELECT ID, NAME ,DESCRIPTION FROM Medcategory ")
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

        # print("yes refreshed")

    def realtime_select(self):
        search = self.real_change.text

        if search:
            return self.realtime_search()
        else:
            self.get_beds()

    def realtime_search(self):
        search = self.real_change.text

        search += '%'
        c.execute("SELECT ID, NAME ,DESCRIPTION FROM Medcategory WHERE NAME LIKE ?  ", (search,))
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

        self.row_data = self.data_items[instance.index]['Index']

        ''' Instantiate and Open Popup '''
        popup = EditMedcategoryPopup(self.row_data)
        popup.open()
        print('ok got it')

    def refresh(self):

        self.rv_id.refresh_from_data()
        self.get_beds()


class Add_medcategory(GridLayout):
    med_cat = ObjectProperty(None)
    med_description = ObjectProperty(None)


    def __init__(self, **kwargs):
        super(Add_medcategory, self).__init__(**kwargs)
        self.create_table_medcategory()
        self.buildLists()

    def buildLists(self):
        c.execute("SELECT Class FROM classes")
        result = c.fetchall()

        self.pickType = [str(t[0]) for t in result]



    def create_table_medcategory(self):
        try:
            c.execute(
                "CREATE TABLE IF NOT EXISTS Medcategory(ID INTEGER PRIMARY KEY AUTOINCREMENT ,NAME TEXT NOT NULL, DESCRIPTION TEXT NOT NULL)")
            con.commit()
        except:
            print("Error")

    def insert_medcategory(self, **kwargs):
        # patient_id = self.patient_id.text
        name = self.med_cat.text
        descr = self.med_description.text


        try:
            c.execute(
                "INSERT INTO Medcategory( NAME , DESCRIPTION) VALUES (?,?) ",
                (name, descr))
            con.commit()
            self.save_succefull()

        except lite.Error:
            print(lite.Error)
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

    def validateif(self):
        if self.med_description.text and self.med_cat.text:
            return self.insert_medcategory()
        else:
            return self.empty_popup()

    def empty_popup(self):
        self.content = Label(text=' All fields must be Filled correctly!!!')
        self.popup = Popup(title='Warning!!!!', content=self.content, size_hint=(.4, .3))
        self.popup.open()


class SelectableButton_medcategory(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton_medcategory, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton_medcategory, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected


class EditMedcategoryPopup(Popup):
    cat_id = ObjectProperty(None)
    med_cat = ObjectProperty(None)
    med_description = ObjectProperty(None)

    def __init__(self, obj, **kwargs):
        super(EditMedcategoryPopup, self).__init__(**kwargs)
        self.obj = obj
        self.editpatient()

    def editpatient(self):

        c.execute("SELECT ID ,NAME , DESCRIPTION FROM Medcategory  WHERE ID=?",
                  (self.obj,))
        self.row_data = c.fetchone()

        self.cat_id.text = str(self.row_data[0])
        self.med_cat.text = self.row_data[1]
        self.med_description.text = self.row_data[2]

    def update(self):


        id = self.cat_id.text
        name = self.med_cat.text
        descr = self.med_description.text


        c.execute(
            " UPDATE Medcategory SET ID = ?, NAME=?, DESCRIPTION = ? WHERE NAME = ?",
            (id,name, descr, name))

        con.commit()
        callback = Med_Category()

        try:
            callback.refresh()

        except:

            print("popup_refresh error")

##################################### Manage medicine #####################


class Manage_med(GridLayout):
    total_col_headings = NumericProperty(0)
    data_items = ListProperty([("?", "?", "?", "?", "?", "?", "?", "?", "?")])
    real_change = ObjectProperty(None)
    contoller = ObjectProperty(None)
    rv_id = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Manage_med, self).__init__(**kwargs)
        self.get_table_column_headings()
        #self.create_table_patients()
        self.get_beds()


    def get_table_column_headings(self):

        try:

            c.execute("PRAGMA table_info(Medine)")
            col_headings = c.fetchall()
            print
            self.total_col_headings = len(col_headings)
        except lite.Error:
            print('not connected')

    def get_beds(self):

        c.execute(" SELECT ID, NAME, DESCRIPTION, PRICE, MANUFACTURER, STATUS FROM Medicine ")
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

        # print("yes refreshed")


    def realtime_select(self):
        search = self.real_change.text

        if search:
            return self.realtime_search()
        else:
            self.get_beds()

    def realtime_search(self):
        search = self.real_change.text

        search += '%'
        c.execute("SELECT ID, NAME , DESCRIPTION, PRICE, MANUFACTURER, STATUS FROM Medicine WHERE NAME LIKE ?  ", (search,))
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

        self.row_data = self.data_items[instance.index]['Index']

        ''' Instantiate and Open Popup '''
        popup = EditMedicinePopup(self.row_data)
        popup.open()
        print('ok got it')

    def refresh(self):

        self.rv_id.refresh_from_data()
        self.get_beds()


class Add_med(GridLayout):
    med_name = ObjectProperty(None)
    med_cat = ObjectProperty(None)
    med_description = ObjectProperty(None)
    med_price = ObjectProperty(None)
    med_status = ObjectProperty(None)
    med_manufacturer = ObjectProperty(None)


    def __init__(self, **kwargs):
        super(Add_med, self).__init__(**kwargs)
        self.create_table_medcategory()
        self.buildLists()

    def buildLists(self):
        c.execute("SELECT NAME FROM Medcategory")
        result = c.fetchall()
        #print(result)
        self.pickType = [str(t[0]) for t in result]
        #print(self.pickType)


    def create_table_medcategory(self):
        try:
            c.execute(
                "CREATE TABLE IF NOT EXISTS Medicine(ID INTEGER PRIMARY KEY AUTOINCREMENT ,NAME TEXT NOT NULL,CATEGORY TEXT NOT NULL, DESCRIPTION TEXT NOT NULL, PRICE TEXT NOT NULL, MANUFACTURER TEXT NOT NULL, QUANTITY INT NOT NULL,STATUS TEXT NOT NULL  )")
            con.commit()
        except:
            print("Error")

    def insert_medcategory(self, **kwargs):

        name = self.med_name.text
        cat = self.med_cat.text
        descr = self.med_description.text
        price = self.med_price.text
        manufacturer = self.med_manufacturer.text
        qty = self.med_status.text

        status = ''
        if int(qty) > 0:
            status  = 'Available'
        else:
            status = 'Not Available'

        try:
            c.execute(
                "INSERT INTO Medicine( NAME , CATEGORY, DESCRIPTION, PRICE, MANUFACTURER, QUANTITY , STATUS) VALUES (?,?,?,?,?,?,?) ",
                (name,cat,  descr, price, manufacturer, qty, status))

            con.commit()

            self.save_succefull()

        except lite.Error:
            print(lite.Error)
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

    def validateif(self):

        if self.med_description.text and self.med_cat.text:
            return self.insert_medcategory()
        else:
            return self.empty_popup()

    def empty_popup(self):
        self.content = Label(text=' All fields must be Filled correctly!!!')
        self.popup = Popup(title='Warning!!!!', content=self.content, size_hint=(.4, .3))
        self.popup.open()


class SelectableButton_medicine(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton_medicine, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton_medicine, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected


class EditMedicinePopup(Popup):
    med_id= ObjectProperty(None)
    med_name = ObjectProperty(None)
    med_cat = ObjectProperty(None)
    med_description = ObjectProperty(None)
    med_price = ObjectProperty(None)
    med_status = ObjectProperty(None)
    med_manufacturer = ObjectProperty(None)


    def __init__(self, obj, **kwargs):
        super(EditMedicinePopup, self).__init__(**kwargs)
        self.obj = obj
        self.editpatient()

    def editpatient(self):

        c.execute("SELECT ID, NAME , CATEGORY, DESCRIPTION, PRICE, MANUFACTURER, QUANTITY  FROM Medicine  WHERE ID=?",
                  (self.obj,))

        self.row_data = c.fetchone()

        self.med_id.text = str(self.row_data[0])
        self.med_name.text = str(self.row_data[1])
        self.med_cat.text = str(self.row_data[2])
        self.med_description.text = str(self.row_data[3])
        self.med_price.text = str(self.row_data[4])
        self.med_manufacturer.text = str(self.row_data[5])
        self.med_status.text = str(self.row_data[6])



    def update(self):

        name = self.med_name.text
        cat = self.med_cat.text
        descr = self.med_description.text
        price = self.med_price.text
        manufacturer = self.med_manufacturer.text
        qty = self.med_status.text

        status = ''
        if int(qty) > 0:
            status = 'Available'
        else:
            status = 'Not Available'

        try:
            c.execute(
                "INSERT INTO Medicine( NAME , CATEGORY, DESCRIPTION, PRICE, MANUFACTURER, QUANTITY , STATUS) VALUES (?,?,?,?,?,?,?) ",
                (name, cat, descr, price, manufacturer, qty, status))

            con.commit()
            callback = Manage_med()
            callback.refresh()

        except:

            print("popup_refresh error")
#################################################################

class Pharmdashboard(GridLayout):
    calendar = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(Pharmdashboard, self).__init__(**kwargs)
        Clock.schedule_once(lambda *args: self.create_calendar())

    def create_calendar(self):
        self.cal = CalendarWidget()
        self.calendar.add_widget(self.cal)


class Manage_medprescription(GridLayout):
    def adding_prescription(self):
        layout = Factory.Add_medprescription()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
        
    def return_medprescriptionList(self):
        layout = Factory.Return_medprescriptionList()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
class Add_medprescription(GridLayout):
    pass

class Return_medprescriptionList(BoxLayout):
    pass


################# Admin ##############################################

class ScreenAdmin(Screen):
    state = BooleanProperty(False)
    calendar = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(ScreenAdmin, self).__init__(**kwargs)
        Clock.schedule_once(lambda *args: self.create_calendar())
        

    def create_calendar(self):
        self.cal = CalendarWidget()
        self.calendar.add_widget(self.cal)

    def patient(self):
        layout = Factory.Patient_list()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
    def dashboard(self):
        layout = Factory.Doctor_dashboard()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def appointment_list(self):
        layout = Factory.Appointment()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        
    def prescription_list(self):
        layout = Factory.Manage_Prescription()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def allotment_list(self):
        layout = Factory.Bed_allotement()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def blood_bank(self):
        layout = Factory.Manage_Blood()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        
    def report_list(self):
        layout = Factory.Manage_Report()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def profile(self):
        layout = Factory.Manage_Profile()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        
    def department_list(self):
        layout = Factory.Manage_department()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def doctor_list(self):
        layout = Factory.Manage_doctor()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def nurse_list(self):
        layout = Factory.Manage_nurse()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)  


    def pharm_list(self):
        layout = Factory.Manage_pharm()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)  

    def lab_list(self):
        layout = Factory.Manage_Lab()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        
    def accountant_list(self):
        layout = Factory.Manage_Accountant()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        

class Manage_department(GridLayout):
    def adding_deparment(self):
        layout = Factory.Add_department()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
        
    def return_departmentList(self):
        layout = Factory.Return_departmentList()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
  


class Add_department(GridLayout):
    pass

class Return_departmentList(BoxLayout):
    pass
class Manage_doctor(GridLayout):
    def adding_doctor(self):
        layout = Factory.Add_doctor()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
        
    def return_doctorList(self):
        layout = Factory.Return_doctorList()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
class Add_doctor(GridLayout):
    pass

class Return_doctorList(BoxLayout):
    pass

class Manage_nurse(GridLayout):
    def adding_nurse(self):
        layout = Factory.Add_nurse()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
        
    def return_nurseList(self):
        layout = Factory.Return_nurseList()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
class Add_nurse(GridLayout):
    pass

class Return_nurseList(BoxLayout):
    pass

class Manage_pharm(GridLayout):
    def adding_pharm(self):
        layout = Factory.Add_pharm()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
        
    def return_pharmList(self):
        layout = Factory.Return_pharmList()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
class Add_pharm(GridLayout):
    pass

class Return_pharmList(BoxLayout):
    pass

class Manage_Lab(GridLayout):
    def adding_lab(self):
        layout = Factory.Add_lab()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
        
    def return_labList(self):
        layout = Factory.Return_labList()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
class Add_lab(GridLayout):
    pass

class Return_labList(BoxLayout):
    pass


################### manage accountx ##############################

class Manage_Accountant(GridLayout):
    def adding_accountant(self):
        layout = Factory.Add_accountant()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
        
    def return_accountantList(self):
        layout = Factory.Return_accountantList()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)
class Add_accountant(GridLayout):
    pass

class Return_accountantList(BoxLayout):
    pass
################ Doctor ###########################

class ScreenDoctor(Screen):
    calendar = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(ScreenDoctor, self).__init__(**kwargs)
        Clock.schedule_once(lambda *args: self.create_calendar())

    def create_calendar(self):
        self.cal = CalendarWidget()
        self.calendar.add_widget(self.cal)

    def patient(self):
        layout = Factory.Patient_list()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        
    def dashboard(self):
        layout = Factory.Doctor_dashboard()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def appointment_list(self):
        layout = Factory.Appointment()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        
    def prescription_list(self):
        layout = Factory.Manage_Prescription()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def allotment_list(self):
        layout = Factory.Bed_allotement()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def blood_bank(self):
        layout = Factory.Manage_Blood()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        
    def report_list(self):
        layout = Factory.Manage_Report()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

    def profile(self):
        layout = Factory.Manage_Profile()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        
    def patient_select(self):
        
        layout = Factory.Selected_patient()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)
        print("pressed")
        
    def reallotment_list(self):
        layout = Factory.Return_allotmentList()
        self.manage_prescription.clear_widgets()
        self.manage_prescription.add_widget(layout)

    def adding_Allotment(self):
        layout = Factory.Add_allotment()
        self.manage_prescription.clear_widgets()
        self.manage_prescription.add_widget(layout)

    
        
########################## bed allotment selectable buttons ############

class SelectableButton_allotment(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(SelectableButton_allotment, self).__init__(**kwargs)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton_allotment, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton_allotment, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

    def on_press(self, *args):
        select_patient = Manage_Prescription()
        select_patient.man_selected_patient()


class EditAllotmentPopup(Popup):
    patient_id = ObjectProperty(None)
    patient_name = ObjectProperty(None)
    room_type = ObjectProperty(None)
    room = ObjectProperty(None)
    bed_no = ObjectProperty(None)
    alloc_time = ObjectProperty(None)

    def __init__(self, obj, **kwargs):
        super(EditAllotmentPopup, self).__init__(**kwargs)
        self.obj = obj
        self.editallocation()

    def editallocation(self):

        c.execute("SELECT * FROM Allotment  WHERE ID=?", (self.obj,))
        self.row_data = c.fetchone()

        self.patient_id.text = str(self.row_data[0])
        self.patient_name.text = self.row_data[1]
        self.room_type.text = self.row_data[2]
        self.room_no.text = self.row_data[3]
        self.bed_no.text = self.row_data[4]
        self.alloc_time.text = self.row_data[5]

    def update(self):

        patient_id =  self.patient_id.text
        name = self.patient_name.text
        room_type = self.room_type.text
        room_no = self.room_no.text
        bed = self.bed_no.text
        alloc_time = self.alloc_time.text

        c.execute(" UPDATE Allotment SET ID =?, NAME=? , ROOM_TYPE=?, ROOM_NUMBER =?, BED_NUMBER=?, ALLOCATION_TIME=? WHERE ID =? ", (patient_id, name, room_type, room_no, bed, alloc_time, patient_id,))
        con.commit()
        callback = Bed_allotement()
        try:
            callback.allotment_list()
        except:
            print("popup_refresh error")


class Bed_allotement(GridLayout):
    total_col_headings = NumericProperty(0)
    data_items = ListProperty([("?", "?", "?", "?", "?", "?", "?", "?", "?")])
    real_change = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Bed_allotement, self).__init__(**kwargs)
        self.get_table_column_headings()
        self.get_allocations()

    def adding_Allotment(self):
        layout = Factory.Add_allotment()
        self.manage_prescription.clear_widgets()
        self.manage_prescription.add_widget(layout)

    def allotment_list(self):
        call = App.get_running_app().root.screen_doctor.allotment_list
        return call()



    def get_table_column_headings(self):

        try:

            c.execute("PRAGMA table_info(Allotment)")
            col_headings = c.fetchall()
            self.total_col_headings = 5
        except lite.Error:
            print('not connected')

    def get_allocations(self):

        c.execute("SELECT ID,NAME , ROOM_TYPE, ALLOCATION_TIME FROM Allotment")
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
            self.get_allocations()

    def realtime_search(self):
        search = self.real_change.text

        search += '%'
        c.execute("SELECT ID ,NAME , ROOM_TYPE, ALLOCATION_TIME FROM Allotment WHERE NAME LIKE ?  ", (search,))
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

        self.row_data = self.data_items[instance.index]['Index']

        ''' Instantiate and Open Popup '''
        popup = EditAllotmentPopup(self.row_data)
        popup.open()

    def refresh(self):

        call = App.get_running_app().root.screen_doctor.allotment_list()
        return call()
        print('yes refreshed')


class Add_allotment(GridLayout):
    patient_id = ObjectProperty(None)
    patient_name = ObjectProperty(None)
    room_type = ObjectProperty(None)
    room = ObjectProperty(None)
    bed_no= ObjectProperty(None)
    alloc_time = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Add_allotment, self).__init__(**kwargs)
        self.create_table_allotment()



    def create_table_allotment(self):
        try:
            c.execute("CREATE TABLE IF NOT EXISTS Allotment(ID INT ,NAME TEXT , ROOM_TYPE TEXT, ROOM_NUMBER TEXT, BED_NUMBER TEXT, ALLOCATION_TIME TEXT)")
            con.commit()
        except:
            print("Error")

    def insert_allotment(self, **kwargs):
        patient_id = self.patient_id.text
        name = self.patient_name.text
        room_type = self.room_type.text
        room_no = self.room_no.text
        bed = self.bed_no.text
        date = self.alloc_time.text


        try:
            c.execute("INSERT INTO Allotment(ID ,NAME , ROOM_TYPE,ROOM_NUMBER, BED_NUMBER, ALLOCATION_TIME) VALUES (?,?,?,?,?,?) ",
                      (patient_id, name, room_type, room_no, bed, date))
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
        self.content = Label(text=' Allocation Successfull!!!!')
        self.popup = Popup(title='Applause!!', content=self.content,
                           size_hint=(.4, .3))
        self.popup.open()

    def validateif(self):
        if self.patient_id.text and self.patient_name.text and self.room_type.text and  self.room_no.text and self.bed_no.text and self.alloc_time.text:
            return self.insert_allotment()
        else:
            return self.empty_popup()

    def empty_popup(self):
        self.content = Label(text=' All fields must be Filled correctly!!!')
        self.popup = Popup(title='Warning!!!!', content=self.content, size_hint=(.4, .3))
        self.popup.open()

################################ Manage report #################################################################################

class Manage_Report(GridLayout):
    total_col_headings = NumericProperty(0)
    data_items = ListProperty([("?")])
    search_op = ObjectProperty(None)
    search_birth = ObjectProperty(None)
    search_death = ObjectProperty(None)
    data_birth = ListProperty([("?")])
    data_death = ListProperty([("?")])

    def __init__(self, **kwargs):
        super(Manage_Report, self).__init__(**kwargs)
        self.get_table_column_headings()
        self.get_report()
        self.get_report_death()
        self.get_report_birth()

    def adding_report(self):
        layout = Factory.Add_Report()
        self.manage_prescription.clear_widgets()
        self.manage_prescription.add_widget(layout)


    def Report_list(self):
        layout = Factory.Return_reportList()
        self.manage_prescription.clear_widgets()
        self.manage_prescription.add_widget(layout)


    def get_table_column_headings(self):

        try:

            c.execute("PRAGMA table_info(Report)")
            col_headings = c.fetchall()
            self.total_col_headings = 6
        except lite.Error:
            print('not connected')

    def get_report_death(self):

        c.execute(
            "SELECT ID,REPORT_DESCRIPTION, DATE , PATIENT_NAME, REPORT_DOCTOR FROM Report WHERE REPORT_TYPE = 'Death' ")
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
        self.data_death = [{'text': str(x[0]), 'Index': str(x[1]), 'range': x[2], 'selectable': True} for x in data]
        self.ids.rv.refresh_from_data()

    def get_report_birth(self):

        c.execute(
            "SELECT ID,REPORT_DESCRIPTION, DATE , PATIENT_NAME, REPORT_DOCTOR FROM Report WHERE REPORT_TYPE = 'Birth' ")
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
        self.data_birth = [{'text': str(x[0]), 'Index': str(x[1]), 'range': x[2], 'selectable': True} for x in data]
        self.ids.rv.refresh_from_data()

    def realtime_search_birth(self):
        search = self.search_birth.text

        search += '%'
        c.execute(
            "SELECT ID,REPORT_DESCRIPTION, DATE , PATIENT_NAME, REPORT_DOCTOR  FROM Report WHERE PATIENT_NAME Like ? AND REPORT_TYPE = 'Birth' ",
            (search,))
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
        self.data_birth = [{'text': str(x[0]), 'Index': str(x[1]), 'range': x[2], 'selectable': True} for x in data]
        self.ids.rv.refresh_from_data()

    def realtime_select(self):
        search = self.search_death.text

        if search:
            return self.realtime_search_death()
        else:
            print('nothing')

    def realtime_search_death(self):
        search = self.search_death.text

        search += '%'
        c.execute(
            "SELECT ID,REPORT_DESCRIPTION, DATE , PATIENT_NAME, REPORT_DOCTOR  FROM Report WHERE PATIENT_NAME Like ? AND REPORT_TYPE = 'Death' ",
            (search,))
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
        self.data_death = [{'text': str(x[0]), 'Index': str(x[1]), 'range': x[2], 'selectable': True} for x in data]
        self.ids.rv.refresh_from_data()

    def realtime_select(self):
        search = self.real_change.text

        if search:
            return self.realtime_search()
        else:
            self.refresh

    def realtime_search_op(self):
        search = self.search_op.text

        search += '%'
        c.execute(
            "SELECT ID,REPORT_DESCRIPTION, DATE , PATIENT_NAME, REPORT_DOCTOR  FROM Report WHERE PATIENT_NAME Like ?  ",
            (search,))
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
        self.ids.rv.refresh_from_data()

    def get_report(self):

        c.execute("SELECT ID,REPORT_DESCRIPTION, DATE , PATIENT_NAME, REPORT_DOCTOR FROM Report")
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

        self.row_data = self.data_items[instance.index]['Index']

        ''' Instantiate and Open Popup '''
        popup = EditReportPopup(self.row_data)
        popup.open()

    def refresh(self):

        call = App.get_running_app().root.screen_doctor.report_list()
        return call



class Add_Report(GridLayout):

    patient_id = ObjectProperty(None)
    report_patient = ObjectProperty(None)
    report_type = ObjectProperty(None)
    report_doctor=ObjectProperty(None)
    report_date = ObjectProperty(None)
    report_description = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Add_Report, self).__init__(**kwargs)
        self.create_table_Report()

    def create_table_Report(self):
        try:
            c.execute("CREATE TABLE IF NOT EXISTS Report(ID INT ,PATIENT_NAME TEXT , REPORT_TYPE TEXT, REPORT_DOCTOR TEXT,REPORT_DESCRIPTION TEXT,  DATE TEXT)")
            con.commit()

        except:
            print("Error")

    def insert_report(self, **kwargs):

        patient_id = self.patient_id.text
        patient = self.report_patient.text
        report_type = self.report_type.text
        doctor = self.report_doctor.text
        date = self.report_date.text
        descr = self.report_description.text

        try:
            c.execute("INSERT INTO Report(ID ,PATIENT_NAME, REPORT_TYPE, REPORT_DOCTOR, DATE, REPORT_DESCRIPTION) VALUES (?,?,?,?,?,?) ",
                    (patient_id,patient, report_type, doctor, date , descr))
            con.commit()
            self.save_succefull()

        except lite.Error:
            self.save_popup()


    def save_popup(self):
        self.content = Label(text=' Data not saved!!!')
        self.popup = Popup(title='Error!!!!', content=self.content,
                           size_hint=(.4, .3))
        self.popup.open()

    def save_succefull(self):
        self.content = Label(text=' Allocation Successfull!!!!')
        self.popup = Popup(title='Applause!!', content=self.content,
                           size_hint=(.4, .3))
        self.popup.open()

    def validateif(self):
        if self.patient_id.text and self.report_patient.text and self.report_type.text and self.report_description.text and self.report_date.text and self.report_doctor.text:
            return self.insert_report()
        else:
            return self.empty_popup()

    def empty_popup(self):
        self.content = Label(text=' All fields must be Filled correctly!!!')
        self.popup = Popup(title='Warning!!!!', content=self.content, size_hint=(.4, .3))
        self.popup.open()


class SelectableButton_Report(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(SelectableButton_Report, self).__init__(**kwargs)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton_Report, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton_Report, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected


class EditReportPopup(Popup):
    patient_id = ObjectProperty(None)
    report_patient = ObjectProperty(None)
    report_type = ObjectProperty(None)
    report_doctor = ObjectProperty(None)
    report_date = ObjectProperty(None)
    report_description = ObjectProperty(None)

    def __init__(self, obj, **kwargs):
        super(EditReportPopup, self).__init__(**kwargs)
        self.obj = obj
        self.editallocation()

    def editallocation(self):

        c.execute("SELECT * FROM  Report WHERE ID=?", (self.obj,))
        self.row_data = c.fetchone()
        self.patient_id.text = str(self.row_data[0])
        self.report_patient.text = self.row_data[1]
        self.report_type.text = self.row_data[2]
        self.report_doctor.text = self.row_data[3]
        self.report_date.text = self.row_data[4]
        self.report_description.text = self.row_data[5]

    def update(self):

        patient_id = self.patient_id.text
        name = self.report_patient.text
        report_type = self.report_type.text
        report_doctor = self.report_doctor.text
        report_date = self.report_date.text
        report_decr = self.report_description.text

        c.execute(
            " UPDATE Report SET ID =?,PATIENT_NAME=?, REPORT_TYPE=?, REPORT_DOCTOR = ?, DATE= ?, REPORT_DESCRIPTION= ? WHERE ID =? ",
            (patient_id, name, report_type, report_doctor, report_date, report_decr, patient_id,))
        con.commit()
        callback = Manage_Report()
        try:
            return callback.refresh()
        except:
            print("popup_refresh error")

################################################# manage Blood ###############################



class Manage_Blood(GridLayout):
    pass
    total_col_headings = NumericProperty(0)
    data_items = ListProperty([("?", "?", "?" ,"?", "?", "?" ,"?", "?", "?")])
    real_change = ObjectProperty(None)
    contoller = ObjectProperty(None)
    rv_id = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Manage_Blood, self).__init__(**kwargs)
        self.get_table_column_headings()
        #self.create_table_patients()
        self.get_beds()


    def create_table_patients(self):
        try:
            c.execute(
                "CREATE TABLE IF NOT EXISTS BloodBank(ID INTEGER PRIMARY KEY AUTOINCREMENT ,NAME TEXT NOT NULL, EMAIL TEXT NOT NULL,ADDRESS TEXT NOT NULL,PHONE INT NOT NULL,SEX TEXT NOT NULL, AGE TEXT NOT NULL,BLOOD TEXT NOT NULL, LAST_DONATED TEXT NOT NULL)")
            con.commit()
        except:
            print("Error")
    def adding_bed(self):
        layout = Factory.Add_blood()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)

    def return_bedList(self):
        layout = Factory.Return_bedList()
        self.manage_adding.clear_widgets()
        self.manage_adding.add_widget(layout)

    def man_selected_patient(self):

        layout = Factory.Selected_patient()

        self.ids['manage_selected'].clear_widgets()
        self.ids['manage_selected'].add_widget(layout)
        print("pressed")

    def get_table_column_headings(self):

        try:

            c.execute("PRAGMA table_info(BloodBank)")
            col_headings = c.fetchall()
            self.total_col_headings = 6
        except lite.Error:
            print('not connected')

    def get_beds(self):

        c.execute("SELECT ID, NAME ,SEX ,AGE, BLOOD, LAST_DONATED FROM BloodBank ")
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

        #print("yes refreshed")

    def realtime_select(self):
        search = self.real_change.text

        if search:
            return self.realtime_search()
        else:
            self.get_beds()

    def realtime_search(self):
        search = self.real_change.text

        search += '%'
        c.execute("SELECT ID, NAME , SEX,AGE, BLOOD, LAST_DONATED FROM BloodBank WHERE NAME LIKE ?  ", (search,))
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

        self.row_data = self.data_items[instance.index]['Index']

        ''' Instantiate and Open Popup '''
        popup = EditBloodPopup(self.row_data)
        popup.open()
        print('ok got it')


    def refresh(self):

        self.rv_id.refresh_from_data()
        self.get_beds()


class Add_blood(GridLayout):
    #patient_id: ObjectProperty(None)
    patient_name= ObjectProperty(None)
    patient_email= ObjectProperty(None)
    patient_address= ObjectProperty(None)
    patient_fon = ObjectProperty(None)
    patient_sex= ObjectProperty(None)
    patient_dob= ObjectProperty(None)
    patient_age= ObjectProperty(None)
    patient_blood= ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Add_blood, self).__init__(**kwargs)
        self.create_table_patients()
        self.buildLists()

    def buildLists(self):
        c.execute("SELECT Class FROM classes")
        result = c.fetchall()

        self.pickType = [str(t[0]) for t in result]

    def regenerate(self):
        self.gen_patient_id()

    def gen_patient_id(self):
        gen = random.randint(500, 50000)
        c.execute("SELECT * FROM Patients WHERE ID = ?", (gen,))
        results = c.fetchall()

        if results:
            return self.regenerate()
        else:
            self.patient_id.text = str(gen)

    def create_table_patients(self):
        try:
            c.execute(
                "CREATE TABLE IF NOT EXISTS BloodBank(ID INTEGER PRIMARY KEY AUTOINCREMENT ,NAME TEXT NOT NULL, EMAIL TEXT NOT NULL,ADDRESS TEXT NOT NULL,PHONE INT NOT NULL,SEX TEXT NOT NULL, AGE TEXT NOT NULL,BLOOD TEXT NOT NULL, LAST_DONATED TEXT NOT NULL)")
            con.commit()
        except:
            print("Error")

    def insert_patients(self, **kwargs):
        #patient_id = self.patient_id.text
        name = self.patient_name.text
        email = self.patient_email.text
        address = self.patient_address.text
        fon = self.patient_fon.text
        sex = self.patient_sex.text
        dob = self.patient_dob.text
        age = self.patient_age.text
        blood = self.patient_blood.text

        try:
            c.execute(
                    "INSERT INTO BloodBank( NAME , EMAIL,ADDRESS,PHONE,SEX, AGE,BLOOD, LAST_DONATED) VALUES (?,?,?,?,?,?,?,?) ",
                    ( name, email, address, fon, sex, age,blood, dob))
            con.commit()
            self.save_succefull()

        except lite.Error:
            print(lite.Error)
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

    def validateif(self):
        if self.patient_name.text and self.patient_email.text and self.patient_address.text and self.patient_fon.text and self.patient_sex.text and self.patient_dob.text and self.patient_age.text and self.patient_blood.text:
            return self.insert_patients()
        else:
            return self.empty_popup()

    def empty_popup(self):
        self.content = Label(text=' All fields must be Filled correctly!!!')
        self.popup = Popup(title='Warning!!!!', content=self.content, size_hint=(.4, .3))
        self.popup.open()

class SelectableButton_blood_manage(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton_blood_manage, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton_blood_manage, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected


class EditBloodPopup(Popup):
    patient_id: ObjectProperty(None)
    patient_name: ObjectProperty(None)
    patient_email: ObjectProperty(None)
    patient_address: ObjectProperty(None)
    patient_fon: ObjectProperty(None)
    patient_sex: ObjectProperty(None)
    patient_dob: ObjectProperty(None)
    patient_age: ObjectProperty(None)
    patient_blood: ObjectProperty(None)

    def __init__(self, obj, **kwargs):
        super(EditBloodPopup, self).__init__(**kwargs)
        self.obj = obj
        self.editpatient()

    def editpatient(self):

        c.execute("SELECT ID ,NAME , EMAIL, ADDRESS, PHONE, SEX ,AGE, BLOOD , LAST_DONATED FROM BloodBank  WHERE ID=?",
                  (self.obj,))
        self.row_data = c.fetchone()

        self.patient_id.text = str(self.row_data[0])
        self.patient_name.text = self.row_data[1]
        self.patient_email.text = self.row_data[2]
        self.patient_address.text = self.row_data[3]
        self.patient_fon.text = str(self.row_data[4])
        self.patient_sex.text = self.row_data[5]
        self.patient_age.text = str(self.row_data[6])
        self.patient_blood.text = self.row_data[7]
        self.patient_dob.text = str(self.row_data[8])

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

        c.execute(
            " UPDATE BloodBank SET  NAME=?, EMAIL=? , ADDRESS = ? , PHONE = ? , SEX = ? , AGE = ?, BLOOD = ?, LAST_DONATED = ? WHERE NAME =?",
            (name, email, address, fon, sex,  age, blood, dob,name,))
        con.commit()
        callback = Manage_Blood()
        try:
            callback.refresh()
        except:
            print("popup_refresh error")
########################################### manage Profile #############################################

class Manage_Profile(GridLayout):
    name_id = ObjectProperty(None)
    old_pass = ObjectProperty(None)
    new_pass = ObjectProperty(None)
    konfirm_pass = ObjectProperty(None)
    name = ObjectProperty(None)

    fon = ObjectProperty(None)
    Address = ObjectProperty(None)
    email = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Manage_Profile, self).__init__(**kwargs)

    def search_name(self):
        search = self.name.text

        search += '%'
        c.execute(
            "SELECT Name FROM Users WHERE Name like ? ",
            (search,))
        rows = c.fetchall()

        if len(search) > 3:

            if rows:
                self.name.error = False
                self.name.helper_text = 'Name found in the database'
                return True
            else:
                self.name.error = True
                self.name.helper_text = 'Name not found in the database'
                return False

        else:
            pass

    def validate_email(self):
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        email = self.email.text
        if len(email) > 3:

            if (re.search(regex, email)):
                self.email.error = False
                self.email.helper_text = 'Valid email adress'
                return True
            else:
                self.email.error = True
                self.email.helper_text = 'invalid email Adress must include [@,a-z,.,0-9]'
                return False

        else:
            self.email.error = False

    def validate_fon(self):
        fon = self.fon.text

        for i in range(len(fon)):
            if re.match(r"^[0789]{1}\d{9}$", fon):
                self.fon.error = False
                self.fon.helper_text = 'Valid email phone number'
                return True
            else:
                self.fon.error = True
                self.fon.helper_text = 'Enter a valid phone number'
                return False

    def valid_input(self):
        fon = self.fon.text
        email = self.email.text
        address = self.address.text
        name = self.name.text

        if fon and email and address and name:
            return True
        else:
            return False


    def update_name(self):
        fon = self.fon.text
        email = self.email.text
        address = self.address.text
        name = self.name.text
        if self.validate_email() and self.validate_fon() and self.search_name() and self.valid_input() == True:
            try:

                c.execute("UPDATE Users SET Phone=?,Email=?, Address=?  WHERE Name = ?", (fon, email, address, name,))
                con.commit()
                self.save_successfull()
            except:
                self.save_unsuccessfull()

        else:
            self.save_unsuccessfull()

    def save_successfull(self):
        self.content = Label(text=' Updated Successfully!!!')
        self.popup = Popup(title='Applause!!', content=self.content,
                           size_hint=(.4, .3))
        self.popup.open()

    def save_unsuccessfull(self):
        self.content = Label(text=' Unsuccessfull!!!!')
        self.popup = Popup(title='Applause!!', content=self.content,
                           size_hint=(.4, .3))
        self.popup.open()

    def validate_name(self):
        search = self.name_id.text

        search += '%'
        c.execute(
            "SELECT Name FROM Users WHERE Name like ? ",
            (search,))
        rows = c.fetchall()

        if len(search) > 3:

            if rows:
                self.name_id.error = False
                self.name_id.helper_text = 'User exists'
            else:
                self.name_id.error = True
                self.name_id.helper_text = 'User does not exist!'

        else:
            pass


    def validate_password(self):
        name = self.name_id.text
        password = self.old_pass.text

        password += '%'
        c.execute(
            "SELECT * FROM Users WHERE Name like ? And Password like ?",
            (name, password,))

        rows = c.fetchall()
        # print(rows)

        if len(password) > 3:

            if rows:
                self.old_pass.error = False
                self.old_pass.helper_text = 'Correct'
            else:
                self.old_pass.error = True
                self.old_pass.helper_text = 'Incorrect password'

    def password_strength(self):
        password = self.new_pass.text

        if len(password) > 2:
            if len(password) < 6:
                self.new_pass.error = True
                self.new_pass.helper_text = 'The password should contain upto 6 charecters'
            else:
                self.new_pass.error = False
                self.new_pass.helper_text = ''

            password_scores = {0: 'Horrible', 1: 'Weak', 2: 'Medium', 3: 'Strong'}
            password_strength = dict.fromkeys(['has_upper', 'has_lower', 'has_num'], False)
            if re.search(r'[A-Z]', password):
                password_strength['has_upper'] = True
            if re.search(r'[a-z]', password):
                password_strength['has_lower'] = True
            if re.search(r'[0-9]', password):
                password_strength['has_num'] = True

            score = len([b for b in password_strength.values() if b])

            #print(score)
            #print('Password is %s' % password_scores[score])

            if score == 1:
                self.new_pass.error = True
                self.new_pass.helper_text = 'Weak.'
                return False
            elif score == 2:
                self.new_pass.error = False
                self.new_pass.helper_text = 'Medium'
                return True
            elif score == 3:
                self.new_pass.error = False
                self.new_pass.helper_text = 'Strong'
                return True

    def validate_new_pass(self):
        konfirm = self.konfirm_pass.text
        new = self.new_pass.text

        if len(new) > 3:

            if konfirm != new:
                self.konfirm_pass.helper_text = "Password Does not match"
                self.konfirm_pass.error = True
                return False
            else:
                self.konfirm_pass.helper_text = "Password matched"
                self.konfirm_pass.error = False
                return True

        else:
            self.konfirm_pass.error = False

    def valid_pass_change(self):
        old_pass = self.old_pass.text
        new_pass = self.new_pass.text
        konfirm = self.konfirm_pass.text
        name = self.name_id.text

        if old_pass and new_pass and konfirm and name:
            return True
        else:
            return False

    def update_password(self):
        old_pass = self.old_pass.text
        new_pass = self.new_pass.text
        konfirm = self.konfirm_pass.text
        name = self.name_id.text

        if self.password_strength() and self.validate_new_pass() and self.valid_pass_change() == True:

            try:

                c.execute("UPDATE Users SET Password = ? WHERE Name = ?", (new_pass, name,))
                con.commit()
                self.update_successfull()
            except:
                self.update_unsuccessfull()
        else:
            self.update_unsuccessfull()

    def update_successfull(self):
        self.content = Label(text=' Updated Successfully!!!')
        self.popup = Popup(title='Applause!!', content=self.content,
                           size_hint=(.4, .3))
        self.popup.open()

    def update_unsuccessfull(self):
        self.content = Label(text=' Unsuccessfull!!!!')
        self.popup = Popup(title='Applause!!', content=self.content,
                           size_hint=(.4, .3))
        self.popup.open()

    pass
    
class ImageButton(ButtonBehavior, Image):  
    def on_press(self):  
        print ('pressed')

class Selected_patient(GridLayout):
    pass

######################### login #################################

class ScreenLogin(Screen):
    password = ObjectProperty()
    username = ObjectProperty()
    tablename = ObjectProperty()
    
    def user_input(self):
        if self.username.text and self.password.text:
            return self.validate_login()
        
        else:
            return self.input_empty()

    def input_empty(self):

        self.content = Label(text='username or password cannot be empty')
        self.popup = Popup(title='Warning', content=self.content,
                           size_hint=(.4, .3))
        
        self.popup.open()
        a = self.manager.current = 'Login' 
        
        
    def validate_login( self,**kwargs):
        tablename = self.tablename.text
        c.execute("SELECT * FROM {tn} WHERE Name = ? AND Password = ?".format(tn = tablename),(self.username.text, self.password.text))
        data = c.fetchall()
        #a = self.manager.current = 'Doctor'
        if data:
            return self.validate_table()
        else:
            return self.relogin_popup()

    def validate_table(self):
        tablename = self.tablename.text
        if tablename == 'Doctor':
            self.manager.current ='Doctor'
        else:
            pass
        if tablename == 'Admin':
            self.manager.current ='Admin'
        else:
            pass
        if tablename == 'Pharm':
            self.manager.current ='Pharmascist'
        else:
            pass
        if tablename == 'Nurse':
            self.manager.current ='Nurse'
        else:
            pass
        if tablename == 'Lab':
            self.manager.current ='Labaratorist'
        else:
            pass
        if tablename == 'Account':
            self.manager.current ='Accountant'
        else:
            pass
        
    def relogin_popup(self):
        self.content = Label(text='Invalid username or password')
        self.popup = Popup(title='Warning', content=self.content,
                           size_hint=(.4, .3))
        self.popup.open()
        a = self.manager.current = 'Login' 



class Manager(ScreenManager):

    screen_login = ObjectProperty()
    screen_doctor = ObjectProperty()
    screen_accountant = ObjectProperty()
    screen_labaratorist = ObjectProperty()
    screen_nurse = ObjectProperty()
    screen_pharmascist = ObjectProperty()
    screen_admin = ObjectProperty()

class ScreenApp(App):
    title = 'Hospital Management System'
    change_layout =Manage_Prescription()
    rv = Patient_list()
    rv1 = Appointment()
    rv2 = Manage_Prescription()
    rv3 = Bed_allotement()
    appointment = Appointment()
    call= Add_bed()
    rv5 = Manage_Bed()
    call1 = Add_blood()

    rv6 = Manage_Blood()
    call2 = Add_medcategory()
    rv7 = Med_Category()
    call3 = Add_med()
    rv8 = Manage_med()
    theme_cls = ThemeManager()
    theme_cls.theme_style = 'Light'
    def build(self):
        
        n= Manager(transition=WipeTransition())
        self.rv4 = Manage_Report()
        
        return n 

if __name__ == "__main__":
    ScreenApp().run()
