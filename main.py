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

        self.intro1 = 'intro1'
        self.sound_intro1 = SoundLoader.load("./sounds/" + self.intro1 + ".wav")

        self.intro2 = 'intro2'
        self.sound_intro2 = SoundLoader.load("./sounds/" + self.intro2 + ".wav")

        self.sounds_A = []
        self.sounds_B = []
        for n in range(len(self.phrases_A)):
            self.sounds_A.append(SoundLoader.load("./sounds/" + self.phrases_A[n] + ".wav"))
            self.sounds_B.append(SoundLoader.load("./sounds/" + self.phrases_B[n] + ".wav"))

    def init_circles(self):
        self.ids['left_circle'].opacity = 0
        self.ids['right_circle'].opacity = 0

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
         anim = Animation(x=x-10, y=y-10) + Animation(x=x, y=y, duration=5, t='in_out_elastic')
         anim.start(the_circle)

    def no_circles(self):
        self.ids['right_circle'].opacity = 0
        self.ids['left_circle'].opacity = 0

    def introduction1(self):
        print "introduction1"
        self.sound_intro1.bind(on_stop=lambda d: self.introduction2())
        self.sound_intro1.play()

    def introduction2(self):
        print "introduction2"
        self.sound_intro2.bind(on_stop=lambda d: self.next_question())
        self.sound_intro2.play()

    def first_phrase(self, current_question):
        print self.phrases_A[current_question]
        self.show_right_circle()
     #   TTS.speak(self.phrases_A[current_question - 1], TTS.finished)
        self.sounds_A[current_question].bind(on_stop=lambda d: self.second_phrase(current_question))
        self.sounds_A[current_question].play()

    def second_phrase(self, current_question):
        print self.phrases_B[current_question]
        self.show_left_circle()
    #    TTS.speak(self.phrases_B[current_question - 1], TTS.finished)
        self.sounds_B[current_question].bind(on_stop=lambda d: self.question_phrase())
        self.sounds_B[current_question].play()


    def question_phrase(self):
        print self.question
        self.no_circles()
        self.sound_question.bind(on_stop=lambda d: self.enable_buttons())
        self.sound_question.play()

        #TTS.speak(self.question, TTS.finished)

    def enable_buttons(self):
        print 'buttons enabled'
        self.ids['play_again'].opacity = 1
        self.ids['A_button'].disabled = False
        self.ids['B_button'].disabled = False


    def disable_buttons(self):
        self.ids['play_again'].opacity = 0
        self.ids['A_button'].disabled = True
        self.ids['B_button'].disabled = True

    def next_question(self):
        print("next_question")
        self.current_question += 1
        self.disable_buttons()
        self.ids['A_button'].name = str(self.current_question ) + '_A'
        self.ids['B_button'].name = str(self.current_question ) + '_B'

   #     self.sm.current = 'question_screen'
        self.first_phrase(self.current_question)

    def pressed_play_again(self):
        print("press_play_again")
        self.ids['A_button'].disabled = True
        self.ids['B_button'].disabled = True
        self.ids['A_button'].name = str(self.current_question) + '_A'
        self.ids['B_button'].name = str(self.current_question) + '_B'
        #     self.sm.current = 'question_screen'
        self.first_phrase(self.current_question)


    def pressed(self, answer, the_button):
            print("pressed", answer)
            if self.current_question >= self.number_of_questions-1:
                self.end_game()
            else:
                #self.animate_flufbuf(the_button)
                self.disable_buttons()
                Clock.schedule_once(self.delay, 1)


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
        #self.the_app.stop()

class left_circle(Widget):
    pass

class MindsetAssessmentApp(App):


    def build(self):
        # initialize logger
        KL.start([DataMode.file, DataMode.communication, DataMode.ros], self.user_data_dir)
        KL.log.insert(action=LogAction.data, obj='app', comment='mindset_assessment_app')
        # KL.start([DataMode.file], "/sdcard/curiosity/")#self.user_data_dir)
        # TTS.start()
        self.sm = ScreenManager()

        self.zero_screen = ZeroScreen(name='zero_screen')
        self.sm.add_widget(self.zero_screen)

        self.question_screen = QuestionScreen(name='question_screen',the_app=self)
        self.sm.add_widget(self.question_screen)

        self.sm.current = 'zero_screen'
        return self.sm

    def start_assessment(self, pre_post_flag):
        self.sm.current = 'question_screen'
        self.question_screen.pre_post_flag = pre_post_flag # 1 for pre, 2 for post
        print ('condition', self.question_screen.pre_post_flag)
        self.question_screen.disable_buttons()
        self.question_screen.init_sounds()
        if (pre_post_flag == 1):
            self.question_screen.introduction1()
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



if __name__ == '__main__':
    MindsetAssessmentApp().run()
