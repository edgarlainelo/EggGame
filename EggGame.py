from kivy.app import App
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle
from kivy.graphics import Rotate, PushMatrix, PopMatrix

from kivy.uix.slider import Slider
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

from kivy.config import Config

from kivy.lang import Builder
from kivy.event import EventDispatcher
from kivy.core.audio import SoundLoader

import random
import json
import os
import time

Config.set('graphics', 'resizable', True)


class Save():
    def __init__(self, **kwargs):
        app = App.get_running_app()

        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        self.save_json = {
            'coins': app.coins,
            'tillBreak': app.tillBreak,
            'clicks_count': app.clicks_count,
            'meteor_count': app.meteor_count,
            'hammer_count': app.hammer_count,
            'nuke_count': app.nuke_count,
            'count': app.count,
            'hammer': app.hammer,
            'meteor': app.meteor,
            'nuke': app.nuke,
            'egg_selected_dic': app.egg_selected_dic,
            'bought_eggs': app.bought_eggs,
            'new_ach': app.new_ach,
            'ach_list': app.ach_list,
            'restart_game': app.restart_game
        }


    def save_to_file(self):
        json_obj = json.dumps(self.save_json, indent = 4)

        try:
            with open(os.path.join(self.script_dir,"Save.txt"), 'w') as outfile:
                outfile.write(json_obj)
            
        except Exception as e:
            print(f"Error saving data: {e}")

        

    def update_data(self):
        """Update the save data from the app."""
        app = App.get_running_app()
        self.save_json.update({
            'coins': app.coins,
            'tillBreak': app.tillBreak,
            'clicks_count': app.clicks_count,
            'meteor_count': app.meteor_count,
            'hammer_count': app.hammer_count,
            'nuke_count': app.nuke_count,
            'count': app.count,
            'hammer': app.hammer,
            'meteor': app.meteor,
            'nuke': app.nuke,
            'egg_selected_dic': app.egg_selected_dic,
            'bought_eggs': app.bought_eggs,
            'new_ach': app.new_ach,
            'ach_list': app.ach_list,
            'restart_game': app.restart_game
        
            
        })    


    

class Achievments(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.9294, 0.8157, 0.698, 1)  # RGB + Alpha (background color)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect)

        self.script_dir  = os.path.dirname(os.path.abspath(__file__))

        

        self.btn_egg_page = Button(size_hint = (0.1, 0.1), pos_hint = {'x':0.015, 'y':0.875}, background_normal = os.path.join(self.script_dir, "EggPics","EggIcon.png"))
        self.btn_egg_page.bind(on_press = self.switch_egg)

        self.btn_settings_page = Button(size_hint = (0.1, 0.1), pos_hint = {'x':0.8825, 'y':0.875}, background_normal = os.path.join(self.script_dir, "OtherIcons","SettingIcon.png"))
        self.btn_settings_page.bind(on_press = self.switch_settings)


        self.add_widget(self.btn_egg_page)
        self.add_widget(self.btn_settings_page)


        self.scroll = ScrollView(size_hint=(1, 0.85), pos_hint={'x': 0, 'y': 0})
        self.add_widget(self.scroll)

        # BoxLayout as the container for the ScrollView
        self.scroll_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.scroll_layout.bind(minimum_height=self.scroll_layout.setter('height'))  # Adjust height automatically
        self.scroll.add_widget(self.scroll_layout)
        
        if len(app.ach_list) != 0:
            for i in app.ach_list:
                btn_ach = Button(text=i, size_hint=(1, None), height=100, background_normal = os.path.join(self.script_dir, "OtherIcons","Frame.png"))
                self.scroll_layout.add_widget(btn_ach)
        

        Clock.schedule_interval(self.check_achievements, 0.5)
        Clock.schedule_interval(self.check_hammer, 0.5)
        Clock.schedule_interval(self.check_meteor, 0.5)
        Clock.schedule_interval(self.check_nuke, 0.5)
        Clock.schedule_interval(self.del_ach, 0.5)
        
        self.ach_list = []

    def update_rect(self, *args):
        """Update the rectangle size and position."""
        self.rect.size = self.size
        self.rect.pos = self.pos
    

    def check_achievements(self, dt):
        
        app = App.get_running_app()
        
        if app.clicks_count >= app.count:
            # Add a new achievement button
            btn_ach = Button(text=f'Made {app.count} clicks', size_hint=(1, None), height=100, background_normal = os.path.join(self.script_dir, "OtherIcons","Frame.png"))
            self.scroll_layout.add_widget(btn_ach)
            app.ach_list.append(f'Made {app.count} clicks')

            app.count *= 10
            app.new_ach = True
            

    def check_hammer(self, dt):
        app = App.get_running_app()
        if (app.hammer_count >= app.hammer) and app.hammer == 1:
            btn_ach = Button(text=f'Used hammer {app.hammer} times', size_hint=(1, None), height=100, background_normal = os.path.join(self.script_dir, "OtherIcons","Frame.png"))
            self.scroll_layout.add_widget(btn_ach)
            app.ach_list.append(f'Used hammer {app.hammer} times')
            app.hammer += 9
            app.new_ach = True
            self.ach_list.append(btn_ach)
            
        elif (app.hammer_count >= app.hammer):
            btn_ach = Button(text=f'Used hammer {app.hammer} times', size_hint=(1, None), height=100, background_normal = os.path.join(self.script_dir, "OtherIcons","Frame.png"))
            self.scroll_layout.add_widget(btn_ach)
            app.ach_list.append(f'Used hammer {app.hammer} times')
            app.hammer += 10
            app.new_ach = True
            self.ach_list.append(btn_ach)
            
        else:
            pass

    def check_meteor(self, dt):
        app = App.get_running_app()
        if (app.meteor_count >= app.meteor) and app.meteor == 1:
            btn_ach = Button(text=f'Used meteor {app.meteor} times', size_hint=(1, None), height=100, background_normal = os.path.join(self.script_dir, "OtherIcons","Frame.png"))
            self.scroll_layout.add_widget(btn_ach)
            app.ach_list.append(f'Used meteor {app.meteor} times')
            app.meteor += 4
            app.new_ach = True
            self.ach_list.append(btn_ach)
            
        elif (app.meteor_count >= app.meteor):
            btn_ach = Button(text=f'Used meteor {app.meteor} times', size_hint=(1, None), height=100, background_normal = os.path.join(self.script_dir, "OtherIcons","Frame.png"))
            self.scroll_layout.add_widget(btn_ach)
            app.ach_list.append(f'Used meteor {app.meteor} times')
            app.meteor += 5
            app.new_ach = True
            self.ach_list.append(btn_ach)
            
        else:
            pass

    def check_nuke(self, dt):
        app = App.get_running_app()
        if app.nuke_count >= app.nuke:
            btn_ach = Button(text=f'Used nuke {app.nuke} times', size_hint=(1, None), height=100, background_normal = os.path.join(self.script_dir, "OtherIcons","Frame.png"))
            self.scroll_layout.add_widget(btn_ach)
            app.ach_list.append(f'Used nuke {app.nuke} times')
            app.nuke += 1
            app.new_ach = True
            self.ach_list.append(btn_ach)
            
            

    def del_ach(self, dt):
        app = App.get_running_app()

        if app.restart_game == True:
            for i in self.ach_list:
                self.scroll_layout.remove_widget(i)

            app.restart_game = False
            app.new_ach = False

    def switch_settings(self, button):
        app.screen_managet.transition = SlideTransition(direction = 'left')
        app.screen_managet.current = 'Settings'

    def switch_egg(self, button):
        app.screen_managet.transition = SlideTransition(direction = 'right')
        app.screen_managet.current = 'Egg'

class Settings(RelativeLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.9294, 0.8157, 0.698, 1)  # RGB + Alpha (background color)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        self.bind(size=self.update_rect, pos=self.update_rect)

        self.btn_egg_page = Button(size_hint = (0.1, 0.1), pos_hint = {'x':0.015, 'y':0.875}, background_normal = os.path.join(self.script_dir, "EggPics", "EggIcon.png"))
        self.btn_egg_page.bind(on_press = self.switch_egg)

        


        
        self.btn_sound_on_off = Button(size_hint = (0.1, 0.1), pos_hint = {'x':0.15, 'y':0.6}, background_normal = os.path.join(self.script_dir, "OtherIcons", "SoungOnIcon.png"))
        self.btn_sound_on_off.bind(on_press = self.sound_on_off)
        

        

        self.sound = SoundLoader.load(os.path.join(self.script_dir, "Sounds","EggBreakMusic.mp3"))
        self.sound_slider = Slider(min = 0, max = 100, size_hint = (0.4, 0.1), pos_hint = {'x':0.3, 'y':0.6}, value = 100)
        self.sound_slider.bind(value = self.sound_volume)

        self.add_widget(self.btn_egg_page)
        self.add_widget(self.btn_sound_on_off)
        self.add_widget(self.sound_slider)
        

        self.sound.loop = True
        self.sound.play()
        self.volumne_TF = True


    def update_rect(self, *args):
        """Update the rectangle size and position."""
        self.rect.size = self.size
        self.rect.pos = self.pos

    def sound_volume(self, instance, value):
        self.sound.volume = value/100

    def sound_on_off(self, button):
        if self.volumne_TF == True:
            self.volumne_TF = False
            self.sound.volume = 0
            self.sound_slider.value = 0
            self.sound_slider.max = 0
            self.sound.loop = False
            self.sound.stop()
            self.btn_sound_on_off.background_normal = os.path.join(self.script_dir, "OtherIcons", "SoundOffIcon.png")
        elif self.volumne_TF == False:
            self.volumne_TF = 1
            self.sound_slider.max = 100
            self.sound_slider.value = 100
            self.sound.loop = True
            self.sound.volume = 1
            self.sound.play()
            self.btn_sound_on_off.background_normal = os.path.join(self.script_dir, "OtherIcons", "SoungOnIcon.png")
            

    def switch_egg(self, button):
        app.screen_managet.transition = SlideTransition(direction = 'right')
        app.screen_managet.current = 'Egg'
    
    



class Store(RelativeLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.9294, 0.8157, 0.698, 1)  # RGB + Alpha (background color)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect)

        self.script_dir  = os.path.dirname(os.path.abspath(__file__))
        
        app = App.get_running_app()
        self.coinsLabel = Label(size_hint = (0.1, 0.1), pos_hint = {'x':0.45, 'y':0.875}, text = app.coins)
        self.add_widget(self.coinsLabel)
        app.bind(coins = lambda instance, value: self.update_coins_label(value))
        
        
        self.btn_egg_page = Button(size_hint = (0.1, 0.1), pos_hint = {'x':0.015, 'y':0.875}, background_normal = os.path.join(self.script_dir, "EggPics", "EggIcon.png"))
        self.btn_egg_page.bind(on_press = self.switch_egg)
        

        self.btn_settings_page = Button(size_hint = (0.1, 0.1), pos_hint = {'x':0.8825, 'y':0.875}, background_normal = os.path.join(self.script_dir, "OtherIcons", "SettingIcon.png"))
        self.btn_settings_page.bind(on_press = self.switch_settings)
        

        self.add_widget(self.btn_egg_page)
        self.add_widget(self.btn_settings_page)

        self.grid = GridLayout(cols = 2, size_hint = (0.5, 0.85), pos_hint = {'x':0.25,'y':0}, spacing=[20, 20])
        
        self.egg_buttons = {}

        Clock.schedule_interval(self.check_eggs_buttons, 1)
        

        #1-Icon, 2-Activated, 3-Buy
        self.egg_dict_list = {'norm_egg':[os.path.join(self.script_dir, "EggPics", "EggIcon.png"),os.path.join(self.script_dir, "EggPics", "EggActivated.png")],
        'ice_egg': [os.path.join(self.script_dir, "EggPics", "EggIceIcon.png"), os.path.join(self.script_dir, "EggPics", "EggIceActivated.png"), os.path.join(self.script_dir, "EggPics", "EggIceBuy.png")],
        'lava_egg': [os.path.join(self.script_dir, "EggPics", "EggLavaIcon.png"),os.path.join(self.script_dir, "EggPics", "EggLavaActivated.png"), os.path.join(self.script_dir, "EggPics", "EggLavaBuy.png")],
        'slime_egg': [os.path.join(self.script_dir, "EggPics", "EggSlimeIcon.png"),os.path.join(self.script_dir, "EggPics", "EggSlimeActivated.png"),os.path.join(self.script_dir, "EggPics", "EggSlimeBuy.png")],
        'gold_egg': [os.path.join(self.script_dir, "EggPics", "EggGoldIcon.png"), os.path.join(self.script_dir, "EggPics", "EggGoldActivated.png"),os.path.join(self.script_dir, "EggPics", "EggGoldBuy.png")],
        'metal_egg': [os.path.join(self.script_dir, "EggPics", "EggMetalIcon.png"),os.path.join(self.script_dir, "EggPics", "EggMetalActivated.png"), os.path.join(self.script_dir, "EggPics", "EggMetalBuy.png")],
        'air_egg': [os.path.join(self.script_dir, "EggPics", "EggAirIcon.png"), os.path.join(self.script_dir, "EggPics", "EggAirActivated.png"),os.path.join(self.script_dir, "EggPics", "EggAirBuy.png")],
        'water_egg': [os.path.join(self.script_dir, "EggPics", "EggWaterIcon.png"), os.path.join(self.script_dir, "EggPics", "EggWaterActivated.png"), os.path.join(self.script_dir, "EggPics", "EggWaterBuy.png")]
        }
        
        for egg in self.egg_dict_list:
            if app.bought_eggs[egg] == False:
                if egg == 'norm_egg':
                    self.btn_egg = Button(background_normal = self.egg_dict_list.get(egg)[1])
                    self.btn_egg.egg_id = egg
                    self.btn_egg.bind(on_press = lambda instance, egg_id = egg: self.buy_egg(instance, egg_id))
                    self.grid.add_widget(self.btn_egg)
                    self.egg_buttons[egg] = self.btn_egg
                else:
                    self.btn_egg = Button(background_normal = self.egg_dict_list.get(egg)[2])
                    self.btn_egg.egg_id = egg
                    self.btn_egg.bind(on_press = lambda instance, egg_id = egg: self.buy_egg(instance, egg_id))
                    self.grid.add_widget(self.btn_egg)
                    self.egg_buttons[egg] = self.btn_egg
            elif app.bought_eggs[egg] == True and app.egg_selected_dic[egg] ==True:
                self.btn_egg = Button(background_normal = self.egg_dict_list.get(egg)[1])
                self.btn_egg.egg_id = egg
                self.btn_egg.bind(on_press = lambda instance, egg_id = egg: self.buy_egg(instance, egg_id))
                self.grid.add_widget(self.btn_egg)
                self.egg_buttons[egg] = self.btn_egg
            
            elif app.bought_eggs[egg] == True and app.egg_selected_dic[egg] == False:
                self.btn_egg = Button(background_normal = self.egg_dict_list.get(egg)[0])
                self.btn_egg.egg_id = egg
                self.btn_egg.bind(on_press = lambda instance, egg_id = egg: self.buy_egg(instance, egg_id))
                self.grid.add_widget(self.btn_egg)
                self.egg_buttons[egg] = self.btn_egg
                
            else:
                pass

    

        self.add_widget(self.grid)

        for active_egg in app.egg_selected_dic:
            if app.egg_selected_dic[active_egg] == True:
                self.active_egg = active_egg
                


    def check_eggs_buttons(self, dt):
        
        try:
            for i in app.bought_eggs.items():

                
                if i[1] == True and i[0] != 'norm_egg' and app.egg_selected_dic[i[0]] != True:
                    
                    if (self.egg_buttons[i[0]].background_normal != self.egg_dict_list[i[0]][0]):
                        self.egg_buttons[i[0]].background_normal = self.egg_dict_list[i[0]][0]
                    else:
                        continue
                    
                elif i[1] == False and i[0] != 'norm_egg':
                    
                    self.egg_buttons[i[0]].background_normal = self.egg_dict_list[i[0]][2]
                    
        except Exception as e:
            print(f'Error {e}')
            
                

        
    def update_rect(self, *args):
        """Update the rectangle size and position."""
        self.rect.size = self.size
        self.rect.pos = self.pos

    def update_coins_label(self, value):
        self.coinsLabel.text = str(value)

    def switch_egg(self, button):
        app.screen_managet.transition = SlideTransition(direction ='right')
        app.screen_managet.current = 'Egg'

    def switch_settings(self, button):
        app.screen_managet.transition = SlideTransition(direction = 'left')
        app.screen_managet.current = 'Settings'

    def buy_egg(self, button, egg_id):
        app = App.get_running_app()

        # Update the previous button before changing the active egg
        previous_button = self.egg_buttons[self.active_egg]
        previous_button.background_normal = self.egg_dict_list[self.active_egg][0]
        

        # Handle newly selected egg
        if not app.bought_eggs[egg_id]:
            if int(app.coins) >= 250000:
                app.coins = str(int(app.coins) - 250000)
                app.bought_eggs[egg_id] = True

                # Update egg selection logic
                app.egg_selected_dic[self.active_egg] = False
                app.egg_selected_dic[egg_id] = True
                self.active_egg = egg_id

                # Update the new button's icon
                if egg_id == 'norm_egg':
                    button.background_normal = self.egg_dict_list[egg_id][1]  # Activated icon for norm_egg
                else:
                    button.background_normal = self.egg_dict_list[egg_id][1]  # Activated icon for other eggs
            else:
                previous_button = self.egg_buttons[self.active_egg]
                previous_button.background_normal = self.egg_dict_list[self.active_egg][1]

        elif app.bought_eggs[egg_id]:
            app.egg_selected_dic[self.active_egg] = False
            app.egg_selected_dic[egg_id] = True
            self.active_egg = egg_id

            # Update the new button's icon
            if egg_id == 'norm_egg':
                button.background_normal = self.egg_dict_list[egg_id][1]  # Activated icon for norm_egg
            else:
                button.background_normal = self.egg_dict_list[egg_id][1]  # Activated icon for other eggs
        else:
            pass
        
    
    


class TouchableLabel(ButtonBehavior, Label):
    pass
        


class EggPage(RelativeLayout):
    
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.9294, 0.8157, 0.698, 1)  # RGB + Alpha (background color)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect)

        app = App.get_running_app()
        
        self.angle = 0

        self.script_dir  = os.path.dirname(os.path.abspath(__file__))

        self.eggImage = Image(source = os.path.join(self.script_dir, "EggPics","EggPic.png"))
        self.add_widget(self.eggImage)

        
        self.touchable_egg_label = TouchableLabel(text=app.tillBreak, font_size=32)
        self.touchable_egg_label.bind(on_press=lambda instance: self.on_egg_click(self.touchable_egg_label))
        self.add_widget(self.touchable_egg_label)
        

        
        self.canvas_widget = Widget()
        
        self.coinImage = Image(source = os.path.join(self.script_dir, "OtherIcons", "CoinPic.png"), pos_hint = {'x':0.04, 'y':0.3}, size_hint = (0.05, 0.05))
        self.add_widget(self.coinImage)
        self.coinsLabel = Label(size_hint = (0.1, 0.1), pos_hint = {'x':0.015, 'y':0.23}, text = app.coins)

        self.coinImage = Image(source = os.path.join(self.script_dir, "OtherIcons", "CoinPic.png"), pos_hint = {'x':0.07, 'y':0.54}, size_hint = (0.03, 0.03))
        self.add_widget(self.coinImage)
        self.coinsHammer = Label(size_hint = (0.1, 0.1), pos_hint = {'x':0.005, 'y':0.505}, text = str(100))
        self.add_widget(self.coinsHammer)

        self.coinImage = Image(source = os.path.join(self.script_dir, "OtherIcons", "CoinPic.png"), pos_hint = {'x':0.07, 'y':0.69}, size_hint = (0.03, 0.03))
        self.add_widget(self.coinImage)
        self.coinsMeteor = Label(size_hint = (0.1, 0.1), pos_hint = {'x':0.002, 'y':0.655}, text = str(1000))
        self.add_widget(self.coinsMeteor)

        self.coinImage = Image(source = os.path.join(self.script_dir, "OtherIcons", "CoinPic.png"), pos_hint = {'x':0.07, 'y':0.84}, size_hint = (0.03, 0.03))
        self.add_widget(self.coinImage)
        self.coinsNuke = Label(size_hint = (0.1, 0.1), pos_hint = {'x':0, 'y':0.805}, text = str(10000))
        self.add_widget(self.coinsNuke)

        
        app.bind(coins = lambda instance, value: self.update_coins_label(value))
        

        self.btn_store_page = Button(size_hint = (0.1, 0.1), pos_hint = {'x':0.015, 'y':0.375}, background_normal = os.path.join(self.script_dir, "OtherIcons", "SkinsIcon.png"))
        self.btn_store_page.bind(on_press = self.switch_store)

        self.btn_settings_page = Button(size_hint = (0.1, 0.1), pos_hint = {'x':0.8825, 'y':0.875}, background_normal = os.path.join(self.script_dir, "OtherIcons", "SettingIcon.png"))
        self.btn_settings_page.bind(on_press = self.switch_settings)

        self.hammer = Button(size_hint = (0.1, 0.1), pos_hint = {'x':0.015, 'y':0.575}, background_normal = os.path.join(self.script_dir, "HammerMeteorNuke", "HammerIcon.png"))
        self.hammer.bind(on_press = self.hammerBreak)
        
        self.meteor = Button(size_hint = (0.1, 0.1), pos_hint = {'x':0.015, 'y':0.725}, background_normal = os.path.join(self.script_dir, "HammerMeteorNuke", "MeteorIcon.png"))
        self.meteor.bind(on_press = self.meteorBreak)

        self.nuke = Button(size_hint = (0.1, 0.1), pos_hint = {'x':0.015, 'y':0.875}, background_normal = os.path.join(self.script_dir, "HammerMeteorNuke", "NukeIcon.png"))
        self.nuke.bind(on_press = self.nukeBreak)

        self.btn_achievments_page = Button(size_hint = (0.1, 0.1), pos_hint = {'x':0.8825, 'y':0.775}, background_normal = os.path.join(self.script_dir, "OtherIcons", "AchievIcon.png"))
        self.btn_achievments_page.bind(on_press = self.switch_achivments)

        

        
        self.add_widget(self.btn_store_page)
        self.add_widget(self.btn_settings_page)
        self.add_widget(self.hammer)
        self.add_widget(self.meteor)
        self.add_widget(self.nuke)
        self.add_widget(self.coinsLabel)
        self.add_widget(self.btn_achievments_page)

        Clock.schedule_interval(self.check_egg, 0.5)
        Clock.schedule_interval(self.check_achievements, 0.5)
        Clock.schedule_interval(self.check_eggs_won, 1)
        
        
    def update_rect(self, *args):
        """Update the rectangle size and position."""
        self.rect.size = self.size
        self.rect.pos = self.pos

    def on_egg_click(self, label):
        self.break_egg(label)  # Trigger coin increase or other logic
        self.shake_egg()  # Trigger the shake effect
        self.coin_appear()
        self.minus_appear()

    def minus_appear(self):
        x = random.uniform(0.4, 0.5)
        
        minus = Label(text = '-1', pos_hint = {'x':x, 'y': 0.6}, size_hint = (0.1, 0.1))
        anim = Animation(pos_hint={'x': x, 'y':0.6+0.1}, duration = 0.5, opacity =0)
        self.add_widget(minus)
        
        anim.bind(on_complete=lambda *args: self.remove_widget(minus))

        anim.start(minus)


    def coin_appear(self):
        x = random.uniform(0.25, 0.75)
        y = random.uniform(0.25, 0.75)

        coinPop = Image(source = os.path.join(self.script_dir, "OtherIcons", "CoinPic.png"), pos_hint ={'x':x, 'y':y}, size_hint = (0.05, 0.05))
        anim1 = Animation(pos_hint={'x': x, 'y': y + 0.05}, duration=0.5, opacity=0)
        
        self.add_widget(coinPop)

        anim1.bind(on_complete=lambda *args: self.remove_widget(coinPop))

        # Start the animation
        anim1.start(coinPop)


        

    def shake_egg(self):
        initial_pos = self.eggImage.pos
        x, y = initial_pos

        

        # Create the shake animation
        anim1 = Animation(pos=(0 + 10, y), duration=0.05)
        anim2 = Animation(pos=(0 - 10, y), duration=0.05)
        anim3 = Animation(pos=(0, y), duration=0.05)

        # Chain the animations together to create a shaking effect
        shake_animation = anim1 + anim2 + anim3

        # Apply the animation to the egg image
        shake_animation.start(self.eggImage)
        

    def update_coins_label(self, value):
        self.coinsLabel.text = str(value)


    def change_prize_size(self, dt):
        self.x_prize += 10
        self.y_prize += 10
        

        self.rect_prize.size = (self.x_prize, self.y_prize)

        if self.rect_prize.size == (200,200):
            Clock.unschedule(self.change_prize_size)

            self.prize_label = Label(pos_hint = {'x': 0, 'y': 0}, size = (200, 200), text= 'You have won\n    new egg!')
            self.add_widget(self.prize_label)


    def restart_game(self, instance):
        self.remove_widget(self.rect_prize)
        self.do_layout()

        for egg_key in app.bought_eggs.keys():
            if egg_key == 'norm_egg':
                app.egg_selected_dic.update({egg_key: True})
            else:
                app.bought_eggs.update({egg_key:False})
                app.egg_selected_dic.update({egg_key: False})


        
        
        app.tillBreak = str(1000000)
        app.coins = str(0)
        app.clicks_count = 0
        app.meteor_count = 0
        app.hammer_count = 0
        app.nuke_count = 0
        app.new_ach = False
        app.hammer = 1
        app.meteor = 1
        app.nuke = 1
        app.count = 100
        app.ach_list = []
        app.restart_game = True

        Clock.schedule_interval(self.check_eggs_won, 1)
        

            

    def endGame(self):
        
        count = 0
        for true_False in list(app.bought_eggs.values()):
            if true_False == True or true_False == 'true':
                count += 1
            else:
                pass

        if count >= 8:

            Clock.unschedule(self.check_eggs_won)

            self.rect_prize = Button(pos = (365, 350),size_hint = (0.4,0.2),text = 'You have got all the eggs! Click to restart!' ,background_normal = os.path.join(self.script_dir, "OtherIcons", "Frame.png"))
            
            self.rect_prize.bind(on_press = self.restart_game)
            
            self.add_widget(self.rect_prize)
            
        else:
            check_prizes_list = list(app.bought_eggs.items())
            
            affordable_prizes = []

            for i in check_prizes_list:
                if i[1] == False:
                    
                    affordable_prizes.append(i)
                    app.tillBreak = str(1000000)
                    self.touchable_egg_label.text = app.tillBreak

            
            if len(affordable_prizes) != 0:

                rand_prize = random.choice(affordable_prizes)
                
                
                if rand_prize[1] == False:
                    
                        
                    self.rect_prize = Button(pos = (450, 350),size_hint = (0.25,0.2),text = 'Click me and win a prize!' ,background_normal = os.path.join(self.script_dir, "OtherIcons", "Frame.png"))
                    self.rect_prize.bind(on_press = lambda instance: self.new_egg_prize(rand_prize))
                    self.add_widget(self.rect_prize)
                        
            else:
                pass

        
            
    def new_egg_prize(self, rand_prize):

        app.bought_eggs.update({rand_prize[0]:True})
        self.remove_widget(self.rect_prize)
        

    def break_egg(self, label):
        
        
        app.coins = str(int(app.coins)+1)
        app.tillBreak = str(int(app.tillBreak)-1)
        self.touchable_egg_label.text = app.tillBreak
        app.clicks_count = app.clicks_count+1
        


        if int(app.tillBreak) <= 0:
            
            self.endGame()

    

    def hammerBreak(self, button):
        
        self.angle = 0      
        self.hammer.unbind(on_press = self.hammerBreak)
        if int(app.coins)>=100:
            with self.canvas:
                
                self.push_matrix = PushMatrix()
                self.rotation = Rotate(origin=(725, 575), angle=self.angle)
                self.rect = Rectangle(pos=(650, 500), size=(150, 150), source=os.path.join(self.script_dir, "HammerMeteorNuke", "Hammer.png"))
                self.pop_matrix = PopMatrix()

            Clock.schedule_interval(self.update_rotation, 1 / 30)
            
        else:
            pass

        

    def update_rotation(self, dt):
        """Updates the angle of rotation."""
        self.angle += 10
        self.rotation.angle = self.angle

        
        
        if self.angle >= 90:
            Clock.unschedule(self.update_rotation)

            self.canvas.remove(self.push_matrix)  # Remove PushMatrix
            self.canvas.remove(self.rotation)    # Remove Rotate transformation
            self.canvas.remove(self.rect)        # Remove the Rectangle
            self.canvas.remove(self.pop_matrix)

            app.tillBreak = str(int(app.tillBreak) - 100)
            app.coins = str(int(app.coins) - 100)
            self.touchable_egg_label.text = app.tillBreak
            app.hammer_count += 1
            
            minus = Label(text = '-100', pos_hint = {'x':0.45, 'y': 0.6}, size_hint = (0.1, 0.1))
            anim = Animation(pos_hint={'x': 0.45, 'y':0.6+0.1}, duration = 1, opacity =0)
            self.add_widget(minus)
            
            anim.bind(on_complete=lambda *args: self.remove_widget(minus))

            anim.start(minus)

            self.shake_egg()
            self.hammer.bind(on_press = self.hammerBreak)
            

        if int(app.tillBreak) <= 0:
            self.endGame()

        
    def check_eggs_won(self, dt):
        
        count = 0
        for true_False in list(app.bought_eggs.values()):
            if true_False == True or true_False == 'true':
                count += 1
            else:
                pass
        
        if count >= 8:
            self.endGame()

        

        
            


    def meteorBreak(self, button):
        
        def complete_anim(animation, widget):
            self.remove_widget(meteor_icon)

            
            app.tillBreak = str(int(app.tillBreak)-1000)
            app.coins = str(int(app.coins)-1000)
            self.touchable_egg_label.text = app.tillBreak
            app.meteor_count += 1

    
            minus = Label(text = '-1000', pos_hint = {'x':0.45, 'y': 0.6}, size_hint = (0.1, 0.1))
            anim = Animation(pos_hint={'x': 0.45, 'y':0.6+0.1}, duration = 1, opacity =0)
            self.add_widget(minus)
            
            anim.bind(on_complete=lambda *args: self.remove_widget(minus))

            anim.start(minus)
            self.shake_egg()

            
            if int(app.tillBreak) <= 0:
                self.endGame()
                
                
            


        meteor_icon = Image(source = os.path.join(self.script_dir, "HammerMeteorNuke","Meteor.png"), pos_hint ={'x':1, 'y':1}, size_hint = (1, 1))
        
        

        anim1 = Animation(pos_hint = {'x': 0.1, 'y': 0.1}, duration = 1)
        anim1.bind(on_complete = complete_anim)
        if int(app.coins) >= 1000:
            self.add_widget(meteor_icon)
            anim1.start(meteor_icon)
        else:
            pass

    

    def nukeBreak(self, button):
        
        def complete_anim(animation, widget):
            self.remove_widget(nuke_icon)
            
            app.tillBreak = str(int(app.tillBreak)-10000)
            app.coins = str(int(app.coins)-10000)
            self.touchable_egg_label.text = app.tillBreak
            app.nuke_count += 1


            minus = Label(text = '-10000', pos_hint = {'x':0.45, 'y': 0.6}, size_hint = (0.1, 0.1))
            anim = Animation(pos_hint={'x': 0.45, 'y':0.6+0.1}, duration = 1, opacity =0)
            self.add_widget(minus)
            
            anim.bind(on_complete=lambda *args: self.remove_widget(minus))

            anim.start(minus)
            self.shake_egg()

            if int(app.tillBreak) <= 0:
                self.endGame()
                
                
            


        nuke_icon = Image(source = os.path.join(self.script_dir, "HammerMeteorNuke", "Nuke.png"), pos_hint ={'x':0, 'y':1}, size_hint = (1, 1))
        
        

        anim1 = Animation(pos_hint = {'x': 0, 'y': 0.1}, duration = 1)
        anim1.bind(on_complete = complete_anim)

        if int(app.coins) >= 10000:
            self.add_widget(nuke_icon)
            anim1.start(nuke_icon)
        else:
            pass
         
        
    def switch_store(self, button):
        app.screen_managet.transition = SlideTransition(direction='left')
        app.screen_managet.current = 'Skins'

    def switch_settings(self, button):
        app.screen_managet.transition = SlideTransition(direction = 'left')
        app.screen_managet.current = 'Settings'

    def switch_achivments(self, button):
        
        app.screen_managet.transition = SlideTransition(direction = 'left')
        app.screen_managet.current = 'Achievments'
        app.new_ach = False
        self.btn_achievments_page.background_normal = os.path.join(self.script_dir, "OtherIcons", "AchievIcon.png")
        
        


    
    def check_egg(self, instance):
        app = App.get_running_app()

        if app.egg_selected_dic["norm_egg"] == True:
            self.eggImage.source = os.path.join(self.script_dir, "EggPics", "EggPic.png")
        elif app.egg_selected_dic['ice_egg'] == True:
            self.eggImage.source = os.path.join(self.script_dir, "EggPics", "EggIcePic.png")
        elif app.egg_selected_dic['lava_egg'] == True:
            self.eggImage.source = os.path.join(self.script_dir, "EggPics", "EggLavaPic.png")
        elif app.egg_selected_dic['slime_egg'] == True:
            self.eggImage.source = os.path.join(self.script_dir, "EggPics", "EggSlimePic.png")
        elif app.egg_selected_dic['air_egg'] == True:
            self.eggImage.source = os.path.join(self.script_dir, "EggPics", "EggAirPic.png")
        elif app.egg_selected_dic['water_egg'] == True:
            self.eggImage.source = os.path.join(self.script_dir, "EggPics", "EggWaterPic.png")
        elif app.egg_selected_dic['gold_egg'] == True:
            self.eggImage.source = os.path.join(self.script_dir, "EggPics", "EggGoldPic.png")
        elif app.egg_selected_dic['metal_egg'] == True:
            self.eggImage.source = os.path.join(self.script_dir, "EggPics", "EggMetalPic.png")


    def check_achievements(self, instance):
        app = App.get_running_app()
        
        if app.new_ach == True:
            self.btn_achievments_page.background_normal = os.path.join(self.script_dir, "OtherIcons", "AchievAlertIcon.png")
        elif app.new_ach == False:
            self.btn_achievments_page.background_normal = os.path.join(self.script_dir, "OtherIcons", "AchievIcon.png")


class MyApp(App):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    with open(os.path.join(script_dir, "Save.txt"), 'r') as save_file:
        file = json.load(save_file)
    
    coins = StringProperty(file.get('coins')) 
    tillBreak = StringProperty(file.get('tillBreak'))  
    clicks_count = NumericProperty(int(file.get('clicks_count')))
    meteor_count = NumericProperty(int(file.get('meteor_count')))
    hammer_count = NumericProperty(int(file.get('hammer_count')))
    nuke_count = NumericProperty(int(file.get('nuke_count')))
    egg_selected_dic = file.get('egg_selected_dic')
    bought_eggs =file.get('bought_eggs')
    new_ach = file.get('new_ach')
    ach_list = file.get('ach_list')
    hammer = file.get('hammer')
    count = file.get('count')
    meteor = file.get('meteor')
    nuke = file.get('nuke')
    restart_game = file.get('restart_game')
    
    
    
    
    def build(self):
        
        self.screen_managet = ScreenManager()

        self.safe_managment = Save()
        self.achPage = Achievments()
        self.storePage = Store()
        self.eggPage = EggPage()

        
        screen = Screen(name = 'Egg')
        screen.add_widget(self.eggPage)
        self.screen_managet.add_widget(screen)

        screen = Screen(name = 'Achievments')
        screen.add_widget(self.achPage)
        self.screen_managet.add_widget(screen)
        
        screen = Screen(name='Skins')
        screen.add_widget(self.storePage)
        self.screen_managet.add_widget(screen)

        self.settingsPage = Settings()
        screen = Screen(name = 'Settings')
        screen.add_widget(self.settingsPage)
        self.screen_managet.add_widget(screen)

        Clock.schedule_interval(self.periodic_save, 0.5)

        return self.screen_managet

    def periodic_save(self, dt):
        self.safe_managment.update_data()
        self.safe_managment.save_to_file()
    


app = MyApp()
app.run()