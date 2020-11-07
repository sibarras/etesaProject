#!/usr/bin/python3
from programData import nombres_generales, nombre_SE
from datetime import date
import sqlite3

from extra_hours_handler import ExtraHours
import pandas as pd
import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqt_gui import Ui_mainWindow


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])


class ListModel(QtCore.QAbstractListModel):
    def __init__(self, data):
        super(ListModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self._data[index.row()][:]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])


class Main_UI(Ui_mainWindow):

    def BotonSumarTrabajo(self):
        try:
            equip = self.comboBoxEquipments.currentText()
            place = self.comboBoxSubstations.currentText()
            name = self.lineEditNameID.text()
            
            if equip == self.__unselected or place == self.__unselected or name =='':
                raise Exception("No se llenaron los campos requeridos...")
            inicio = self.dateTimeEditInit.text()
            fin = self.dateTimeEditEnd.text()
            date = inicio.split()[0]
            newWorks = self.__darFormatoATrabajos(place, inicio, fin, equip, name)
            self.__InsertarTrabajos(newWorks)

            self.comboBoxEquipments.setCurrentIndex(0)
            self.comboBoxSubstations.setCurrentIndex(0)
            self.lineEditNameID.setText('')

            # Solo se hace al inicio para determinar la quincena
            if len(list(works.values())[0])==1:
                m, d, y = date.split('/')
                del y
                self.__month = int(m)
                self.__half = int((1 if int(d)>=1 and int(d)<16 else 2))

        except Exception as e:
            print('[ERROR]: ', e)
    
    def BotonEliminarTrabajo(self):
        try:
            pass
        except Exception as e:
            print('[ERROR]: ', e)
    
    def __obtenerDatos(self):
        try:
            db_path='./database/colaborators.db'
            conn = sqlite3.connect(db_path)
            self.employees_df = pd.read_sql_query('SELECT * FROM colaborators', conn, index_col='index')
            conn.close()
            db_name = './database/accounts.db'
            conn = sqlite3.connect(db_name)
            self.accounts_data = pd.read_sql_query('SELECT * FROM accounts', conn, index_col='index')
            conn.close()
            del db_path, db_name, conn
        except Exception as e:
            print('[ERROR IN SQL QUERY]: ', e)

    def __darFormatoATrabajos(self, place, inicio, fin, equip, name):
        dia = int(inicio.split('/')[1])
        inicio, initCycle = inicio.split()[1:]
        h, m = inicio.split(':')
        if int(h) == 12:
            if initCycle=='AM':
                inicio = '{}:{}'.format(int(h)-12, m)
        elif initCycle=='PM':
            inicio = '{}:{}'.format(int(h)+12, m)

        fin, finCycle = fin.split()[1:]
        h, m = fin.split(':')
        if int(h) == 12:
            if finCycle=='AM':
                fin = '{}:{}'.format(int(h)-12, m)
        elif finCycle=='PM':
            fin = '{}:{}'.format(int(h)+12, m)
        for key, sub in nombre_SE.items():
            if sub == place:
                place = key
                break
        return [place, dia, inicio, fin, equip, name]     

    def __InsertarTrabajos(self, newWorks):

        for key, nw in list(zip(works.keys(), newWorks)):
            works[key].append(nw)
        # Insertar en la tabla
        data = np.transpose(list(works.values())).tolist()
        model = TableModel(data)
        self.tableViewWorks.setModel(model)
        del model

    def mostrarInfoColaborador(self):
        try:
            selected_name = self.comboBoxColaborators.currentText()
            if selected_name == self.__unselected:
                return
            self.personal_data = self.employees_df.loc[self.employees_df['nombre']==selected_name]
            model = ListModel(self.personal_data.values[0])
            self.listViewColaborator.setModel(model)
        except Exception as e:
            print('[ERROR]:', e)
    
    def BotonCrearExcel(self):
        try:
            if len(list(works.values())[0]) == 0:
                raise Exception("No se añadieron trabajos...")
            elif self.comboBoxColaborators.currentText() == self.__unselected:
                raise Exception("No se ha seleccionado un Usuario...")
            self.__wb = ExtraHours(self.__month, self.__half)
            self.__wb.write_personal_data(self.personal_data)
            self.__wb.write_time_data()
            self.__wb.write_works(works, self.accounts_data)
            self.__wb.write_non_worked_days()
            # Generar Archivo
            folder_name = self.__wb.make_folder(self.__wb.suggested_output_filename) + '\\'
            self.final_path = results_path + folder_name
            self.__wb.save_document(self.__wb.suggested_output_filename, self.final_path)
        except Exception as e:
            print('[ERROR]:', e)
    
    def BotonCrearPDF(self):
        try:
            self.__wb.excel_to_pdf(self.__wb.suggested_output_filename, self.final_path)
        except Exception as e:
            print('[ERROR]:', e)
    
    def actions_setup(self):
        # Obtener datos desde las bases de datos
        self.__obtenerDatos()

        # Push Buttons para crear excel, pdf, anadir y eliminar
        self.pushButtonExcelCreator.clicked.connect(self.BotonCrearExcel)
        self.pushButtonPDFCreator.clicked.connect(self.BotonCrearPDF)
        self.pushButtonAddWork.clicked.connect(self.BotonSumarTrabajo)
        self.pushButtonDeleteWork.clicked.connect(self.BotonEliminarTrabajo)

        # Listas para mostrar los datos del colaborador y de coordinacion
        self.comboBoxColaborators.currentIndexChanged.connect(self.mostrarInfoColaborador)

        # Selectores para Usuario, coordinacion, equipo
        self.__unselected = 'Seleccionar...'
        self.comboBoxColaborators.addItem(self.__unselected)
        self.comboBoxCoordinations.addItem(self.__unselected)
        self.comboBoxEquipments.addItem(self.__unselected)
        self.comboBoxSubstations.addItem(self.__unselected)

        self.comboBoxColaborators.addItems(self.employees_df['nombre'].values)
        self.comboBoxCoordinations.addItems(self.employees_df['depto'].drop_duplicates())
        self.comboBoxEquipments.addItems(nombres_generales.keys())
        self.comboBoxSubstations.addItems(nombre_SE.values())

        # Input Readers
        actual_time = QtCore.QDateTime.currentDateTime()
        self.dateTimeEditInit.setDateTime(actual_time)
        self.dateTimeEditEnd.setDateTime(actual_time)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    person = ''
    works = {'place':[],'day':[],'init':[],'end':[],'equip':[],'name':[]}
    results_path = 'C:\\Users\\Samuel\\Desktop\\Projects\\etesaProject\\Excel Books\\results\\'

    ui = Main_UI()
    ui.setupUi(mainWindow)
    ui.actions_setup()
    mainWindow.show()
    sys.exit(app.exec_())