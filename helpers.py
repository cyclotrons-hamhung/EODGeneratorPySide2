import re
import os
import sys
import ghostscript
import locale


class Helpers():
    # method to print the inputted pdf file
    def pdf_printer(self, pdf_input_path):
        args = ['pdf_printer',
                '-dNOPAUSE',
                '-sDEVICE=mswinpr2',
                pdf_input_path]

        encoding = locale.getpreferredencoding()
        args = [a.encode(encoding) for a in args]

        ghostscript.Ghostscript(*args)
        ghostscript.cleanup()

    # method to get the absolute path to a resource
    def resource_locator(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    # method to return the day of the week given its index
    def day_of_week(self, day_index):
        week_days = ['Monday', 'Tuesday', 'Wednesday',
                     'Thursday', 'Friday', 'Saturday', 'Sunday']
        return week_days[day_index]

    # method to remove all characters that are not numerals or .
    def char_remover(self, input_string):
        try:
            return float(re.sub('[^0-9\.]', '', input_string))
        except ValueError as err:
            return 0

    # method to convert a float to a string and add a $ to the front
    def dollar_adder(self, input_float):
        if input_float == 0.0:
            return '-'
        elif input_float != None:
            value = '{:.2f}'.format(input_float)
            return '$' + value
        else:
            return ''

    def diff_dollar_adder(self, input_float):
        if input_float == 0.0:
            return '-'
        elif input_float != None:
            if input_float > 0:
                value = '{:.2f}'.format(input_float)
                return '+ $' + value
            elif input_float < 0:
                input_float -= 2 * input_float
                value = '{:.2f}'.format(input_float)
                return '- $' + value
        else:
            return ''

    def calc_diff(self, input_1, input_2):
        diff = input_1 - input_2
        return diff
