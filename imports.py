import os
os.environ['KIVY_IMAGE'] = 'pil,sdl2'
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager,Screen,WipeTransition
from kivy.properties import BooleanProperty
from kivy.properties import ObjectProperty, StringProperty, ListProperty, NumericProperty
from kivy.graphics.vertex_instructions import (Rectangle, Ellipse, Line)
#from kivy.graphics.context_instructions import Color
from kivy.core.image import Image
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.dropdown import DropDown
#from kivy.graphics import BorderImage
from kivy.graphics import Color, Rectangle
#from kivy.uix.image import AsyncImage
from tkinter.filedialog import askopenfilename
from tkinter import Tk
from KivyCalendar import CalendarWidget
from KivyCalendar import DatePicker
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import sqlite3 as lite
from kivy.uix.image import Image
from kivy.factory import Factory
import sys
import re
import random
from kivy.uix.video import Video
from kivy.clock import Clock
from kivy.clock import mainthread
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

from kivymd.utils.cropimage import crop_image
from kivymd.utils import asynckivy
from kivymd.fanscreenmanager import MDFanScreen
from kivymd.popupscreen import MDPopupScreen
from kivymd.button import MDIconButton
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, OneLineIconListItem, OneLineListItem
from kivymd.selectioncontrols import MDCheckbox
from kivymd.theming import ThemeManager
from kivymd.ripplebehavior import CircularRippleBehavior
from kivymd.cards import MDCard
from kivymd.icon_definitions import md_icons




con = lite.connect('test.db')
c = con.cursor()
