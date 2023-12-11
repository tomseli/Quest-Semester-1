from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.tabbedpanel import TabbedPanelHeader
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.clock import Clock
from math import sin, pi
import time



class MyApp(App):
    def build(self):
        tabbed_panel = TabbedPanel(do_default_tab=False, tab_pos='left_mid')
        self.current_tab_label = Label(text='')
        self.previous_tab = None

        # Bind the on_tab_switch event to the update_current_tab function
        tabbed_panel.bind(on_tab_switch=self.update_current_tab)

        # Settings tab
        settings_tab = TabbedPanelHeader(text='Settings')
        settings_tab.content = BoxLayout(orientation='vertical')
        settings_tab.content.add_widget(Slider(min=0, max=100, value=50))
        settings_tab.content.add_widget(Slider(min=0, max=100, value=50))
        settings_tab.content.add_widget(Slider(min=0, max=100, value=50))
        tabbed_panel.add_widget(settings_tab)

        # Graphs tab
        graphs_tab = TabbedPanelHeader(text='Graphs')
        graphs_tab.content = MyGraph()
        tabbed_panel.add_widget(graphs_tab)

        # Add the current_tab_label to the tabbed_panel
        tabbed_panel.add_widget(self.current_tab_label)

        return tabbed_panel

    def update_current_tab(self, instance, value):
        self.current_tab_label.text = 'Current tab: ' + value.text
        if self.previous_tab:
            self.previous_tab.background_color = [0, 0, 0.8, 1]
        value.background_color = [1, 0, 0, 1]
        self.previous_tab = value

    def update_current_tab(self, instance, value):
        self.current_tab_label.text = 'Current tab: ' + value.text
        if self.previous_tab:
            self.previous_tab.background_color = [0, 0, 0.8, 1]
        value.background_color = [1, 0, 0, 1]
        self.previous_tab = value



class MyGraph(BoxLayout):
    def __init__(self, **kwargs):
        super(MyGraph, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.graph = Graph(xlabel='Time', ylabel='Y', x_ticks_minor=5,
                           x_ticks_major=25, y_ticks_major=1,
                           y_grid_label=True, x_grid_label=True, padding=5,
                           xlog=False, ylog=False, x_grid=True, y_grid=True,
                           xmin=-0, xmax=10, ymin=-1, ymax=1)
        self.plot = MeshLinePlot(color=[1, 0, 0, 1])
        self.graph.add_plot(self.plot)
        self.add_widget(self.graph)
        Clock.schedule_interval(self.update_graph, 1/60.)

    def update_graph(self, dt):
        self.plot.points = [(x/10., sin(2*pi*(x/10. - time.time()))) for x in range(0, 101)]




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

#class MyApp(App):
 #   def build(self):
  #      root = BoxLayout(orientation='horizontal')
   #     root.add_widget(SwitchContainer())
    #    root.add_widget(MyGraph())
     #   return root

if __name__ == '__main__':
    MyApp().run()