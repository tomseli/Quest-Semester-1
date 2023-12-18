from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.properties import NumericProperty
from kivy.clock import Clock
import math




class MyGraph(Graph):
    x_scale = NumericProperty(1)
    y_scale = NumericProperty(1)

    def __init__(self, **kwargs):
        super(MyGraph, self).__init__(**kwargs)
        self.plot = MeshLinePlot(color=[1, 0, 0, 1])
        self.add_plot(self.plot)
        self.bind(x_scale=self.update_scale, y_scale=self.update_scale)
        Clock.schedule_interval(self.update_plot, 1.0 / 60.0)

    def update_scale(self, *args):
        self.xmin = -50 * self.x_scale
        self.xmax = 50 * self.x_scale
        self.ymin = -1 * self.y_scale
        self.ymax = 1 * self.y_scale

    def update_plot(self, dt):
        self.plot.points = [(x / 10., math.sin(x / 10.)) for x in range(-500, 500)]

class MyApp(App):
    def build(self):
        Window.clearcolor = (0.15, 0.15, 0.15, 1)  # Dark background


        #tabs
        tabbed_panel = TabbedPanel(do_default_tab=False, tab_pos='left_mid')

        # Settings tab --------------------------------------------------------------------------------------------------------------------------	
        settings_tab = TabbedPanelHeader(text='Settings')
        settings_layout = AnchorLayout()


        # Add V,t diagram
        graph_layout = AnchorLayout(anchor_x='right', anchor_y='top')
        graph_box = BoxLayout(size_hint=(None, None), size=(600, 400))  # Adjust size as needed

        placeholder_graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
                                x_ticks_major=25, y_ticks_major=1,
                                y_grid_label=True, x_grid_label=True, padding=5,
                                xlog=False, ylog=False, x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=-1, ymax=1)
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        plot.points = [(x, 0) for x in range(0, 101)]
        placeholder_graph.add_plot(plot)

        graph_box.add_widget(placeholder_graph)
        graph_layout.add_widget(graph_box)
        settings_layout.add_widget(graph_layout) 

        # Add slider APM
        slider_layout = AnchorLayout(anchor_x='left', anchor_y='bottom')
        slider_box = BoxLayout(size_hint=(None, None), size=(700, 100))  # Adjust size as needed

        self.slider1 = Slider(min=0, max=100, step=1, value=50)
        self.slider1_label = Label(text=f'{self.slider1.value} ({self.slider1.min}-{self.slider1.max})')
        self.slider1.bind(value=self.update_slider1_label)

        slider_box.add_widget(self.slider1)
        slider_box.add_widget(self.slider1_label)

        slider_layout.add_widget(slider_box)
        settings_layout.add_widget(slider_layout)

        # Add switches for presets
        switch_layout = AnchorLayout(anchor_x='left', anchor_y='top')
        switch_box = BoxLayout(orientation='vertical', size_hint=(None, None), size=(200, 200))  # Adjust size as needed

        self.switch1 = Switch(active=False)
        self.switch1_label = Label(text='Borst of buik')
        self.switch2 = Switch(active=False)
        self.switch2_label = Label(text='Instructie of zonder')

        switch_box.add_widget(self.switch1_label)
        switch_box.add_widget(self.switch1)
        switch_box.add_widget(self.switch2_label)
        switch_box.add_widget(self.switch2)

        switch_layout.add_widget(switch_box)
        settings_layout.add_widget(switch_layout)

        # Start-stop button
        button_layout = AnchorLayout(anchor_x='right', anchor_y='bottom')
        button_box = BoxLayout(size_hint=(None, None), size=(100, 100))  # Adjust size as needed

        start_stop_button = Button(text='Start or Stop')
        start_stop_button.bind(on_release=self.start_stop)

        button_box.add_widget(start_stop_button)
        button_layout.add_widget(button_box)
        settings_layout.add_widget(button_layout)



        #finish Settings tab
        settings_tab.content = settings_layout
        tabbed_panel.add_widget(settings_tab)        


        #graph tab --------------------------------------------------------------------------------------------------------------------------
        graphs_tab = TabbedPanelHeader(text='Graphs')
        self.graph = MyGraph()

        # Create a BoxLayout to contain the slider and the graph
        graph_layout = AnchorLayout()

        # Add slider for adjusting the y scale of the graph
        self.y_scale_slider = Slider(min=0.1, max=2, value=1, orientation='vertical', size_hint_x = 0.1)
        self.y_scale_slider.bind(value=self.update_y_scale)

        graph_layout.add_widget(self.y_scale_slider)
        graph_layout.add_widget(self.graph)

        # Add slider for adjusting the x scale of the graph
        self.x_scale_slider = Slider(min=0.1, max=2, value=1, size_hint_y = 0.1)
        self.x_scale_slider.bind(value=self.update_x_scale)

        main_layout = AnchorLayout()
        main_layout.add_widget(graph_layout)
        main_layout.add_widget(self.x_scale_slider)

        graphs_tab.content = main_layout
        tabbed_panel.add_widget(graphs_tab)

        return tabbed_panel

    def update_x_scale(self, instance, value):
        self.graph.x_scale = value

    def update_y_scale(self, instance, value):
        self.graph.y_scale = value
    
    def update_slider1_label(self, instance, value):
        self.slider1_label.text = f'{value} ({instance.min}-{instance.max})'

    def update_slider2_label(self, instance, value):
        self.slider2_label.text = f'{value} ({instance.min}-{instance.max})'

    def update_slider3_label(self, instance, value):
        self.slider3_label.text = f'{value} ({instance.min}-{instance.max})'
    
    def start_stop(self, instance):
        if instance.text == 'Start':
            instance.text = 'Stop'
        else:
            instance.text = 'Start'
        



        print('Slider 1 value:', self.slider1.value)

if __name__ == '__main__':
    MyApp().run()