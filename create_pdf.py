import sys, os, json
import shutil
from datetime import date, timedelta
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import QMarginsF
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QPageLayout, QPageSize
from PyPDF2 import PdfFileMerger


root = "output/entries/"

def log(msg):
    print("+ " + msg);



def printPDF(url, margins):
    app = QtWidgets.QApplication(sys.argv)
    loader = QtWebEngineWidgets.QWebEngineView()
    loader.setZoomFactor(1)
    loader.load(url)
    
    layout = QPageLayout(
        QPageSize(QPageSize.A4),
        QPageLayout.Portrait, QMarginsF(margins[0], margins[1], margins[2], margins[3])
    )
    
    def printFinished():
        page = loader.page()
        # page.profile().clearHttpCache()
        log("%s 页面打印完成!" % page.title())
        app.exit()
    
    def printToPDF(finished):
        page = loader.page()
        page.printToPdf("./pdfs/%s.pdf" % page.title(), layout)
    
    
    loader.page().pdfPrintingFinished.connect(printFinished)
    loader.loadFinished.connect(printToPDF)
    app.exec_()


def initialization():
    if os.path.exists('pdfs'):
        shutil.rmtree('pdfs')

    os.mkdir('pdfs')


def usage(availables):
    script_name = sys.argv[0]

    examples = [
        '- python %s %s' % (script_name, x) \
        for x in availables
    ]
    
    log('可选执行列表: \n  ' + '\n  '.join(examples))


if __name__ == '__main__':
    # init
    initialization()

    log("初始化;")

    availables = [ 
        os.path.join('output', x) \
        for x in os.listdir('output/') \
        if x.endswith('.json') 
    ]

    try:
        _file = sys.argv[1]
    
        with open(_file, 'r') as f:
            entries = json.loads(f.read())
    except IndexError:
        log('Error: 请输入要打印的Journal JSON 文件.')
        usage(availables)
        exit(1)
    except FileNotFoundError:
        log('Error: 你必须要在以下参数中选取一个.')
        usage(availables)
        exit(1)

    name = _file.replace('.json', '')
    name = name.split('/')[-1]

    log("打印 %s PDF文件;" % name)

    margins = [16, 16, 16, 16]
    for entry in entries:
        url = root + entry + '.html'
        url = os.path.abspath(os.path.join(os.path.dirname(__file__), url))
        url = QtCore.QUrl.fromLocalFile(url)
        # url = QtCore.QUrl(url)
        printPDF(url, margins)

    log("+ 合并PDF文件;")

    pdfs = [ os.path.join('./pdfs', x) for x in os.listdir('./pdfs') if x.endswith(".pdf") ]

    merger = PdfFileMerger()

    for pdf in pdfs:
        merger.append(open(pdf, 'rb'))

    with open("%s.pdf" % name, "wb") as fout:
        merger.write(fout)

    log("+ 已合并! 保存到'%s.pdf'" % name)
