from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class SwitchContainer(BoxLayout):
    def __init__(self, **kwargs):
        super(SwitchContainer, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.button = Button(text='Apply Values')
        self.button.bind(on_press=self.on_button_press)
        self.slider1 = Slider(min=0, max=100, value=50)
        self.slider1.bind(value=self.on_slider_value)
        self.slider2 = Slider(min=0, max=100, value=50)
        self.slider2.bind(value=self.on_slider_value)
        self.slider3 = Slider(min=0, max=100, value=50)
        self.slider3.bind(value=self.on_slider_value)
        self.label1 = Label(text=f'Slider 1: {self.slider1.value}')
        self.label2 = Label(text=f'Slider 2: {self.slider2.value}')
        self.label3 = Label(text=f'Slider 3: {self.slider3.value}')
        self.add_widget(self.button)
        self.add_widget(Label(text=f'Min: {self.slider1.min}'))
        self.add_widget(self.slider1)
        self.add_widget(Label(text=f'Max: {self.slider1.max}'))
        self.add_widget(self.label1)
        self.add_widget(Label(text=f'Min: {self.slider2.min}'))
        self.add_widget(self.slider2)
        self.add_widget(Label(text=f'Max: {self.slider2.max}'))
        self.add_widget(self.label2)
        self.add_widget(Label(text=f'Min: {self.slider3.min}'))
        self.add_widget(self.slider3)
        self.add_widget(Label(text=f'Max: {self.slider3.max}'))
        self.add_widget(self.label3)



    
    def on_button_press(self, instance):
        print('Button pressed, values are:')
        print('Slider 1:', self.slider1.value)
        print('Slider 2:', self.slider2.value)
        print('Slider 3:', self.slider3.value)

    def on_slider_value(self, instance, value):
        if instance == self.slider1:
            self.label1.text = f'Slider 1: {value}'
        elif instance == self.slider2:
            self.label2.text = f'Slider 2: {value}'
        elif instance == self.slider3:
            self.label3.text = f'Slider 3: {value}'

class MyApp(App):
    def build(self):
        return SwitchContainer()

if __name__ == '__main__':
    MyApp().run()