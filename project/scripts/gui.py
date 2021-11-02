import tkinter
import threading
import tkinter.scrolledtext
from tkinter import simpledialog
from recognizer import Recognizer
from speech_recognizer import SpeechRecognizer
from spider import WebSpider
from admin import AdminPanel
from time import sleep


class LeoindGUI:

    def __init__(self):
        # INITIALIZE Other parts
        self.recognizer = Recognizer()
        self.spider = WebSpider()
        self.speech_recognizer = SpeechRecognizer()
        self.admin_panel = AdminPanel()

        # FILEPATH
        self.password_saved_filepath = '../assets/passwords/password_saved.txt'

        # BOOLEAN FLAGS
        self.gui_done = False
        self.running = True
        self.password_saved = open(self.password_saved_filepath).readline()
        print(self.password_saved)



        if self.password_saved == 'False':
            msg = tkinter.Tk()
            msg.withdraw()

            self.login = simpledialog.askstring('Логин', 'Ваш логин(m1111111@edu.misis.ru)', parent=msg)
            self.password = simpledialog.askstring('Пароль', "Введите пароль", parent=msg)


            with open('../assets/user_status/curr_password.txt', 'w', encoding='utf-8') as users_file:
                users_file.write(f'{self.login}|{self.password}')
            with open('../assets/user_status/logged_in.txt', 'w', encoding='utf-8') as status_file:
                status_file.write('True')


        else:
            self.login, self.password = self.spider.get_user_data()

        print('[INFO] -> Получил данные пользователя')




    def gui_loop(self):
        self.win = tkinter.Tk()
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

        self.gui_done = True

        self.win.protocol('WM_DELETE_WINDOW', self.stop)

        self.write_assistant_answer('Привет! Напиши мне что-нибудь!')
        self.win.mainloop()


    def take_user_input(self):
        return self.input_area.get('1.0', 'end')

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


    def handle_user_input(self):

        user_input = self.take_user_input()
        if user_input:
            self.input_area.delete('1.0', 'end')

            self.write_user_message(user_input)

            func = self.recognizer.get_func(user_input)
            self.write_assistant_answer(func['answer'])
            sleep(2)

            if func['func'] is not None:
                eval(func['func'])






    def stop(self):
        self.running = False
        self.win.destroy()
        self.spider.exit()
        exit(0)




if __name__ == '__main__':
    Leonid = LeoindGUI()
    Leonid.gui_loop()






    