import sys,sqlite3
from sqlite3 import Error

from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtWidgets import QMainWindow,QApplication,QDialog
from calculatorwindow import *
from addCourseDialog import *
from dialogdisplaygpa import *

conn = sqlite3.connect("acudata.db")
cur = conn.cursor()

class Calc_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setCentralWidget(self.ui.tabWidget)
        self.move(300,0)
     
        self.ui.gpatable.clicked.connect(self.addcourse_upload)
        self.ui.no_of_coursesspinbox.valueChanged.connect(self.displayData)
        self.ui.calculategpabutton.clicked.connect(self.calculategpa)

        self.ui.actionDelete.triggered.connect(self.deletedata)
        self.ui.actionReload.triggered.connect(self.displayData)
        self.ui.actionNew.triggered.connect(self.new_data)
        self.ui.actionContact_Information.triggered.connect(self.about_message)

        self.ui.tableWidget.clicked.connect(self.displaydialog)
        self.ui.no_of_semesterspin.valueChanged.connect(self.displayData)
        self.ui.calc_cgpabutton.clicked.connect(self.calculate_cgpa)
    

        self.loadData()
        self.loadTable()
        self.create_cgpa_table()
        self.cgpa_display()

    def loadData(self):
        '''Creates table in database '''
        try:
            sqlStatement = '''CREATE TABLE IF NOT EXISTS gpa 
                                (Coursecode varchar UNIQUE,
                                Units INTEGER NOT NULL,
                                Grade varchar NOT NULL,
                                Point INTEGER NOT NULL
                                )'''
            cur.execute(sqlStatement)
        except Error as e:
            QtWidgets.QMessageBox.information(self.ui.tabWidget,'Error','Database Connection Error ')

    def addcourse_upload(self):
        '''Displays add course window '''
        try:
            row_number = self.ui.gpatable.currentRow() + 1
            num_of_courses = int(self.ui.no_of_coursesspinbox.text())
            if row_number > num_of_courses:
                QtWidgets.QMessageBox.information(self.ui.tabWidget,'Information','Increase the number of courses')
            else:
                self.addcourse_form = QDialog()
                self.add_object = Ui_Dialog()
                self.add_object.setupUi(self.addcourse_form)
                self.addcourse_form.show()
                table_rowno = self.ui.gpatable.currentRow()        #for checking items in table
                table_coursecode = self.ui.gpatable.item(table_rowno,0).text()
                table_unit = self.ui.gpatable.item(table_rowno,1).text() 
                table_grade = self.ui.gpatable.item(table_rowno,2).text()
                self.add_object.courseline.setText(table_coursecode)
                self.add_object.unitline.setText(table_unit)
                self.add_object.gradecombo.setCurrentText(table_grade)
                if table_coursecode.strip(" ") == "" and table_unit.strip(" ") == "":
                    self.add_object.submitbutton.clicked.connect(self.insertdata) 
                else:
                    self.add_object.submitbutton.clicked.connect(self.updatedata) 
        except AttributeError:
            table_coursecode = ""
            table_unit = ""
            table_grade = ""
            self.add_object.courseline.setText(table_coursecode)
            self.add_object.unitline.setText(table_unit)
            self.add_object.gradecombo.setCurrentText(table_grade)
            if table_coursecode.strip(" ") == "" and table_unit.strip(" ") == "":
                self.add_object.submitbutton.clicked.connect(self.insertdata) 
            else:
                self.add_object.submitbutton.clicked.connect(self.updatedata) 
        
        except Error:
            QtWidgets.QMessageBox.information(self.ui.tabWidget,'Error','Reload Table!')

    def loadTable(self):
        ''' Displays all items from database on opening '''  
        try: 
            sqlStatement = 'SELECT Coursecode,Units,Grade FROM gpa'
            cur.execute(sqlStatement)
            all_row = cur.fetchall()
            
            for row_no,result in enumerate(all_row):
                for col_no,data in enumerate(result):
                    cell = QtWidgets.QTableWidgetItem(str(data))
                    self.ui.gpatable.setItem(row_no,col_no,cell)

            row_no += 1
            self.ui.no_of_coursesspinbox.setValue(row_no)
        except UnboundLocalError:
            row_no = 1 
            self.ui.no_of_coursesspinbox.setValue(row_no)
        except Error:
            QtWidgets.QMessageBox.information(self.ui.tabWidget,'Error','Reload Table!')
       
    def displayData(self):
        '''Displays items in database '''
        try:
            if self.ui.tabWidget.currentIndex() == 0:
                self.ui.gpatable.clearContents()
                no_of_courses = int(self.ui.no_of_coursesspinbox.text())
                sqlStatement = 'SELECT Coursecode,Units,Grade FROM gpa'
                cur.execute(sqlStatement)
                row_item = cur.fetchmany(no_of_courses)
                
                for row_no,result in enumerate(row_item):
                    for col_no,data in enumerate(result):
                        cell = QtWidgets.QTableWidgetItem(str(data))
                        self.ui.gpatable.setItem(row_no,col_no,cell)
            
            elif self.ui.tabWidget.currentIndex() == 1:
                wipe_data = ""
                for row_no in range(9):
                    first_cell = QtWidgets.QTableWidgetItem(wipe_data)
                    second_cell = QtWidgets.QTableWidgetItem(wipe_data)
                    self.ui.tableWidget.setItem(row_no,0,first_cell)
                    self.ui.tableWidget.setItem(row_no,1,second_cell)

                num_of_sem = int(self.ui.no_of_semesterspin.text())             #fetchmany method returns on a row basis
                if num_of_sem % 2 != 0: 
                    num_of_semester = (num_of_sem // 2) + 1
                else :
                    num_of_semester = (num_of_sem // 2)

                loadStatement = '''SELECT GpaFirst,GpaSecond from first ORDER BY Level '''
                self.cur_cgpa.execute(loadStatement)
                gpa_item = self.cur_cgpa.fetchmany(num_of_semester)

                total_item = 0
                for row,data in enumerate(gpa_item):
                    for col,result in enumerate(data):
                        if result == None:
                            result = ""
                        cell = QtWidgets.QTableWidgetItem(str(result))
                        self.ui.tableWidget.setItem(row,col,cell)
                        total_item += 1
                        if total_item == num_of_sem:
                            break
        except Error:
            QtWidgets.QMessageBox.information(self.ui.tabWidget,'Error','Reload Table!')
             
    def insertdata(self):
        '''Inserts data into database '''
        try:
            coursecode = (self.add_object.courseline.text()).upper()
            unit = int(self.add_object.unitline.text())
            grade = self.add_object.gradecombo.currentText()
            if grade == 'A':
                points = 5
            elif grade == 'B':
                points = 4
        
            elif grade == 'C':
                points = 3
                
            elif grade == 'D':  
                points = 2
                
            elif grade == 'F':
                points = 0
            
            if unit <0 or unit >30:
                    QtWidgets.QMessageBox.information(self.addcourse_form,'Information',
                    'Unit cannot be less than 0 or greater than 30')

            
            if coursecode.strip(" ") != "" and unit >= 0 and unit <= 30:
                sqlStatement = "INSERT INTO gpa VALUES('" + coursecode +"','" +str(unit) +"','" + grade + "','" + str(points) +"')"
                cur.execute(sqlStatement)
                conn.commit()
                self.addcourse_form.close()
                self.displayData()
        except ValueError:
            QtWidgets.QMessageBox.information(self.addcourse_form,'Error','Fill in the Fields')
        except sqlite3.IntegrityError:
            QtWidgets.QMessageBox.information(self.addcourse_form,'Error','Course is already added')
        except Error as e:
            QtWidgets.QMessageBox.information(self.addcourse_form,'Error','Reload Table!')
            
    def updatedata(self):
        '''Updates data in database '''
        try:
            coursecode = (self.add_object.courseline.text()).upper()
            unit = int(self.add_object.unitline.text())
            grade = self.add_object.gradecombo.currentText()
            table_rowno = self.ui.gpatable.currentRow()
            table_coursecode = self.ui.gpatable.item(table_rowno,0).text()
          
            if grade == 'A':
                points = 5
            elif grade == 'B':
                points = 4
        
            elif grade == 'C':
                points = 3
                
            elif grade == 'D':
                points = 2
                
            elif grade == 'F':
                points = 0
            
            if unit <0 or unit >30:
                    QtWidgets.QMessageBox.information(self.addcourse_form,'Information',
                    'Unit cannot be less than 0 or greater than 30')

            if coursecode.strip(" ") != "" and unit >= 0 and unit <= 30:
                    sqlStatement = "UPDATE gpa SET coursecode='" + coursecode + "',Units='" + str(unit) +"',Grade='"+ grade +"',Point='"+ str(points) +"' WHERE coursecode='" + table_coursecode +"'" 
                    cur.execute(sqlStatement)
                    conn.commit()
                    self.addcourse_form.close()
                    self.displayData()
        except ValueError:
            QtWidgets.QMessageBox.information(self.addcourse_form,'Error','Fill in the Fields correctly!')
        except sqlite3.IntegrityError:
            QtWidgets.QMessageBox.information(self.addcourse_form,'Error','Course is already added!')
        except:
            QtWidgets.QMessageBox.information(self.addcourse_form,'Error','Reload Table!')

    def deletedata(self):
        '''Deletes data from database '''
        try:
            if self.ui.tabWidget.currentIndex() == 0:
                table_rowno = self.ui.gpatable.currentRow()
                table_coursecode = self.ui.gpatable.item(table_rowno,0).text()
                sqlStatement = "DELETE FROM gpa WHERE coursecode='" + table_coursecode +"'"
                cur.execute(sqlStatement)
                conn.commit()
                self.displayData()
            elif self.ui.tabWidget.currentIndex() == 1:
                table_rowno = int(self.ui.tableWidget.currentRow()) + 1
                table_colno = int(self.ui.tableWidget.currentColumn())
                if table_rowno == 1:
                    level = 100
                elif table_rowno == 2:
                    level = 200
                elif table_rowno == 3:
                    level = 300
                elif table_rowno == 4:
                    level = 400
                elif table_rowno == 5:
                    level = 500
                elif table_rowno == 6:
                    level = 600
                elif table_rowno == 7:
                    level = 700
                elif table_rowno == 8:
                    level = 800

                if table_colno == 0:
                    Gpavalue = "GpaFirst"
                elif table_colno == 1:
                    Gpavalue = "GpaSecond"
                
                deleteStatement = "UPDATE first set '" + Gpavalue + "'= NULL WHERE Level='" + str(level) +"'"
                self.cur_cgpa.execute(deleteStatement)
                self.conn_cgpa.commit()
                self.displayData()
            
        except ValueError:
            self.delete_message()
        except AttributeError:
            self.delete_message()

    def delete_message(self):
        QtWidgets.QMessageBox.information(self.ui.tabWidget,"Error","Please select an item to be deleted")

    def new_data(self):
        try:
            if self.ui.tabWidget.currentIndex() == 0:
                title = 'New File'
                message = 'Do you want to create a new table?'
                message_result = QtWidgets.QMessageBox.question(self.ui.tabWidget,title,
                message,QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No,QtWidgets.QMessageBox.No)

                if message_result == QtWidgets.QMessageBox.No:
                    pass
                elif message_result == QtWidgets.QMessageBox.Yes:
                    sqlStatement = '''DROP TABLE IF EXISTS gpa'''
                    cur.execute(sqlStatement)
                    self.loadData()
                    self.displayData()
            elif self.ui.tabWidget.currentIndex() == 1:
                title = 'New File'
                message = 'Do you want to create a new table?'
                message_result = QtWidgets.QMessageBox.question(self.ui.tabWidget,title,
                message,QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No,QtWidgets.QMessageBox.No)

                if message_result == QtWidgets.QMessageBox.No:
                    pass
                elif message_result == QtWidgets.QMessageBox.Yes:
                    no_of_item = int(self.ui.no_of_semesterspin.text())
                    no_of_item += 1
                    deleteStatement = '''DROP TABLE IF EXISTS first'''
                    self.cur_cgpa.execute(deleteStatement)
                    self.create_cgpa_table()
                    wipe_data = ""
                    for row_no in range(no_of_item):
                        first_cell = QtWidgets.QTableWidgetItem(wipe_data)
                        second_cell = QtWidgets.QTableWidgetItem(wipe_data)
                        self.ui.tableWidget.setItem(row_no,0,first_cell)
                        self.ui.tableWidget.setItem(row_no,1,second_cell)

                    self.ui.no_of_semesterspin.setValue(1)
                
        except:
            QtWidgets.QMessageBox.information(self.ui.tabWidget,"Error","Error in creating new table!")

    def about_message(self):
        '''Displays the about us message '''
        title = 'About Us'
        message = "Created:2020\nFunction:GPA Calculator\nDeveloper:Pelumi Oguntola\nEmail:oguntolapelumi6@gmail.com"
        QtWidgets.QMessageBox.about(self.ui.tabWidget,title,message)
 
    def calculategpa(self):
        try:
            sqlStatement = 'SELECT Units, Point FROM gpa'
            cur.execute(sqlStatement)
            no_of_courses = int(self.ui.no_of_coursesspinbox.text())
            result = cur.fetchmany(no_of_courses)
            total_unit = 0
            calc_result = 0
            for col_no,unit in enumerate(result):
                unit_rep = unit[0]
                total_unit += unit_rep
            
            for row_no,unit_point in enumerate(result):
                unit_for_calc = unit_point[0]
                point_for_calc = unit_point[1]
                calculator = unit_for_calc * point_for_calc
                calc_result += calculator
            
            result_gpa = calc_result / total_unit
            gpa_result = round(result_gpa,2)
            self.dialoggpa = QDialog()
            self.displaygpa = Gpa_Dialog()
            self.displaygpa.setupUi(self.dialoggpa)
            self.displaygpa.label_gpa.setText(str(gpa_result))
            self.displaygpa.label_gpa.setStyleSheet("color: rgb(255, 255, 255);")
            
            if gpa_result >= 4.5 and gpa_result <= 5.0:
                self.displaygpa.frame_gpa.setStyleSheet("background-color: rgb(0, 170, 0);\n""border-radius:75px;")
            elif gpa_result >= 3.5 and gpa_result <= 4.49:
                self.displaygpa.frame_gpa.setStyleSheet("background-color: rgb(0, 0, 127);\n""border-radius:75px;")
            elif gpa_result >= 2.4 and gpa_result <= 3.49:
                self.displaygpa.frame_gpa.setStyleSheet("background-color: rgb(85, 0, 127);\n""border-radius:75px;")
            elif gpa_result >= 1.5 and gpa_result <= 2.39:
                self.displaygpa.frame_gpa.setStyleSheet("background-color: rgb(255, 85, 0);\n""border-radius:75px;")
            elif gpa_result >= 0 and gpa_result <= 1.49:
                self.displaygpa.frame_gpa.setStyleSheet("background-color: rgb(255, 0, 0);\n""border-radius:75px;")

            self.dialoggpa.show()
            

        except:
            QtWidgets.QMessageBox.information(self.ui.tabWidget,'Error','Add Courses to the table')

    def create_cgpa_table(self):
        '''Creates table in the database '''
        try:
            self.conn_cgpa = sqlite3.connect("cgpa_data.db")
            self.cur_cgpa = self.conn_cgpa.cursor()
            sqlStatement ='''CREATE TABLE IF NOT EXISTS first 
                                            (
                                                GpaFirst DOUBLE,
                                                GpaSecond DOUBLE,
                                                Level INTEGER UNIQUE 
                                            ) '''
            self.cur_cgpa.execute(sqlStatement)
        except Error as e:
            QtWidgets.QMessageBox.information(self.ui.tabWidget,'Error','Database Connection Error')

    def insert_cgpa(self):
        '''Inserts or updates into database from table'''
        #use the current item changed method
        try:
            col_num = self.ui.tableWidget.currentColumn()
            row_num = self.ui.tableWidget.currentRow()
            table_gpa = self.ui.tableWidget.item(row_num,col_num).text()
            if table_gpa.strip(" ") == "":
                gpa, self.ok = QtWidgets.QInputDialog.getDouble(self.ui.tabWidget,"GPA","Enter your Gpa",0,0,5.0,2)
            else:    
                value = float(table_gpa)
                gpa, self.ok = QtWidgets.QInputDialog.getDouble(self.ui.tabWidget,"GPA","Enter your Gpa",value,0,5.0,2)
            
            row_no = self.ui.tableWidget.currentRow() + 1
            if row_no == 1:
                level = 100
            elif row_no == 2:
                level = 200
            elif row_no == 3:
                level = 300
            elif row_no == 4:
                level = 400
            elif row_no == 5:
                level = 500
            elif row_no == 6:
                level = 600
            elif row_no == 7:
                level = 700
            elif row_no == 8:
                level = 800


            
            if self.ok:
                searchStatement = "SELECT Level FROM first WHERE Level=" + str(level)
                self.cur_cgpa.execute(searchStatement)
                level_confirm = self.cur_cgpa.fetchone()
                if col_num == 0:
                    if level_confirm == None:
                        sqlStatement = "INSERT INTO first(GpaFirst,Level) VALUES('" + str(gpa) + "','" + str(level) +"')"
                        self.cur_cgpa.execute(sqlStatement)
                        self.conn_cgpa.commit()
                        self.displayData()
                       
                    else:
                        updateStatement = "UPDATE first SET GpaFirst='" + str(gpa) + "' WHERE Level='" + str(level) +"'"
                        self.cur_cgpa.execute(updateStatement)
                        self.conn_cgpa.commit()
                        self.displayData()
                       
                        
                elif col_num == 1:
                    if level_confirm == None:
                        sqlStatement = "INSERT INTO first(GpaSecond,Level) VALUES('" + str(gpa) + "','" + str(level) +"')"
                        self.cur_cgpa.execute(sqlStatement)
                        self.conn_cgpa.commit()
                        self.displayData()
                        
                    else:
                        updateStatement = "UPDATE first SET GpaSecond='" + str(gpa) + "' WHERE Level='" + str(level) +"'"
                        self.cur_cgpa.execute(updateStatement)
                        self.conn_cgpa.commit()
                        self.displayData()
                        
                        
                
            
        except ArithmeticError:
            pass
        except UnboundLocalError:
            pass
        except:
            QtWidgets.QMessageBox.information(self.ui.tabWidget,"Error","Reload Table!")

    def displaydialog(self):
        ''' Displays the double spinbox '''
        try:
            col_num = self.ui.tableWidget.currentColumn()
            row_num = self.ui.tableWidget.currentRow()
            table_num = row_num + 1
            num_of_sem = int(self.ui.no_of_semesterspin.text())
            
            if num_of_sem % 2 != 0: 
                num_of_semester = (num_of_sem // 2) + 1
            else :
                num_of_semester = (num_of_sem // 2)

            if table_num > num_of_semester:
                QtWidgets.QMessageBox.information(self.ui.tabWidget,'Information','Increase the number of semesters')
            else:
                if num_of_sem % 2 != 0:
                    rownum_sem = num_of_semester - 1
                    if self.ui.tableWidget.currentColumn() == 1 and self.ui.tableWidget.currentRow() == rownum_sem:
                        QtWidgets.QMessageBox.information(self.ui.tabWidget,'Information','Increase the number of semesters')
                    else:
                        table_gpa = self.ui.tableWidget.item(row_num,col_num).text()
                        if table_gpa.strip(" ") == "":
                            self.insert_cgpa()
                        else:
                            self.insert_cgpa()
                else:
                    table_gpa = self.ui.tableWidget.item(row_num,col_num).text()
                    if table_gpa.strip(" ") == "":
                        self.insert_cgpa()
                    else:
                        self.insert_cgpa()
        except AttributeError:
            QtWidgets.QMessageBox.information(self.ui.tabWidget,'Error','Enter a number!')
        except:
            QtWidgets.QMessageBox.information(self.ui.tabWidget,'Error','Enter a number!')

    def cgpa_display(self):
        '''displays items in the database at launch'''
        try:

            sqlStatement = '''SELECT GpaFirst,GpaSecond from first ORDER BY Level '''
            self.cur_cgpa.execute(sqlStatement)
            gpa_item = self.cur_cgpa.fetchall()

            total_item = 0
            for row,data in enumerate(gpa_item):
                for col,result in enumerate(data):
                    if result == None:
                        result = ""
                    cell = QtWidgets.QTableWidgetItem(str(result))
                    self.ui.tableWidget.setItem(row,col,cell)

                    total_item += 1

            self.ui.no_of_semesterspin.setValue(total_item)
                
        
        except :
            QtWidgets.QMessageBox.information(self.ui.tabWidget,"Error","Reload Table!")
    
    def calculate_cgpa(self):
        try:

            num_of_sem = int(self.ui.no_of_semesterspin.text())             #fetchmany method returns on a row basis
            if num_of_sem % 2 != 0: 
                num_of_semester = (num_of_sem // 2) + 1
            else :
                num_of_semester = (num_of_sem // 2)

            if num_of_semester == 1:
                level = 100
            elif num_of_semester == 2:
                level = 200
            elif num_of_semester == 3:
                level = 300
            elif num_of_semester == 4:
                level = 400
            elif num_of_semester == 5:
                level = 500
            elif num_of_semester == 6:
                level = 600
            elif num_of_semester == 7:
                level = 700
            elif num_of_semester == 8:
                level = 800


            tableStatement = "SELECT Level from first"
            self.cur_cgpa.execute(tableStatement)
            table_no = self.cur_cgpa.fetchall()
            
            all_level = []
            for row_num,tup_levels in enumerate(table_no):
                for col_num,levels in enumerate(tup_levels):
                    all_level.append(levels)
                    
            if level not in all_level:
                QtWidgets.QMessageBox.information(self.ui.tabWidget,"Error","Fill the empty columns!")
        
            searchStatement = "SELECT GpaFirst,GpaSecond from first ORDER BY Level"
            self.cur_cgpa.execute(searchStatement)
            gpa_score = self.cur_cgpa.fetchmany(num_of_semester)

            total_item = 0
            total_gpa = 0
            total_none = 0
            for row,data in enumerate(gpa_score):
                for col,result in enumerate(data):
                    if result == None:
                        total_none += 1
                        if total_none == 1:
                            QtWidgets.QMessageBox.information(self.ui.tabWidget,"Error","Fill the empty columns!")
                            
                    else:
                        total_gpa += result
                        total_item += 1
                        if total_item == num_of_sem:
            
                            cum_cgpa = total_gpa / num_of_sem

                            cgpa_result = round(cum_cgpa,2)
                            self.dialoggpa = QDialog()
                            self.displaygpa = Gpa_Dialog()
                            self.displaygpa.setupUi(self.dialoggpa)
                            self.displaygpa.label_gpa.setText(str(cgpa_result))
                            self.displaygpa.label_gpa.setStyleSheet("color: rgb(255, 255, 255);")
                            
                            if cgpa_result >= 4.5 and cgpa_result <= 5.0:
                                self.displaygpa.frame_gpa.setStyleSheet("background-color: rgb(0, 170, 0);\n""border-radius:75px;")
                            elif cgpa_result >= 3.5 and cgpa_result <= 4.49:
                                self.displaygpa.frame_gpa.setStyleSheet("background-color: rgb(0, 0, 127);\n""border-radius:75px;")
                            elif cgpa_result >= 2.4 and cgpa_result <= 3.49:
                                self.displaygpa.frame_gpa.setStyleSheet("background-color: rgb(85, 0, 127);\n""border-radius:75px;")
                            elif cgpa_result >= 1.5 and cgpa_result <= 2.39:
                                self.displaygpa.frame_gpa.setStyleSheet("background-color: rgb(255, 85, 0);\n""border-radius:75px;")
                            elif cgpa_result >= 0 and cgpa_result <= 1.49:
                                self.displaygpa.frame_gpa.setStyleSheet("background-color: rgb(255, 0, 0);\n""border-radius:75px;")

                            self.dialoggpa.show()
                            break
            

        except TypeError:
            QtWidgets.QMessageBox.information(self.ui.tabWidget,'Error','Fill the table!')
        except Error as e:
            QtWidgets.QMessageBox.information(self.ui.tabWidget,'Error','Reload Table!')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    windows = Calc_Window()
    windows.show()
    sys.exit(app.exec_())