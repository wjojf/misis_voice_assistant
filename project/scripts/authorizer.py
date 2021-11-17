import tkinter
from tkinter import simpledialog

class Authorizer:

    def __init__(self):
        self.WD = '../assets/passwords'
        self.PASSWORD_FILEPATH = self.WD + '/curr_password.txt'
        self.LOGGED_IN_FILEPATH = self.WD + '/logged_in.txt'
        self.PASSWORD_SAVED_FILEPATH = self.WD + '/password_saved.txt'

    def get_user_data(self):

        '''
        Get user data from .txt file
        :return: [login, password]
        '''
        #print(f'[DEBUG] -> {open(self.PASSWORD_FILEPATH).readline()}')
        try:
            with open(self.PASSWORD_FILEPATH) as file:
                return file.readline().split('|')
        except:
            print(open(self.PASSWORD_FILEPATH).readline())
            return 'Error!'

    def password_saved(self):
        return open(self.LOGGED_IN_FILEPATH).readline()

    def write_log_in(self):
        with open(self.LOGGED_IN_FILEPATH, 'w') as f:
            f.write('True')

    def write_login_password(self, login, password):
        with open(self.PASSWORD_FILEPATH, 'w') as f:
            f.write(f'{login}|{password}')


    def ask_save_password(self):
        '''
        Change status for saving password after exit
        :return: None
        '''


        user_answer = input('[INPUT] -> Save password?(y/n): ')

        #print(Fore.RED + f'[DEBUG] -> {user_answer}')

        if user_answer.lower() in ['yes', 'y']:
            return True

        elif user_answer.lower() in ['no', 'n']:
            return False

        else:
            self._print('[ОШИБКА] -> Команда не распознана')
            self.ask_save_password()


    def exit(self):

        save_password = self.ask_save_password()

        if not save_password:

            with open(self.LOGGED_IN_FILEPATH, 'w') as logged_in_file:
                logged_in_file.write('False')

            with open(self.PASSWORD_FILEPATH, 'w') as password_file:
                password_file.write('')

            with open(self.PASSWORD_SAVED_FILEPATH, 'w') as f:
                f.write('False')

        else:
            with open(self.PASSWORD_SAVED_FILEPATH, 'w') as f:
                f.write('True')

    # GUI FUNCS
    def ask_save_password_gui(self):
        msg = tkinter.Tk()
        msg.eval('tk::PlaceWindow . center')
        msg.withdraw()

        save_password = False # default value
        save_password = simpledialog.askstring('Сохранить пароль?', "Сохранить пароль(y/n)?", parent=msg)

        if save_password.lower() in ['y', 'yes']:
            return True

        elif save_password.lower() in ['n', 'no']:
            return False

        else:
            return False





    def exit_gui(self):

        save_password = self.ask_save_password_gui()

        if save_password:
            with open(self.PASSWORD_SAVED_FILEPATH, 'w') as f:
                f.write('True')

        else:
            #print('Rewriting data')
            with open(self.LOGGED_IN_FILEPATH, 'w') as logged_in_file:
                logged_in_file.write('False')

            with open(self.PASSWORD_FILEPATH, 'w') as password_file:
                password_file.write('')

            with open(self.PASSWORD_SAVED_FILEPATH, 'w') as f:
                f.write('False')

