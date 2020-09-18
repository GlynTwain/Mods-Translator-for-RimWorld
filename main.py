import sys
import xml.etree.ElementTree as ET
import shutil
from googletrans import Translator
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from PyQt5 import QtWidgets
from pyui import Ui_RJM

"""pyinstaller -F -w --i=icon.ico main.py"""
"""pyuic5 -x ui.ui -o pyui.py"""

app = QtWidgets.QApplication(sys.argv)
RJM = QtWidgets.QDialog()
ui = Ui_RJM()
ui.setupUi(RJM)
RJM.show()

file_path = " "
score = 0
mydicDate = {}
len_dict = 0
tag = "tag"
auto_backup = False
root = 123
first_str = ''


def selectMyfile():
    """Выбрать в ручную изначальный файл"""
    global file_path
    global mydicDate
    global len_dict
    global root
    global tree
    global first_str

    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    file_path = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    print("Ввод: " + file_path)
    tree = ET.parse(file_path)
    ui.label_name_file.setText(file_path)

    if auto_backup: backup_file() #

    root = tree.getroot()
    for child in root: mydicDate[child.tag] = child.text
    print(mydicDate)
    len_dict = len(mydicDate)
    Refresh_Date()


def Translate_Google(original_string, mysrc, mydest):
    """Перевести строку"""
    translator = Translator()
    result = translator.translate(original_string, src=mysrc, dest=mydest)
    return result.text


def next_String():
    """Перейти к следующей строке"""

    global mydicDate
    global score
    global len_dict
    global tag
    print(score)
    if score >= len_dict:
        score == 0
        Refresh_Date()

    if len_dict >= score >= 0:
        score += 1
        Refresh_Date()

    pass


def string_save():
    """Записать строку в словарь для дальнейшего сохранения"""
    global score
    global mydicDate
    value_text = mydicDate[list(mydicDate.keys())[score]]
    key = str(get_key(mydicDate, value_text))

    final_str = ui.lineEdit.text()
    translation_str = ui.lineEdit_translate.text()
    if final_str != "":
        mydicDate[key] = final_str
        print(final_str)
        print("Сохранён из финальной строки")
    elif final_str == "" and translation_str != "":
        mydicDate[key] = translation_str
        ui.lineEdit.setText(translation_str)
        print(translation_str)
        print("Сохранён из переводчика")
    else:
        print("Error:Save: Ошибка срок")


def write_file():
    """Записать в файл данные"""
    global tree
    global root
    global mydicDate
    version = "1.0"
    encoding = "utf-8"

    for key in mydicDate:
        for child in root:
            if key == child.tag:
                child.text = str(mydicDate[key])
    tree.write("Final_Text.xml", encoding=encoding)
    pass


def allTranslation():
    global mydicDate
    for key in mydicDate:
        print(key)
        if key == "__len__" or mydicDate[key] == '' or mydicDate[key] == ' ' or mydicDate[key] == None:
            continue
        else:
            mydicDate[key] = Translate_Google(mydicDate[key], 'en', 'ru')

    print("--Всё переведено через Google")
    pass


def get_key(d, value):
    """Узнать ключ по значению словаря """
    for k, v in d.items():
        if v == value:
            return k


def Refresh_Date():
    """Обновить данные"""
    global score
    global mydicDate
    value_text = mydicDate[list(mydicDate.keys())[score]]
    ui.lineEdit.setText('')
    ui.lineEdit_original.setText(value_text)
    textForLabel = "Строка №" + " " + str(score) + " / Ключ: " + str(get_key(mydicDate, value_text))
    ui.label_tag.setText(textForLabel)

    ui.lineEdit_translate.setText(Translate_Google(value_text, 'en', 'ru'))


def skip_string():
    """Вернуться к предыдущей строке"""
    global mydicDate
    global score
    global len_dict
    global tag
    print(score)

    if score >= len_dict:
        score == 0
        Refresh_Date()
    elif score >= 0:
        score -= 1
        Refresh_Date()


    elif score == -1:
        score == 1
        Refresh_Date()


def backup_file():
    new_name_file = str(file_path)
    new_name_file = new_name_file[:-4] + "_backup.xml"
    shutil.copy(file_path, new_name_file)
    auto_backup = False


ui.pushButton_openfile.clicked.connect(selectMyfile)
ui.pushButton_save.clicked.connect(string_save)
ui.pushButton_save_file.clicked.connect(write_file)
ui.pushButton_next.clicked.connect(next_String)
ui.pushButton_backup.clicked.connect(backup_file)
ui.pushButton_AllTranslate.clicked.connect(allTranslation)
ui.push_skip.clicked.connect(skip_string)
sys.exit(app.exec_())
