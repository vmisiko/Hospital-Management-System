
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty, ListProperty, NumericProperty,DictProperty,BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
import sys
from kivy.factory import Factory
from kivy.clock import Clock

import requests
import hmac, hashlib
import base64
import json
from enum import Enum
import re
from tkinter.filedialog import askopenfilename
from tkinter import Tk

from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior


#Load kv file

Builder.load_file('test.kv')

Gender = Enum('Gender', 'Male Female')

SelectorStatus = Enum('SelectorStatus', 'Man Woman Boy Girl')

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



class DiagnosisClient:
    'Client class for priaid diagnosis health service'

    # <summary>
    # DiagnosisClient constructor
    # </summary>
    # <param name="username">api user username</param>
    # <param name="password">api user password</param>
    # <param name="authServiceUrl">priaid login url (https://authservice.priaid.ch/login)</param>
    # <param name="language">language</param>
    # <param name="healthServiceUrl">priaid healthservice url(https://healthservice.priaid.ch)</param>
    def __init__(self, username, password, authServiceUrl, language, healthServiceUrl):

        username = "victormisiko.vm@gmail.com"  # Here enter your API user name
        password = "Py9q6S4Bik5JCf3t7"  # Here enter your API password
        authServiceUrl = "https://sandbox-authservice.priaid.ch/login"  # Be aware that sandbox link is for testing pourpose (not real data) once you get live access you shold use https://authservice.priaid.ch/login
        healthServiceUrl = "https://sandbox-healthservice.priaid.ch"  # Be aware that sandbox link is for testing pourpose (not real data) once you get live access you shold use https://healthservice.priaid.ch
        language = "en-gb"  # en-gb, de-ch, fr-fr, it-it, es-es, ar-sa, ru-ru, tr-tr, sr-sp, sk-sk...
        pritnRawOutput = False  # This flag can be set to see printed json data structure of webservice responses

        self._handleRequiredArguments(username, password, authServiceUrl, healthServiceUrl, language)

        self._language = language
        self._healthServiceUrl = healthServiceUrl
        self._token = self._loadToken(username, password, authServiceUrl)

    def _loadToken(self, username, password, url):
        rawHashString = hmac.new(bytes(password, encoding='utf-8'), url.encode('utf-8')).digest()
        computedHashString = base64.b64encode(rawHashString).decode()

        bearer_credentials = username + ':' + computedHashString
        postHeaders = {
            'Authorization': 'Bearer {}'.format(bearer_credentials)
        }

        responsePost = requests.post(url, headers=postHeaders)
        #print(responsePost)
        data = json.loads(responsePost.text.encode().decode('utf-8-sig'))
        return data

    def _handleRequiredArguments(self, username, password, authUrl, healthUrl, language):
        if not username:
            raise ValueError("Argument missing: username")

        if not password:
            raise ValueError("Argument missing: password")

        if not authUrl:
            raise ValueError("Argument missing: authServiceUrl")

        if not healthUrl:
            raise ValueError("Argument missing: healthServiceUrl")

        if not language:
            raise ValueError("Argument missing: language")


    def _loadFromWebService(self, action):
        extraArgs = "token=" + self._token["Token"] + "&format=json&language=" + self._language
        if "?" not in action:
            action += "?" + extraArgs
        else:
            action += "&" + extraArgs

        url = self._healthServiceUrl + "/" + action
        response = requests.get(url)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print("----------------------------------")
            print("HTTPError: " + e.response.text)
            print("----------------------------------")
            raise

        try:
            dataJson = response.json()
        except ValueError:
            raise requests.exceptions.RequestException(response=response)

        data = json.loads(response.text)
        return data

        # <summary>

    # Load all symptoms
    # </summary>
    # <returns>Returns list of all symptoms</returns>
    def loadSymptoms(self):
        return self._loadFromWebService("symptoms")

    # <summary>
    # Load all issues
    # </summary>
    # <returns>Returns list of all issues</returns>
    def loadIssues(self):
        return self._loadFromWebService("issues")

    # <summary>
    # Load detail informations about selected issue
    # </summary>
    # <param name="issueId"></param>
    # <returns>Returns detail informations about selected issue</returns>
    def loadIssueInfo(self, issueId):
        if isinstance(issueId, int):
            issueId = str(issueId)
        action = "issues/{0}/info".format(issueId)
        return self._loadFromWebService(action)

    # <summary>
    # Load calculated list of potential issues for selected parameters
    # </summary>
    # <param name="selectedSymptoms">List of selected symptom ids</param>
    # <param name="gender">Selected person gender (Male, Female)</param>
    # <param name="yearOfBirth">Selected person year of born</param>
    # <returns>Returns calculated list of potential issues for selected parameters</returns>
    def loadDiagnosis(self, selectedSymptoms, gender, yearOfBirth):
        if not selectedSymptoms:
            raise ValueError("selectedSymptoms can not be empty")

        serializedSymptoms = json.dumps(selectedSymptoms)
        action = "diagnosis?symptoms={0}&gender={1}&year_of_birth={2}".format(serializedSymptoms, gender.name,
                                                                              yearOfBirth)
        return self._loadFromWebService(action)

    # <summary>
    # Load calculated list of specialisations for selected parameters
    # </summary>
    # <param name="selectedSymptoms">List of selected symptom ids</param>
    # <param name="gender">Selected person gender (Male, Female)</param>
    # <param name="yearOfBirth">Selected person year of born</param>
    # <returns>Returns calculated list of specialisations for selected parameters</returns>
    def loadSpecialisations(self, selectedSymptoms, gender, yearOfBirth):
        if not selectedSymptoms:
            raise ValueError("selectedSymptoms can not be empty")

        serializedSymptoms = json.dumps(selectedSymptoms)
        action = "diagnosis/specialisations?symptoms={0}&gender={1}&year_of_birth={2}".format(serializedSymptoms,
                                                                                              gender.name, yearOfBirth)
        return self._loadFromWebService(action)

    # <summary>
    # Load human body locations
    # </summary>
    # <returns>Returns list of human body locations</returns>
    def loadBodyLocations(self):
        return self._loadFromWebService("body/locations")

    # <summary>
    # Load human body sublocations for selected human body location
    # </summary>
    # <param name="bodyLocationId">Human body location id</param>
    # <returns>Returns list of human body sublocations for selected human body location</returns>
    def loadBodySubLocations(self, bodyLocationId):
        action = "body/locations/{0}".format(bodyLocationId)
        return self._loadFromWebService(action)

    # <summary>
    # Load all symptoms for selected human body location
    # </summary>
    # <param name="locationId">Human body sublocation id</param>
    # <param name="selectedSelectorStatus">Selector status (Man, Woman, Boy, Girl)</param>
    # <returns>Returns list of all symptoms for selected human body location</returns>
    def loadSublocationSymptoms(self, locationId, selectedSelectorStatus):
        action = "symptoms/{0}/{1}".format(locationId, selectedSelectorStatus.name)
        return self._loadFromWebService(action)

    # <summary>
    # Load list of proposed symptoms for selected symptoms combination
    # </summary>
    # <param name="selectedSymptoms">List of selected symptom ids</param>
    # <param name="gender">Selected person gender (Male, Female)</param>
    # <param name="yearOfBirth">Selected person year of born</param>
    # <returns>Returns list of proposed symptoms for selected symptoms combination</returns>
    def loadProposedSymptoms(self, selectedSymptoms, gender, yearOfBirth):
        if not selectedSymptoms:
            raise ValueError("selectedSymptoms can not be empty")

        serializedSymptoms = json.dumps(selectedSymptoms)
        action = "symptoms/proposed?symptoms={0}&gender={1}&year_of_birth={2}".format(serializedSymptoms, gender.name,
                                                                                      yearOfBirth)
        return self._loadFromWebService(action)

    # <summary>
    # Load red flag text for selected symptom
    # </summary>
    # <param name="symptomId">Selected symptom id</param>
    # <returns>Returns red flag text for selected symptom</returns>
    def loadRedFlag(self, symptomId):
        action = "redflag?symptomId={0}".format(symptomId)
        return self._loadFromWebService(action)

class ScreenAdmin(Screen):
    pass

class ScreenDoctor(Screen):
    pass

class ImageButton(ButtonBehavior, Image):
    pass

class Screen2(BoxLayout):
   pass

class ScreenLogin(Screen):
    tp= ObjectProperty(None)
    diagnosis_box = ObjectProperty(None)
    symptom_box = ObjectProperty(None)
    symptomsearch_id = ObjectProperty(None)
    diagnosearch_id = ObjectProperty(None)
    choose_doc = ObjectProperty(None)
    check_ref = {}

    def __init__(self, **kwargs):
        super(ScreenLogin, self).__init__(**kwargs)
        Clock.schedule_once(self.show)
        Clock.schedule_once(self.show_symptoms)
        self.connection_check()

        username = "victormisiko.vm@gmail.com"
        password = "Py9q6S4Bik5JCf3t7"  # Here enter your API password
        authServiceUrl = "https://sandbox-authservice.priaid.ch"  # Be aware that sandbox link is for testing pourpose (not real data) once you get live access you shold use https://authservice.priaid.ch/login
        healthServiceUrl = "https://sandbox-healthservice.priaid.ch"  # Be aware that sandbox link is for testing pourpose (not real data) once you get live access you shold use https://healthservice.priaid.ch
        language = "en-gb"


        #self.load = DiagnosisClient(username, password, authServiceUrl, healthServiceUrl, language)

    def profile(self):
        layout = Factory.Manage_Profile()
        self.manage_patient.clear_widgets()
        self.manage_patient.add_widget(layout)

############################# Documetn selection code ###########################
    def choose_file(self):
        Tk().withdraw()  # avoids window accompanying tkinter FileChooser
        doc = askopenfilename(initialdir="/", title="Select file",
                               filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.choose_doc.source = doc

    def connection(self):
        username = "victormisiko.vm@gmail.com"
        password = "Py9q6S4Bik5JCf3t7"  # Here enter your API password
        authServiceUrl = "https://sandbox-authservice.priaid.ch"  # Be aware that sandbox link is for testing pourpose (not real data) once you get live access you shold use https://authservice.priaid.ch/login
        healthServiceUrl = "https://sandbox-healthservice.priaid.ch"  # Be aware that sandbox link is for testing pourpose (not real data) once you get live access you shold use https://healthservice.priaid.ch
        language = "en-gb"
        load = DiagnosisClient(username, password, authServiceUrl, healthServiceUrl, language)

        self.loadsymptoms = load.loadSymptoms()

        with open('symptom.txt', 'w') as outfile:
            json.dump(self.loadsymptoms, outfile)

    def show(self,number):

        number = 10
        layout = GridLayout(cols = 1,padding=10,size_hint_y=None , row_force_default= True, row_default_height= '30dp' )
        layout.bind(minimum_height=layout.setter("height"))

        with open('symptom.txt') as json_file:
            symptom_list = json.load(json_file)

        prods=[]
        for person in symptom_list:
            #print(person)
            for k, v in person.items():
                #print('{}: {}'.format(k, v))
                #print(v)

                if k == 'Name':
                    prods.append(v)

        #print(prods)



        #prods = [' Coughing', ' Diarhoer', ' Purse', ' Badbreath',' Weak joints', ' Salamander', ' B_0008', ' B_0200']

        for each in range(len(prods)):
            layout2 = BoxLayout(padding=[0,0,30,0], orientation="horizontal")
            label1 = Button(color=(0,0,0,1 ), font_size=15,background_normal="",background_color= (1,1,1,1), text=prods[each],halign = 'left', markup=True)
            chckbox = CheckBox( color=(0,0,0,1))
            #chckbox.bind(active=self.getcheckboxes_active)

            # Stores a reference to the CheckBox instance
            #self.check_ref[chckbox] = prods[each]
            self.check_ref[str(prods[each])] = chckbox

            layout2.add_widget(chckbox)
            layout2.add_widget(label1)
            layout.add_widget(layout2)

        self.symptom_box.clear_widgets()
        self.symptom_box.add_widget(layout)

        '''button = Button(text="OK 2")
        button.bind(
            on_press=self.getcheckboxes_active)  # self.getcheckboxes_active(self, "test") give an error None is not callable
        layout.add_widget(button)
        self.add_widget(layout)'''

    def getcheckboxes_active(self, *arg):
        username = "victormisiko.vm@gmail.com"
        password = "Py9q6S4Bik5JCf3t7"  # Here enter your API password
        authServiceUrl = "https://sandbox-authservice.priaid.ch"  # Be aware that sandbox link is for testing pourpose (not real data) once you get live access you shold use https://authservice.priaid.ch/login
        healthServiceUrl = "https://sandbox-healthservice.priaid.ch"  # Be aware that sandbox link is for testing pourpose (not real data) once you get live access you shold use https://healthservice.priaid.ch
        language = "en-gb"
        gender ="male"
        yearOfBirth = "1996"

        '''how to get the active state of all checkboxed created in def show'''
        # Iterate over the dictionary storing the CheckBox widgets
        selected_symptoms = []
        for idx, wgt in self.check_ref.items():
            #print(wgt.active)
            if wgt.active == True:
                #print(idx)
                selected_symptoms.append(idx)
        #print(selected_symptoms)


        selectedSymptoms = []
        if self.connection_check():
            for person in self.loadsymptoms:
                #print(person)
                for k, v in person.items():
                    #print('{}: {}'.format(k, v))
                    #print(v)
                    if v in selected_symptoms:
                        selectedSymptoms.append(person['ID'])
        else:
            return self.connection_popup()

        #print(selectedSymptoms)

        load = DiagnosisClient(username, password, authServiceUrl, healthServiceUrl, language)
        self.diagnose = load.loadDiagnosis( selectedSymptoms, Gender.Male, 1996 )

        #print(self.diagnose)

        self.diagnose_list = []
        for person in self.diagnose:
            #print(person)
            for k, v in person.items():
                #print(person['Issue']['Name'])

                self.diagnose_list.append(person['Issue']['Name'])

        #print(diagnose_list)

        layout = GridLayout(cols=1, padding=10, size_hint_y=None, row_force_default=True, row_default_height='30dp')
        layout.bind(minimum_height=layout.setter("height"))
        for each in range(len(self.diagnose_list)):

            layout3 = BoxLayout(padding=[0,0,30,0], orientation="horizontal")
            label1 = Button(color=(0,0,0,1 ), font_size=15,background_normal="",background_color= (1,1,1,1), text=self.diagnose_list[each],halign = 'left', markup=True)
            chckbox = CheckBox(color=(0,0,0,1))
            #chckbox.bind(active=self.getcheckboxes_active)

            # Stores a reference to the CheckBox instance
            #self.check_ref[chckbox] = prods[each]
            self.check_ref[str(self.diagnose_list[each])] = chckbox

            layout3.add_widget(chckbox)
            layout3.add_widget(label1)
            layout.add_widget(layout3)

        if len(self.diagnose_list) > 0:
            self.diagnosis_box.clear_widgets()
            self.diagnosis_box.add_widget(layout)
        else:
            #print('empty')

            self.diagnosis_box.clear_widgets()
            self.diagnosis_box.add_widget(Label(text ='No diagnosis found!', color = (0,0,0,1),  ))

    def connection_popup(self):

        self.content = Label(text='          Connection Failure,\n Check your Internet Connectivity')
        self.popup = Popup(title='Warning', content=self.content,
                           size_hint=(.4, .3))

        self.popup.open()

    def more_info(self, instance):
        info = instance
        self.content = Label(text=info)
        self.popup = Popup(title='Warning', content=self.content,
                           size_hint=(.4, .3))

        self.popup.open()

    def show_symptoms(self,number):

        number = 10
        layout = GridLayout(cols = 1,padding=[0,0,30,0],size_hint_y=None , row_force_default= True, row_default_height= '30dp' )
        layout.bind(minimum_height=layout.setter("height"))
        #print(self.load_diagnosis)
        prods=[]
        '''for person in self.load_diagnosis:
            #print(person)
            for k, v in person.items():
                #print('{}: {}'.format(k, v))
                #print(v)

                if k == 'Name':
                    prods.append(v)'''

        #print(prods)



        prods = [' Coughing', ' Diarhoer', ' Purse', ' Badbreath',' Weak joints', ' Salamander', ' B_0008', ' B_0200']

        for each in range(len(prods)):
            layout2 = BoxLayout(padding=10, orientation="horizontal")
            label1 = Button(color=(0,0,0,1 ), font_size=15,background_normal="",background_color= (1,1,1,1), text=prods[each],halign = 'left', markup=True)
            chckbox = CheckBox(color=(0,0,0,1))
            #chckbox.bind(active=self.getcheckboxes_active)

            # Stores a reference to the CheckBox instance
            #self.check_ref[chckbox] = prods[each]
            self.check_ref[str(prods[each])] = chckbox

            layout2.add_widget(chckbox)
            layout2.add_widget(label1)
            layout.add_widget(layout2)

        self.diagnosis_box.clear_widgets()
        self.diagnosis_box.add_widget(layout)


        '''button = Button(text="OK 2")
        button.bind(
            on_press = self.getcheckboxes_active)  # self.getcheckboxes_active(self, "test") give an error None is not callable
        layout.add_widget(button)
        self.add_widget(layout)'''
    def on_type_validate(self):


        if self.symptomsearch_id.text:
            return self.on_text_typing()
        else:
            self.symptom_box.clear_widgets()
            Clock.schedule_once(self.show)

    def on_text_typing(self):

        #symptom_list = []
        with open('symptom.txt') as json_file:
            symptom_list = json.load(json_file)

        typed_word =self.symptomsearch_id.text
        mylist = [d['Name'] for d in symptom_list]

        #print(mylist)

        r = re.compile(".*{}".format(typed_word))
        newlist = list(filter(r.match, mylist ))  # Read Note
        #print(newlist)

        layout = GridLayout(cols=1, padding=10, size_hint_y=None, row_force_default=True, row_default_height='30dp')
        layout.bind(minimum_height=layout.setter("height"))

        for each in range(len(newlist)):
            layout3 = BoxLayout(padding=[0,0,30,0], orientation="horizontal")
            label1 = Button(color=(0,0,0,1 ), font_size=15,background_normal="",background_color= (1,1,1,1), text=newlist[each],halign = 'left', markup=True)
            chckbox = CheckBox(color=(0,0,0,1))
            #chckbox.bind(active=self.getcheckboxes_active)

            # Stores a reference to the CheckBox instance
            #self.check_ref[chckbox] = prods[each]
            self.check_ref[str(newlist[each])] = chckbox

            layout3.add_widget(chckbox)
            layout3.add_widget(label1)
            layout.add_widget(layout3)


        if len(newlist) > 0  and len(typed_word) > 0:
            self.symptom_box.clear_widgets()
            self.symptom_box.add_widget(layout)
        else:
            #print('empty')

            self.symptom_box.clear_widgets()
            self.symptom_box.add_widget(Label(text ='No Symptom found!', color = (0,0,0,1),  ))

    def on_type_validate_diag(self):


        if self.diagnosearch_id.text:
            return self.on_text_typing_diagnosis()
        else:
            self.diagnosis_box.clear_widgets()
            Clock.schedule_once(self.show_symptoms)

    def on_text_typing_diagnosis(self):

        typed_word =self.diagnosearch_id.text
        mylist = self.diagnose_list

        #print(mylist)

        r = re.compile(".*{}".format(typed_word))
        newlist = list(filter(r.match, mylist ))  # Read Note
        #print(newlist)

        layout = GridLayout(cols=1, padding=10, size_hint_y=None, row_force_default=True, row_default_height='30dp')
        layout.bind(minimum_height=layout.setter("height"))

        for each in range(len(newlist)):
            layout3 = BoxLayout(padding=[0,0,30,0], orientation="horizontal")
            label1 = Button(color=(0,0,0,1 ), font_size=15,background_normal="",background_color= (1,1,1,1), text= newlist[each],halign = 'left', markup=True)
            chckbox = CheckBox(color=(0,0,0,1))

            #chckbox.bind(active=self.getcheckboxes_active)

            # Stores a reference to the CheckBox instance
            #self.check_ref[chckbox] = prods[each]
            self.check_ref[str(newlist[each])] = chckbox

            layout3.add_widget(chckbox)
            layout3.add_widget(label1)
            layout.add_widget(layout3)


        if len(newlist) > 0  and len(typed_word) > 0:
            self.diagnosis_box.clear_widgets()
            self.diagnosis_box.add_widget(layout)
        else:
            #print('empty')

            self.diagnosis_box.clear_widgets()
            self.diagnosis_box.add_widget(Label(text ='No Symptom found!', color = (0,0,0,1),  ))

    def connection_check(self):
        try:
            requests.get("http://google.com", timeout = 3)
            print('connection successful')
            self.connection()
            return True

        except:
            print('connection failed') 
        return False


class SelectableButton_presc(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton_presc, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton_presc, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

class Manage_Profile(ScrollView):
    pass

#Initialize Screens and Start App
class MyScreenManager(ScreenManager):

    screen_login = ObjectProperty()
    screen_doctor = ObjectProperty()
    screen_accountant = ObjectProperty()
#Main application
class SampleApp(App):

    def build(self):
        self.sm = MyScreenManager()
        self.dashboard = Screen2()
        return self.sm

if __name__ == '__main__':
    SampleApp().run()
