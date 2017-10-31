from pyPdf import PdfFileWriter, PdfFileReader

input = PdfFileReader(file("paper/06515173.pdf","rb"))

print("title = %s" % (input.getDocumentInfo().title))

print "document1.pdf has %s pages." % input.getNumPages()