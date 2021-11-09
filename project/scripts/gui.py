import tkinter
import threading
import tkinter.scrolledtext
from tkinter import simpledialog
from recognizer import Recognizer
from speech_recognizer import SpeechRecognizer
from spider import WebSpider
from admin import AdminPanel
from authorizer import Authorizer
from time import sleep


class LeoindGUI:

    def __init__(self):
        # INITIALIZE Other parts
        self.recognizer = Recognizer()
        self.spider = WebSpider()
        self.speech_recognizer = SpeechRecognizer()
        self.admin_panel = AdminPanel()
        self.authorizer = Authorizer()

        

        # BOOLEAN FLAGS
        self.gui_done = False
        self.running = True
        self.password_saved = self.authorizer.password_saved()
        print(self.password_saved)


        # SPECIAL FUNCS (GUI exceptions) 
        self.SPECIAL_FUNCS = {
            "self.spider.open_course_lms()": "self.open_course_lms()",
            "self.exit()": "self.stop()",
        }


        # GET USER DATA
        if self.password_saved == 'False':
            msg = tkinter.Tk()
            msg.withdraw()

            self.login = simpledialog.askstring('Логин', 'Ваш логин(m1111111@edu.misis.ru)', parent=msg)
            self.password = simpledialog.askstring('Пароль', "Введите пароль", parent=msg)


            self.authorizer.write_login_password(self.login, self.password)
            self.authorizer.write_log_in()


        else:
            self.login, self.password = self.authorizer.get_user_data()

        print('[INFO] -> Получил данные пользователя')




    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.title('Леонид МИСиС')
        self.win.configure(bg='lightgray')

        self.chat_label = tkinter.Label(self.win, text='Chat', bg='lightgray')
        self.chat_label.config(font=('Arial', 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_label = tkinter.Label(self.win, text='Message', bg='lightgray')
        self.msg_label.config(font=('Arial', 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text='Send', command=self.handle_user_input)
        self.send_button.config(font=('Arial', 12))
        self.send_button.pack(padx=20, pady=5)

        self.voice_button = tkinter.Button(self.win, text='Voice', command=self.handle_voice_input)
        self.voice_button.config(font=('Arial', 12))
        self.voice_button.pack(padx=20, pady=5)

        self.gui_done = True

        self.win.protocol('WM_DELETE_WINDOW', self.stop)

        self.write_assistant_answer('Привет! Напиши мне что-нибудь!')
        self.win.mainloop()


    def handle_user_input(self):
        '''
        Key func
        Take user input and sends answer
        Exec funcntion if intent recognized
        :return: None
        '''

        user_input = self.take_user_input()
        if user_input: #if something written
            self.input_area.delete('1.0', 'end')#clear input area

            self.write_user_message(user_input)#send input to text area

            func = self.recognizer.get_func(user_input)#if command understood 
            
            self.write_assistant_answer(func['answer']) # send answer to text area
            

            if func['func'] is not None:
                
                if func['func'] in self.SPECIAL_FUNCS: #if funcs should be executed differently in cmd/gui version
                    eval(self.SPECIAL_FUNCS[func['func']])
                
                else:
                    eval(func['func'])

    def handle_voice_input(self):
        '''
        handle_keyboard_input func but voice input instead
        '''
        self.write_assistant_answer('Слушаю вашу команду! У вас три секунды')

        user_input = self.speech_recognizer.take_command()
        
        if self.speech_recognizer.is_valid(user_input):
            func = self.recognizer.get_func(user_input)#if command understood 
            
            self.write_assistant_answer(func['answer']) # send answer to text area
            

            if func['func'] is not None:
                
                if func['func'] in self.SPECIAL_FUNCS: #if funcs should be executed differently in cmd/gui version
                    eval(self.SPECIAL_FUNCS[func['func']])
                
                else:
                    eval(func['func'])

        else:
            self.write_assistant_answer('Я вас не понял:(')

    def take_user_input(self):
        return self.input_area.get('1.0', 'end').strip()

    
    def write_user_message(self, message):
        '''
        Shows the message in text area
        :param message:
        :return: None
        '''
        message = f"[{self.login}]: {message}"

        self.text_area.config(state='normal')
        self.text_area.insert('end', message + '\n')
        self.text_area.yview('end')
        self.text_area.config(state='disabled')

    
    def write_assistant_answer(self, answer):
        assistant_message = f"[Леонид]: {answer}"

        self.text_area.config(state='normal')
        self.text_area.insert('end', assistant_message + '\n')
        self.text_area.yview('end')
        self.text_area.config(state='disabled')


    
    def open_course_lms(self):
        
        def show_courses_lms():
            '''
            Prints list of courses on canvas
            :return: None
            '''
            if self.spider.driver:

                if self.spider.LMS_URL in self.spider.driver.current_url:
                    courses = self.spider.driver.find_elements_by_class_name('ic-DashboardCard')
                    for n, course in enumerate(courses):
                        self.write_assistant_answer(f'{n + 1}) {course.get_attribute("aria-label")}')
    
                else:
                    self.write_assistant_answer('Вы не на платформе LMS Canvas. Скажите "октрой канвас" или что-то похоже...')
                    self.spider.show_error_html('[ERROR] -> Вы не на платформе LMS Canvas. Скажите "октрой канвас" или что-то похоже...')

        '''
        Prints list of courses and clicks on/opens chosen
        :return: None
        '''
        if self.spider.driver:
            self.write_assistant_answer('Вот все курсы: ')

            show_courses_lms()


            msg = tkinter.Tk()
            msg.eval('tk::PlaceWindow . center')
            msg.withdraw()
            course_index = simpledialog.askinteger('Номер курса', 'Введите номер курса',parent=msg)

            courses = self.spider.driver.find_elements_by_class_name('ic-DashboardCard')

            try:
                self.write_assistant_answer(f'Отрываю курс {course_index}')
                courses[course_index - 1].click()

            except IndexError:
                self.write_assistant_answer(f'нет курса с номером {course_index}')
                self.spider.show_error_html(f'[ОШИБКА] -> нет курса с номером {course_index}')





    def stop(self):
        self.running = False
        self.win.destroy()
        self.authorizer.exit_gui()
        self.spider.exit()
        exit(0)



if __name__ == '__main__':
    Leonid = LeoindGUI()
    Leonid.gui_loop()






    