from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.label import Label
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
        tabbed_panel = TabbedPanel(do_default_tab=False, tab_pos='left_mid')

        # Settings tab
        settings_tab = TabbedPanelHeader(text='Settings')
        settings_layout = BoxLayout(orientation='vertical')

        self.slider1 = Slider(min=0, max=100, value=50)
        self.slider2 = Slider(min=0, max=100, value=50)
        self.slider3 = Slider(min=0, max=100, value=50)

        self.slider1_label = Label(text=f'{self.slider1.value} ({self.slider1.min}-{self.slider1.max})')
        self.slider2_label = Label(text=f'{self.slider2.value} ({self.slider2.min}-{self.slider2.max})')
        self.slider3_label = Label(text=f'{self.slider3.value} ({self.slider3.min}-{self.slider3.max})')

        self.slider1.bind(value=self.update_slider1_label)
        self.slider2.bind(value=self.update_slider2_label)
        self.slider3.bind(value=self.update_slider3_label)

        settings_layout.add_widget(self.slider1)
        settings_layout.add_widget(self.slider1_label)
        settings_layout.add_widget(self.slider2)
        settings_layout.add_widget(self.slider2_label)
        settings_layout.add_widget(self.slider3)
        settings_layout.add_widget(self.slider3_label)

        apply_button = Button(text='Apply Settings')
        apply_button.bind(on_release=self.apply_settings)

        settings_layout.add_widget(apply_button)

        settings_tab.content = settings_layout
        tabbed_panel.add_widget(settings_tab)


        # Graphs tab
        graphs_tab = TabbedPanelHeader(text='Graphs')

        self.graph = MyGraph()
       # self.graph.size_hint = (1, 1)

        # Create a BoxLayout to contain the slider and the graph
        graph_layout = BoxLayout(orientation='horizontal')

        # Add slider for adjusting the y scale of the graph
        self.y_scale_slider = Slider(min=0.1, max=2, value=1, orientation='vertical', size_hint_x = 0.1)
        self.y_scale_slider.bind(value=self.update_y_scale)

        # Add the slider and the graph to the graph_layout
        graph_layout.add_widget(self.y_scale_slider)
        graph_layout.add_widget(self.graph)

        # Add slider for adjusting the x scale of the graph
        self.x_scale_slider = Slider(min=0.1, max=2, value=1, size_hint_y = 0.1)
        self.x_scale_slider.bind(value=self.update_x_scale)

        # Add the x scale slider below the graph_layout
        main_layout = BoxLayout(orientation='vertical')
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
    def apply_settings(self, instance):
        print('Slider 1 value:', self.slider1.value)
        print('Slider 2 value:', self.slider2.value)
        print('Slider 3 value:', self.slider3.value)

if __name__ == '__main__':
    MyApp().run()