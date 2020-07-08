from reportlab.pdfgen import canvas
from pdfrw import PdfReader, PdfWriter, PageMerge
import textwrap

from helpers import Helpers as H


class Handlers():
    def __init__(self):
        super(Handlers, self).__init__()

    def generateButton_handler(self, data_dict, file_path):
        pdf = canvas.Canvas('eod_template_overlay.pdf')
        pdf.setFont('Courier', 14)

        # write general information strings
        pdf.drawString(90, 742, data_dict['store'])
        pdf.drawString(90, 713, H.day_of_week(
            self, data_dict['date'].weekday()))
        pdf.drawString(90, 685, data_dict['date'].strftime('%d/%m/%Y'))
        pdf.drawString(90, 657, data_dict['staff'])

        # array of cash values
        cash_arr = [H.char_remover(self, data_dict['cash aside']), H.char_remover(self, data_dict['cash 100s']), H.char_remover(self, data_dict['cash 50s']), H.char_remover(
            self, data_dict['cash 20s']), H.char_remover(self, data_dict['cash 10s']), H.char_remover(self, data_dict['cash 5s']), H.char_remover(self, data_dict['cash coins'])]

        # calculate total cash
        total = 0
        for value in cash_arr:
            if value != None:
                total += value

        if data_dict['cash payouts'] != None:
            total -= H.char_remover(self, data_dict['cash payouts'])

        # write cash strings
        pdf.drawString(153, 577, H.dollar_adder(
            self, H.char_remover(self, data_dict['cash payouts'])))
        pdf.drawString(153, 550, H.dollar_adder(
            self, H.char_remover(self, data_dict['cash aside'])))
        pdf.drawString(153, 523, H.dollar_adder(
            self, H.char_remover(self, data_dict['cash 100s'])))
        pdf.drawString(153, 495, H.dollar_adder(
            self, H.char_remover(self, data_dict['cash 50s'])))
        pdf.drawString(153, 467, H.dollar_adder(
            self, H.char_remover(self, data_dict['cash 20s'])))
        pdf.drawString(153, 440, H.dollar_adder(
            self, H.char_remover(self, data_dict['cash 10s'])))
        pdf.drawString(153, 413, H.dollar_adder(
            self, H.char_remover(self, data_dict['cash 5s'])))
        pdf.drawString(153, 385, H.dollar_adder(
            self, H.char_remover(self, data_dict['cash coins'])))
        pdf.drawString(153, 358, H.dollar_adder(self, total))
        pdf.drawString(153, 330, H.dollar_adder(
            self, H.char_remover(self, data_dict['cash register'])))
        pdf.drawString(153, 303, H.diff_dollar_adder(self, H.calc_diff(
            self, total, H.char_remover(self, data_dict['cash register']))))

        # write lotto strings
        lotto_actual = H.char_remover(self, data_dict['lotto actual'])
        lotto_register = H.char_remover(self, data_dict['lotto register'])

        pdf.drawString(153, 220, H.dollar_adder(self, lotto_actual))
        pdf.drawString(153, 193, H.dollar_adder(self, lotto_register))
        pdf.drawString(153, 166, H.diff_dollar_adder(
            self, H.calc_diff(self, lotto_register, lotto_actual)))

        # write eftpos strings
        eftpos_actual = H.char_remover(self, data_dict['eftpos actual'])
        eftpos_register = H.char_remover(self, data_dict['eftpos register'])

        pdf.drawString(429, 715, H.dollar_adder(self, eftpos_actual))
        pdf.drawString(429, 688, H.dollar_adder(self, eftpos_register))
        pdf.drawString(429, 661, H.diff_dollar_adder(
            self, H.calc_diff(self, eftpos_actual, eftpos_register)))

        # write epay strings
        epay_actual = H.char_remover(self, data_dict['epay actual'])
        epay_register = H.char_remover(self, data_dict['epay register'])

        pdf.drawString(429, 577, H.dollar_adder(self, epay_actual))
        pdf.drawString(429, 550, H.dollar_adder(self, epay_register))
        pdf.drawString(429, 523, H.diff_dollar_adder(
            self, H.calc_diff(self, epay_register, epay_actual)))

        # write scratchie strings
        scratchie_actual = H.char_remover(self, data_dict['scratchies actual'])
        scratchie_register = H.char_remover(
            self, data_dict['scratchies register'])

        pdf.drawString(429, 440, H.diff_dollar_adder(
            self, H.calc_diff(self, scratchie_actual, scratchie_register)))

        # write scratchie payout strings
        scratchie_pay_actual = H.char_remover(
            self, data_dict['scratchies pay actual'])
        scratchie_pay_register = H.char_remover(
            self, data_dict['scratchies pay register'])

        pdf.drawString(429, 358, H.dollar_adder(self, scratchie_pay_actual))
        pdf.drawString(429, 330, H.dollar_adder(self, scratchie_pay_register))
        pdf.drawString(429, 303, H.diff_dollar_adder(self, H.calc_diff(
            self, scratchie_pay_actual, scratchie_pay_register)))

        # write lotto payout strings
        lotto_pay_actual = H.char_remover(self, data_dict['lotto pay actual'])
        lotto_pay_register = H.char_remover(
            self, data_dict['lotto pay register'])

        pdf.drawString(429, 220, H.dollar_adder(self, lotto_pay_actual))
        pdf.drawString(429, 193, H.dollar_adder(self, lotto_pay_register))
        pdf.drawString(429, 166, H.diff_dollar_adder(
            self, H.calc_diff(self, lotto_pay_actual, lotto_pay_register)))

        # write notes section at the bottom of the page
        text = data_dict['notes']
        length = 62
        x_pos = 37
        y_pos = 135
        y_offset = 10

        if len(text) > length:
            wraps = textwrap.wrap(text, length)
            for x in range(len(wraps)):
                pdf.drawString(x_pos, y_pos, wraps[x])
                y_pos -= y_offset
            y_pos += y_offset  # add back offset after last wrapped line
        else:
            pdf.drawString(x_pos, y_pos, text)

        pdf.showPage()
        pdf.save()

        base_pdf = PdfReader('eod_template.pdf')
        watermark_pdf = PdfReader('eod_template_overlay.pdf')
        mark = watermark_pdf.pages[0]

        for page in range(len(base_pdf.pages)):
            merger = PageMerge(base_pdf.pages[page])
            merger.add(mark).render()

        print(file_path)

        writer = PdfWriter()
        writer.write(file_path, base_pdf)

    def printButton_handler(self):
        print('Button pressed!')
