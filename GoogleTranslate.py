import sys
import requests
import execjs
import json
import PyQt5.sip
from PyQt5.QtCore import Qt,QThread,pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,QPlainTextEdit


class gtranslate(QWidget):
    def __init__(self,text=None):
        super().__init__()
        self.setWindowTitle('谷歌翻译')
        # self.setFixedSize(280, 150)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint |   # 使能最小化按钮
                            Qt.WindowCloseButtonHint |      # 使能关闭按钮
                            Qt.WindowStaysOnTopHint)
        self.initUI()
        self.url = 'https://translate.google.cn/translate_a/single'
        self.ctx = execjs.compile("""
            function TL(a) {
                var k = "";
                var b = 406644;
                var b1 = 3293161072;
                var jd = ".";
                var $b = "+-a^+6";
                var Zb = "+-3^+b+-f";
                for (var e = [], f = 0, g = 0; g < a.length; g++) {
                    var m = a.charCodeAt(g);
                    128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
                    e[f++] = m >> 18 | 240,
                    e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
                    e[f++] = m >> 6 & 63 | 128),
                    e[f++] = m & 63 | 128)
                }
                a = b;
                for (f = 0; f < e.length; f++) a += e[f],
                a = RL(a, $b);
                a = RL(a, Zb);
                a ^= b1 || 0;
                0 > a && (a = (a & 2147483647) + 2147483648);
                a %= 1E6;
                return a.toString() + jd + (a ^ b)
            };
            function RL(a, b) {
                var t = "a";
                var Yb = "+";
                for (var c = 0; c < b.length - 2; c += 3) {
                    var d = b.charAt(c + 2),
                    d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
                    d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
                    a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
                }
                return a
            }
        """)
        self.my_thread = translate_thread()
        self.my_thread.my_signal.connect(self.translate)

    def get_tk(self, text):
        return self.ctx.call("TL",text)

    def eng2chn(self,text):
        payload = {
        'client': 'webapp',
        'sl': 'en',
        'tl': 'zh-CN',
        'hl': 'zh-CN',
        'dt': ['at','at','bd','ex','ld','md','qca','rw','rm','ss','t'],
        'otf': '1',
        'ssel': '3',
        'tsel': '6',
        'kc': '1',
        'tk': self.get_tk(text),
        'q': text
        }

        result = self.gethtml(payload).json()
        try:
            wordlist = ''
            for i in range(len(result[1])):
                word = ''
                for res in result[1][i][1]:
                    word +=res+','
                word = word[:-1]
                wordlist += str(result[1][i][0])+'\n'+word+'\n'
            return wordlist
        except:
            sentences = ''
            for res in result[0]:
                sentences += str(res[0])
            # print(sentences)
            return sentences[:-4]

    def gethtml(self,payload):
        res = requests.get(self.url,params=payload)
        return res


    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout1 = QHBoxLayout()
        self.layout2 = QHBoxLayout()

        self.lab = QLabel("谷歌翻译   英文--->中文", self)
        self.layout.addWidget(self.lab)
        self.inputword = QPlainTextEdit()
        self.outputword = QPlainTextEdit()
        self.translatebtn = QPushButton("翻译", self)
        self.translatebtn.clicked.connect(self.translate)
        self.clearbtn = QPushButton("清除", self)
        self.clearbtn.clicked.connect(self.clear)
        self.layout.addLayout(self.layout1)
        self.layout.addLayout(self.layout2)
        self.layout1.addWidget(self.inputword)
        self.layout1.addWidget(self.outputword)

        self.layout2.addWidget(self.translatebtn)
        self.layout2.addWidget(self.clearbtn)
        self.setLayout(self.layout)


    def translate(self,num):
        try:
            text = self.inputword.toPlainText().strip().replace('\n',' ')
            result = self.eng2chn(text)
            self.outputword.setPlainText(result)
        except:
            pass
    def clear(self):
        self.inputword.setPlainText('')
        self.outputword.setPlainText('')


class translate_thread(QThread):
    #定义一个信号，传递一个list
    my_signal = pyqtSignal(list)
    def __init__(self):
        super().__init__()
    def run(self):
        try:
            self.my_signal.emit('translate')
        except:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = gtranslate()
    ex.show()
    sys.exit(app.exec_())
