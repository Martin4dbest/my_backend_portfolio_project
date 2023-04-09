# myfirst_mobile_app

import kivy 
This line imports the Kivy framework which is used to build user interfaces for Python applications.

from kivy.app import App
This line imports the App class from the kivy.app module. The App class is the base class for Kivy applications.

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
These lines import the GridLayout, Label, TextInput, and Button classes from the kivy.uix module.
These classes are used to create UI elements for the application.

class childApp(GridLayout):
This line defines a new class called childApp that inherits from the GridLayout class.

def __init__(self, **kwargs):
    super(childApp, self).__init__()
This is the constructor for the childApp class. It calls the constructor of the parent class (GridLayout) using the super() function.

elf.cols = 2
This sets the number of columns for the GridLayout to 2.

self.add_widget(Label(text = 'Student Name'))
self.s_name = TextInput()
self.add_widget(self.s_name)
These lines create a Label and a TextInput widget for the student's name, and add them to the GridLayout using the add_widget() method.

self.add_widget(Label(text = 'Student Marks'))
self.s_marks = TextInput()
self.add_widget(self.s_marks)
These lines create a Label and a TextInput widget for the student's marks, and add them to the GridLayout.

self.add_widget(Label(text = 'Student Gender'))
self.s_gender = TextInput()
self.add_widget(self.s_gender)
These lines create a Label and a TextInput widget for the student's gender, and add them to the GridLayout.

self.press = Button(text = 'Click me')
self.press.bind(on_press = self.click_me)
self.add_widget(self.press)
These lines create a Button widget with the text "Click me", and add it to the GridLayout. It also binds the click_me() method to the on_press event of the button.

def click_me(self, instance):
    print("Name of Student:  "+self.s_name.text)
    print("Marks of Student: "+self.s_marks.text)
    print("Gender of Students: "+self.s_gender.text)
    print("")
This is a method that is called when the button is pressed. It prints the student's name, marks, and gender to the console.

class parentApp(App):
    def build(self):
        return childApp()
This line defines a new class called parentApp that inherits from the App class. The build() method of this class returns an instance of the childApp class.

if __name__ == "__main__":
    parentApp().run()
This block of code checks if the script is being run as the main program. If it is, it creates an instance of the parentApp class and calls its run() method, which starts the Kivy application.
