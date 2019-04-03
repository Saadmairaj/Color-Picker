from meta import *

__version__ = '0.0.1'

from kivy.config import Config
Config.set('kivy','window_icon','Color1.icns')

from kivy.app import App
from kivy.metrics import *
from kivy.uix.colorpicker import ColorPicker
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

kv = Builder.load_string("""

<Custom_Button@Button>:
    background_color: 1, 1, 1, 0.3
    size_hint: dp(0.07), dp(0.10)
    font_size: sp(13)

<Custom_Spinner@Spinner>:
    background_color: 1, 1, 1, 0.3
    size_hint: dp(0.07), dp(0.10)
    font_size: sp(13)

<CustomPopup>:
    color_picker: color_picker
    
    title: "Color Picker"
    title_align: "center"
    title_size: dp(20)
    seperator_height: 0
    separator_color: [1,1,1,0.5]
    size_hint: (0.8), (0.8)

    GridLayout:
        cols: 1
        padding: (10)
        spacing: (10)

        ColorPicker:
            id: color_picker
        
        Custom_Button:
            text: "Select"
            on_press: 
                root.dismiss()

<Main>:

    input_id: input_id
    spinner_id: spinner_id
    mode_id: mode_id

    padding: (5)
    spacing: (5)
    cols: 1
            
    GridLayout:
        cols: 2
        
        Label:
            id: mode_id
            text: "RGBA:"
            size_hint_x: None
            font_size: sp(22)
            width: dp(125)

        
        TextInput:
            id: input_id
            paddinf_x: dp(self.width)
            multiline: False
            allow_copy: True
            font_size: sp(20)
            # readonly: True
            padding: [ (20), (self.height-self.line_height)/2 ]
        
    Custom_Button:
        text: "Pick Color"
        on_press: root.popup()
    
    Custom_Spinner:
        id: spinner_id
        text: "Mode: [b]{}[/b]".format("RGBA")
        values: [ "RGBA", "HSV", "HEX" ]
        on_text:    
            root.Mode(spinner_id.text)
        markup: True
        
    
    Custom_Button:
        text: "Copy"
        on_press: 
            input_id.select_all()
            input_id.copy()
    
""")


class CustomPopup(Popup):

    color_picker = ObjectProperty(None)

    def __init__(self, master, **kwargs):
        super(CustomPopup, self).__init__(**kwargs)
        self.color_picker.bind(color=self.get_color)

        self.master = master

        self.HEX  = None
        self.RGBA = None
        self.HSV  = None
    
    def get_color(self, instance, value):
        print ( "RGBA = ", str(value) )
        print ( "HSV = ",  str(instance.hsv) )
        print ( "HEX = ",  str(instance.hex_color) )
        print ( "\n" )

        self.RGBA  = str(value)
        self.HSV = str(instance.hsv)
        self.HEX  = str(instance.hex_color)

        if str(self.master.mode_id.text).lower() == "rgba:":
            self.master.input_id.text=self.RGBA
        elif str(self.master.mode_id.text).lower() == "hsv:":
            self.master.input_id.text=self.HSV
        elif str(self.master.mode_id.text).lower() == "hex:":
            self.master.input_id.text=self.HEX
        self.master.mode_id.color = value

class Main(GridLayout):

    input_id =  ObjectProperty(None)
    spinner_id = ObjectProperty(None)
    mode_id = ObjectProperty(None)

    def popup(self):
        self.New_Popup = CustomPopup(master=self)
        self.New_Popup.open()
    
    def Mode(self, value):
        def chng(evt):
            self.spinner_id.text = "Mode: [b]{}[/b]" .format(value)
            self.mode_id.text = str(value).upper()+":"
            self.ll.cancel()
            try:
                if value == "RGBA":
                    self.input_id.text = self.New_Popup.RGBA
                elif value == "HSV":
                    self.input_id.text = self.New_Popup.HSV
                elif value == "HEX":
                    self.input_id.text = self.New_Popup.HEX
            except: pass

        self.ll = Clock.schedule_once( chng, 0 )

class ColorApp(App):
    def build(self):
        Window.size = ( (600), (500) )
        return Main()

ColorApp().run()