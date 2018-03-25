#!/usr/bin/python
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy_communication import *
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from text_handling import *
from kivy.graphics.context_instructions import (Color)
from kivy.graphics.vertex_instructions import (Ellipse)
from kivy.graphics import *
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
import numpy as np
from os.path import join, dirname

try:
    from jnius import autoclass
    from android.runnable import run_on_ui_thread

    android_api_version = autoclass('android.os.Build$VERSION')
    AndroidView = autoclass('android.view.View')
    # AndroidPythonActivity = autoclass('org.renpy.android.PythonActivity')
    AndroidPythonActivity = autoclass('org.kivy.android.PythonActivity')

    Logger.debug(
        'Application runs on Android, API level {0}'.format(
            android_api_version.SDK_INT
        )
    )
except ImportError:
    def run_on_ui_thread(func):
        def wrapper(*args):
            Logger.debug('{0} called on non android platform'.format(
                func.__name__
            ))
        return wrapper

class SetupScreenRoom(Screen):
    ip = ''

class ZeroScreen(Screen):
    pass


class QuestionScreen(Screen):
   # current_question = 0

    def __init__(self, the_app,  **kwargs):
        super(Screen, self).__init__()
        self.the_app = the_app
        self.current_question = -1
        self.init_circles()
        self.phrases_A = []
        self.phrases_B = []
        self.number_of_questions = 0
        self.question = None
        self.sound_question = None
        self.pre_post_flag = None
        self.repeat_question = False

        self.sounds_A = []
        self.sounds_B = []

    def init_sounds(self):
        if self.pre_post_flag == 1:
            self.phrases_A = ['growth_02_buffy',
                              'fixed_03_buffy',
                              'growth_04_buffy',
                              'fixed_05_buffy',
                              'fixed_07_buffy',
                              'growth_08_buffy',
                              'fixed_09_buffy',
                              'growth_10_buffy',
                              'fixed_11_buffy',
                              'growth_12_buffy']
            self.phrases_B = ['fixed_02_fluffy',
                              'growth_03_fluffy',
                              'fixed_04_fluffy',
                              'growth_05_fluffy',
                              'growth_07_fluffy',
                              'fixed_08_fluffy',
                              'growth_09_fluffy',
                              'fixed_10_fluffy',
                              'growth_11_fluffy',
                              'fixed_12_fluffy']
        elif self.pre_post_flag == 2:
            self.phrases_A = ['fixed_01_buffy',
                              'growth_02_buffy',
                              'fixed_03_buffy',
                              'growth_04_buffy',
                              'growth_06_buffy',
                              'fixed_07_buffy',
                              'growth_08_buffy',
                              'fixed_13_buffy',
                              'growth_16_buffy',
                              'fixed_17_buffy']
            self.phrases_B = ['growth_01_fluffy',
                              'fixed_02_fluffy',
                              'growth_03_fluffy',
                              'fixed_04_fluffy',
                              'fixed_06_fluffy',
                              'growth_07_fluffy',
                              'fixed_08_fluffy',
                              'growth_13_fluffy',
                              'fixed_16_fluffy',
                              'growth_17_fluffy']
        self.number_of_questions = len(self.phrases_A)
        self.question = 'which'
        self.sound_question = SoundLoader.load("./sounds/" + self.question + ".wav")

        self.intro1_1 = 'intro1_1'
        self.sound_intro1_1 = SoundLoader.load("./sounds/" + self.intro1_1 + ".wav")

        self.intro1_2 = 'intro1_2'
        self.sound_intro1_2 = SoundLoader.load("./sounds/" + self.intro1_2 + ".wav")

        self.intro1_3 = 'intro1_3'
        self.sound_intro1_3 = SoundLoader.load("./sounds/" + self.intro1_3 + ".wav")

        self.intro2 = 'intro2'
        self.sound_intro2 = SoundLoader.load("./sounds/" + self.intro2 + ".wav")

        self.sounds_A = []
        self.sounds_B = []

        for n in range(len(self.phrases_A)):
            self.sounds_A.append(SoundLoader.load("./sounds/" + self.phrases_A[n] + ".wav"))
            self.sounds_B.append(SoundLoader.load("./sounds/" + self.phrases_B[n] + ".wav"))

        self.perm = np.random.permutation(len(self.phrases_A)) # permutation on the question's

    def init_circles(self):
        self.ids['right_circle'].opacity = 0
        self.ids['left_circle'].opacity = 0


    def show_right_circle(self):
        self.ids['right_circle'].opacity = 1
        self.ids['left_circle'].opacity = 0
        c=self.ids['right_circle']
        print(c)
        self.animate_circle(c)

    def show_left_circle(self):
        self.ids['right_circle'].opacity = 0
        self.ids['left_circle'].opacity = 1
        self.animate_circle(self.ids['left_circle'])

    def animate_circle(self, the_circle):
         Animation.cancel_all(self)
         x = the_circle.x
         y = the_circle.y
         anim = Animation(x=x, y=y-20, duration=1, t='in_out_circ') + Animation(x=x, y=y, duration=1, t='in_out_circ')
         #anim.repeat = True
         anim.start(the_circle)

    def no_circles(self):
        self.ids['right_circle'].opacity = 0
        self.ids['left_circle'].opacity = 0

    def introduction1_1(self, *args):
        print "introduction1_1"
        self.show_right_circle()
        self.sound_intro1_1.bind(on_stop=lambda d: Clock.schedule_once(self.introduction1_2, 0.8))
        self.sound_intro1_1.play()


    def introduction1_2(self, *args):
        print "introduction1_2"
        self.show_left_circle()
        self.sound_intro1_2.bind(on_stop=lambda d: self.introduction1_3())
        self.sound_intro1_2.play()


    def introduction1_3(self):
        print "introduction1_2"
        self.no_circles()
        self.sound_intro1_3.bind(on_stop=lambda d: self.introduction2())
        self.sound_intro1_3.play()


    def introduction2(self):
        print "introduction2"
        self.sound_intro2.bind(on_stop=lambda d: Clock.schedule_once(self.next_question, 2.0))
        self.sound_intro2.play()

    def first_phrase(self, current_question):
        KL.log.insert(action=LogAction.play, obj=self.phrases_A[current_question], comment='play_first_audio')
        print self.phrases_A[current_question]
        self.show_right_circle()
     #   TTS.speak(self.phrases_A[current_question - 1], TTS.finished)
        if not self.repeat_question:
            self.sounds_A[current_question].bind(on_stop=lambda d: self.second_phrase(current_question))
        self.sounds_A[current_question].play()

    def second_phrase(self, current_question):
        KL.log.insert(action=LogAction.play, obj=self.phrases_B[current_question], comment='play_second_audio')
        print self.phrases_B[current_question]
        self.show_left_circle()
    #    TTS.speak(self.phrases_B[current_question - 1], TTS.finished)
        if not self.repeat_question:
            self.sounds_B[current_question].bind(on_stop=lambda d: self.question_phrase())
        self.sounds_B[current_question].play()


    def question_phrase(self, *args):
        print self.question
        self.repeat_question = True
        self.no_circles()
        self.enable_buttons()
        #self.sound_question.bind(on_stop=lambda d: Clock.schedule_once(self.enable_buttons,0.5))
        self.sound_question.play()

        #TTS.speak(self.question, TTS.finished)

    def enable_buttons(self):
        print 'buttons enabled'
        self.ids['play_again'].opacity = 1
        self.ids['play_again'].disabled = False
        self.ids['A_button'].disabled = False
        self.ids['B_button'].disabled = False


    def disable_buttons(self):
        print 'buttons disabled'
        self.ids['play_again'].opacity = 0
        self.ids['play_again'].disabled = True
        self.ids['A_button'].disabled = True
        self.ids['B_button'].disabled = True

    def next_question(self, *args):
        print("next_question")
        self.repeat_question = False
        self.current_question += 1
        self.disable_buttons()
        self.ids['A_button'].name = str(self.perm[self.current_question] ) + '_A_' + self.phrases_A[self.perm[self.current_question]]
        self.ids['B_button'].name = str(self.perm[self.current_question] ) + '_B_' + self.phrases_B[self.perm[self.current_question]]

   #     self.sm.current = 'question_screen'
        self.first_phrase(self.perm[self.current_question])

    def pressed_play_again(self):
        print("press_play_again")
        KL.log.insert(action=LogAction.press, obj="play_again", comment='play_again')
        self.sound_question.stop()
        self.disable_buttons()
        #self.ids['A_button'].name = str(self.perm[self.current_question]) + '_A_' + self.phrases_A[self.perm[self.current_question]]
        #self.ids['B_button'].name = str(self.perm[self.current_question]) + '_B_' + self.phrases_B[self.perm[self.current_question]]
        #     self.sm.current = 'question_screen'
        self.first_phrase(self.perm[self.current_question])


    def pressed(self, answer, the_button):
            print("pressed", answer)
            KL.log.insert(action=LogAction.press, obj=answer, comment='user_answer')
            self.sound_question.stop()
            if self.current_question >= self.number_of_questions-1:
                self.end_game()
            else:
                #self.animate_flufbuf(the_button)
                #self.disable_buttons()
                Clock.schedule_once(self.delay, 0.5)
                self.disable_buttons()


    def animate_flufbuf(self, the_button):
        #not in use
        Animation.cancel_all(self)
        x = the_button.x
        y = the_button.y
        anim = Animation(x=x - 10, y=y - 10) + Animation(x=x, y=y, duration=5, t='out_bounce')
        anim.start(the_button)


    def delay(self, *args):
        self.next_question()
        return False

    def end_game(self):
        self.ids["the_end"].opacity = 1
        self.disable_buttons()
        #self.the_app.stop()

class left_circle(Widget):
    pass

class MindsetAssessmentApp(App):


    def build(self):

        self.sm = ScreenManager()
        self.sm.add_widget(SetupScreenRoom(name='setup_screen_room'))
        self.sm.current = 'setup_screen_room'

        return self.sm

    def on_start(self):
        self.android_set_hide_menu()

    def init_communication(self, ip_addr):
        self.local_ip = ip_addr
        KC.start(the_ip=self.local_ip, the_parents=[self])  # 127.0.0.1

        if ip_addr == "":
            self.on_connection()

    def on_connection(self):
        self.zero_screen = ZeroScreen(name='zero_screen')
        self.android_set_hide_menu()
        self.sm.add_widget(self.zero_screen)

        try:
            with open(join(dirname(self.user_data_dir),"pid_initial.txt"), 'r') as id_f:
                print "hi"
                line = id_f.readlines()
                line = line[0].split(";")
                print line[0], line[1]
                #print self.zero_screen.subject_id.text, self.zero_screen.subject_initial.text
                self.zero_screen.subject_initial.text = line[1]
                self.zero_screen.subject_id.text = line[0]

                id_f.close()
        except Exception as e:
            print e

        self.question_screen = QuestionScreen(name='question_screen',the_app=self)
        self.sm.add_widget(self.question_screen)
        self.sm.current = 'zero_screen'

    def press_connect_button(self, ip_addr):
        # To-Do: save previous ip input
        print ip_addr
        self.init_communication(ip_addr)

    def start_assessment(self, pre_post_flag, id, initial):
        self.subject_id = id
        self.subject_initial = initial
        session = "pre" if pre_post_flag == 1 else "post"

        if self.subject_id == "" or self.subject_initial == "":
            return

        KL.start(mode=[DataMode.file, DataMode.communication, DataMode.ros], pathname=self.user_data_dir,
                 file_prefix=session+"_"+self.subject_id+"_"+self.subject_initial+"_", the_ip=self.local_ip)

        KL.log.insert(action=LogAction.data, obj='MindsetAssessmentApp', comment='start')

        with open(join(dirname(self.user_data_dir),"pid_initial.txt"), 'w') as id_f:
            id_f.write(self.subject_id+";"+self.subject_initial)
            id_f.close()

        self.sm.current = 'question_screen'

        self.question_screen.pre_post_flag = pre_post_flag # 1 for pre, 2 for post
        print ('condition', self.question_screen.pre_post_flag)
        self.question_screen.disable_buttons()
        self.question_screen.init_circles()
        self.question_screen.init_sounds()
        self.android_set_hide_menu()

        if (pre_post_flag == 1):
            Clock.schedule_once(self.question_screen.introduction1_1, 1.0)
        else:
            self.question_screen.introduction2()

    #    self.question_screen.next_question()

    # def next_question(self):
    #     self.current_question += 1
    #
    #     self.question_screen.ids['A_button'].disabled = True
    #     self.question_screen.ids['B_button'].disabled = True
    #
    #     self.question_screen.ids['A_button'].name = str(self.current_question-1) + '_A'
    #     self.question_screen.ids['B_button'].name = str(self.current_question-1) + '_B'
    #
    #     self.sm.current = 'question_screen'
    #     self.question_screen.first_phrase(self.current_question)
  #      self.question_screen.second_phrase(self.current_question)

        # Clock.schedule_once(lambda dt: self.question_screen.right_circle(), 2)
        # Clock.schedule_once(lambda dt: self.question_screen.first_phrase(self.current_question), 2)
        # Clock.schedule_once(lambda dt: self.question_screen.left_circle(), 3)
        # Clock.schedule_once(lambda dt: self.question_screen.second_phrase(self.current_question), 3)
        # Clock.schedule_once(lambda dt: self.question_screen.no_circles(), 4)
        # Clock.schedule_once(lambda dt: self.question_screen.question_phrase(), 5)
        # Clock.schedule_once(lambda dt: self.question_screen.enable_buttons(), 5)

    @run_on_ui_thread
    def android_set_hide_menu(self):
        if android_api_version.SDK_INT >= 19:
            Logger.debug('API >= 19. Set hide menu')
            view = AndroidPythonActivity.mActivity.getWindow().getDecorView()
            view.setSystemUiVisibility(
                AndroidView.SYSTEM_UI_FLAG_LAYOUT_STABLE |
                AndroidView.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION |
                AndroidView.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN |
                AndroidView.SYSTEM_UI_FLAG_HIDE_NAVIGATION |
                AndroidView.SYSTEM_UI_FLAG_FULLSCREEN |
                AndroidView.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
            )


if __name__ == '__main__':
    MindsetAssessmentApp().run()
