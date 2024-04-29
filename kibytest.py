from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown

class Workoutform(App):
    def build(self):
        #returns a window object with all it's widgets
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}

        # image widget
        self.window.add_widget(Image(source="logo.png"))

        # label widget
        self.welcome = Label(
                        text= "Welcome to the Workout Form Corrector",
                        font_size= 50,
                        color= '#FFFFFF'
                        )
        self.window.add_widget(self.welcome)


        dropdown = DropDown()
        btn0 = Button(text='curls-left', size_hint_y=None, height=44)
        btn1 = Button(text='curls-right', size_hint_y=None, height=44)

        btn0.bind(on_release=lambda btn: dropdown.select(btn.text))
        btn1.bind(on_release=lambda btn: dropdown.select(btn.text))


        dropdown.add_widget(btn0)
        dropdown.add_widget(btn1)

        self.curlmenu = Button(
                    text='curls select which side...',
                    size_hint= (1, 0.5)
                    )
        self.curlmenu.bind(on_release=dropdown.open)
        self.window.add_widget(self.curlmenu)
        dropdown.bind(on_select=lambda instance, x: setattr(self.curlmenu, 'text', x))

        # button widget
        self.button = Button(
                      text= "START",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE',
                      #remove darker overlay of background colour
                      # background_normal = ""
                      )
        self.button.bind(on_press=self.callback)
        self.window.add_widget(self.button)

        return self.window

    def callback(self, instance):
        # change label text to "Hello + user name!"
        return self.curlmenu.text

# run Say Hello App Calss
if __name__ == "__main__":
    Workoutform().run()