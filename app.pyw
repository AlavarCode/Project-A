from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog
from views.main import Ui_MainWindow
from views.editingWindow import Ui_Dialog
import sys

class MiApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Intances
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui2 = Ui_Dialog()

        self.peoples = list()

        # Initialization
        self.ui.list.clear()
        self.ui.frame_inferior.setFocus()
        self.ui.lblIndicator.setText("En lista: 0")

        # Buttons controls
        self.ui.btnAdd.clicked.connect(self.addPerson)
        self.ui.btnEdit.clicked.connect(lambda: self.modifyPerson(self.ui.ledSearch.text().strip(), self.ui.list.count(), self.ui.list.currentRow(), self.peoples))
        self.ui.btnDelete.clicked.connect(lambda: self.deletePerson(self.ui.list.count(), self.ui.list.currentRow(), self.peoples, self.ui.list))
        self.ui.btnClean.clicked.connect(lambda: self.cleanList(self.peoples, self.ui.list))
        self.ui.btnSearch.clicked.connect(self.runSearch)

        # signal handling
        self.ui.ledSearch.textChanged.connect(lambda: self.cancelSearch(self.ui.ledSearch.text().strip(), self.ui.list))

    def addPerson(self):
        name = self.ui.ledName.text().strip()
        age = self.ui.ledAge.text().strip()
        if name != '' and age.isnumeric():
            if int(age) <= 100:
                self.peoples.append({'Name':name.title(), 'Age':age})
                self.printList(self.peoples, self.ui.list)

                self.ui.ledName.clear()
                self.ui.ledAge.clear()
                self.ui.ledName.setFocus()

    def modifyPerson(self, nameSearch:str, rows:int, row:int, list:list):
        if row > -1:
            self.editing = QDialog()
            self.ui2.setupUi(self.editing)

            f = self.searchPerson(nameSearch, list, row)
            if len(f[0]) != rows:
                self.ui2.ledName.setText(list[row]['Name'])
                self.ui2.ledAge.setText(list[row]['Age'])
                i = row
            else:
                self.ui2.ledName.setText(f[0][row]['Name'])
                self.ui2.ledAge.setText(f[0][row]['Age'])
                i = f[1]

            self.ui2.btnSave.clicked.connect(lambda: self.saveChanges(list, i))
            self.editing.exec_()

    def saveChanges(self, list:list, index:int):
        newName = self.ui2.ledName.text().strip()
        newAge = self.ui2.ledAge.text().strip()

        if newName != '' and newAge.isnumeric():
            if int(newAge) <= 100:
                list[index]['Name'] = newName.title()
                list[index]['Age'] = newAge
                self.editing.close()
                self.printList(list, self.ui.list)

    def deletePerson(self, rows:int, row:int, list:list, object):
        print = False
        if list != []:
            f = self.searchPerson(self.ui.ledSearch.text().strip(), self.peoples, row)
            if len(f[0]) != rows:
                list.pop(row)
                print = True
            else:
                if rows > 0:
                    list.pop(f[1])
                    print = True
            if print == True:
                self.printList(list, object)

    def cleanList(self, list:list, object):
        list.clear()
        self.printList(list, object)

    def runSearch(self):
        name = self.ui.ledSearch.text().strip()
        if self.peoples != []:
            if name != '':
                f = self.searchPerson(name, self.peoples, -1)
                if len(f[0]) == 0:
                    self.ui.list.clear()
                    self.ui.lblIndicator.setText("No encontrado :(")
                else:
                    self.printList(f[0], self.ui.list)
        else:
            self.ui.lblIndicator.setText("Lista Vacía")

# ------------------------------------------------[ Secondarys ]-----------------------------------------------

    def searchPerson(self, nameSearch:str, list:list, row:int):
        found = []
        index = -1
        for i in range(0, len(list), 1):
            if nameSearch.title() in list[i]['Name']:
                found.append(list[i])
                if row+1 == len(found):
                    index = i
        return found, index

    def printList(self, list:list, object):
        object.clear()
        if list != []:
            for i in range(0, len(list)):
                object.addItem(str(i+1)+'. '+ list[i]['Name']+' '+list[i]['Age']+' años')
        self.ui.lblIndicator.setText("En lista: "+ str(len(list)))

    def cancelSearch(self, nameShearch:str, object):
        if nameShearch == '':
            self.printList(self.peoples, object)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mi_app = MiApp()
    mi_app.show()
    sys.exit(app.exec_())