from ms_active_directory import ADDomain
import logging
import os
import sys


class SelfHelp:
    def __init__(self):
        _pwmu = os.environ['PWMUSER']
        _pwmp = os.environ['PWMPASS']

        self.action = sys.stdin.readline().strip()
        self.userName = sys.stdin.readline().strip()
        self.newPassword = sys.stdin.readline().strip()
        self.oldPassword = sys.stdin.readline().strip()

        self.domain = ADDomain('atcoks.gov')
        self.session = self.domain.create_session_as_user(_pwmu, _pwmp)

        logging.basicConfig(filename='selfhelp.log', filemode='a', format='%(asctime)s - %(message)s',
                            datefmt='%d-%b-%y %H:%M:%S')

        if self.action == 'reset':
            logging.warning(f'Password rest for {self.userName}')
            self.forgot_password()
        if self.action == 'new':
            logging.warning(f'New password request for {self.userName}')
            self.set_new_password()

    def forgot_password(self):
        if self.session.find_user_by_principal_name(self.userName):
            try:
                self.session.reset_password_for_account(self.userName, self.newPassword)
                result = True
                return result
            except Exception as e:
                logging.error('Exception', exc_info=True)
                result = False
                return result
        else:
            result = False
            return result

    def set_new_password(self):
        if self.session.find_user_by_principal_name(self.userName):
            try:
                self.session.change_password_for_account(self.userName, self.newPassword, self.oldPassword)
                result = True
                return result
            except Exception as e:
                result = False
                logging.error("Exception", exc_info=True)
                return result
        else:
            result = False
            return result


if __name__ == "__main__":
    SelfHelp()




