from reportlab.pdfgen import canvas
from pdfrw import PdfReader, PdfWriter, PageMerge

from helpers import Helpers

class Handlers():
    def __init__(self):
        super(Handlers, self).__init__()

    def generateButton_handler(self, data_dict):
        print(data_dict)
        pdf = canvas.Canvas('eod_template_overlay.pdf')
        pdf.setFont('Courier', 14)

        ## write general information strings
        pdf.drawString(90, 740, data_dict['store'])
        pdf.drawString(90, 711, Helpers.day_of_week(self, data_dict['date'].weekday()))
        pdf.drawString(90, 683, data_dict['date'].strftime('%d/%m/%Y'))
        pdf.drawString(90, 655, data_dict['staff'])

        ## write cash strings
        pdf.drawString(142, 542, 'String')
        pdf.drawString(142, 514, 'String')
        pdf.drawString(142, 485, 'String')
        pdf.drawString(142, 456, 'String')
        pdf.drawString(142, 429, 'String')
        pdf.drawString(142, 401, 'String')
        pdf.drawString(142, 372, 'String')
        pdf.drawString(142, 344, 'String')
        pdf.drawString(142, 315, 'String')
        pdf.drawString(142, 287, 'String')

        ## write lotto strings
        pdf.drawString(142, 202, 'String')
        pdf.drawString(142, 174, 'String')
        pdf.drawString(142, 145, 'String')

        ## write eftpos strings
        pdf.drawString(413, 713, 'String')
        pdf.drawString(413, 684, 'String')
        pdf.drawString(413, 655, 'String')

        ## write epay strings
        pdf.drawString(413, 570, 'String')
        pdf.drawString(413, 542, 'String')
        pdf.drawString(413, 514, 'String')

        ## write scratchie strings
        pdf.drawString(413, 429, 'String')

        ## write scratchie payout strings
        pdf.drawString(413, 344, 'String')
        pdf.drawString(413, 315, 'String')
        pdf.drawString(413, 287, 'String')

        ## write lotto payout strings
        pdf.drawString(413, 202, 'String')
        pdf.drawString(413, 174, 'String')
        pdf.drawString(413, 145, 'String')


        pdf.showPage()
        pdf.save()

        base_pdf = PdfReader('eod_template.pdf')
        watermark_pdf = PdfReader('eod_template_overlay.pdf')
        mark = watermark_pdf.pages[0]
    
        for page in range(len(base_pdf.pages)):
            merger = PageMerge(base_pdf.pages[page])
            merger.add(mark).render()
    
        writer = PdfWriter()
        writer.write('eod_final.pdf', base_pdf)



    def printButton_handler(self):
        print('Button pressed!')