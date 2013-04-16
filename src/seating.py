'''
Created on Feb 15, 2013

@author: wilkibr
'''
import random

class Table(object):
    '''
    classdocs
    '''


    def __init__(self, staff, seats):
        '''
        Constructor
        '''
        self.numSeats = int(seats)
        self.staff = staff
        self.seating = []
        
    def getRemainingSeats(self):
        '''
        Returns the number of empty seats so far at a table
        '''
        return self.numSeats - len(self.seating)
    
    def numDomesticStudents(self):
        count = 0;
        for person in self.seating:
            if person.getCountry() == 'd':
                count += 1
        return count
    
    def isFilled(self):
        return (self.numSeats - len(self.seating)) == 0
    
    def getTotalSeats(self):
        return self.numSeats
    
    def getTableSeating(self):
        return self.seating
    
    def addStudent(self, student):
        self.seating.append(student)
        
    def removeStudent(self, student):
        self.seating.remove(student)
        
    def getStaffMember(self):
        return self.staff
    
    def clearStudents(self):
        self.seating = []
        
    def __str__(self):
        return self.staff + "'s table has " + str(self.numSeats) + " seats."
        
        
class Student(object):
    '''
    Class that defines as a student.  Usually the information will be pulled from
    a CSV file that must include the students name and whether the student is
    (i)nternational or (d)omestic.
    '''
    
    def __init__(self, name, country):
        '''
        Constructor
        '''
        self.name = name
        self.country = country
        self.tablesSatAt = []
        
    def addTable(self, tableNumber):
        '''
        when a student is assigned to sit at a table, that number is 
        added to this list
        '''
        self.tablesSatAt.append(tableNumber)
        
    def removeTable(self, tableNumber):
        '''
        deletes the last table the student sat at
        '''
        del self.tablesSatAt[-1]
        
    def getTablesSatAt(self):
        '''
        returns the entire list of tables where the student sat
        in a given time period
        '''
        return self.tablesSatAt
    
    def getName(self):
        '''
        returns the name of the student
        '''
        return self.name
    
    def getCountry(self):
        return self.country
    
    def lastTableSatAt(self):
        '''
        returns the last table the student sat at
        '''
        return self.tablesSatAt[-1]
        
    def __str__(self):
        return self.name + " is a " + self.country + " student."
        
if __name__ == '__main__':
    
    # defines the number of table seatings desired
    NUM_WEEKS = 10
    
    def addStudent(student, tableList, tableNumber):
        '''
        Takes a student object, the list of tables and the number of the table.
        Add the student to the particular table, then adds that table number to 
        the list of tables the student has sat at.
        '''
        tableList[tableNumber].addStudent(student)
        student.addTable(tableNumber)
        
    def removeStudent(student, tableList, tableNumber):
        '''
        while recursing, if a student has to be removed after they are already seated,
        they need to be removed from the current tables seating as well as have the 
        table number removed from the list of tables where they have sat
        '''
        tableList[tableNumber].removeStudent(student)
        student.removeTable(tableNumber)
        
    def createTables(studentList, tables, startingNumber):
        '''
        selects a student randomly from the list of students.  If there is room at the table
        add the student to that table and remove them from the list of available students.
        Otherwise go to the next table to see if there is room:
        '''
        tableNumber = startingNumber
        while len(studentList) > 0:
            nextStudent = random.choice(studentList)
            if tables[tableNumber].getRemainingSeats() > 0:
                addStudent(nextStudent, tables, tableNumber)
                studentList.remove(nextStudent)
            startingNumber += 1
            tableNumber = startingNumber % len(tables)
    
    def seatRecursive(studentList, tables):
        '''
        Recursively places the students at each table using backtracking.  The function 
        first checks to make sure there is a) space at the current table and b) they have not sit
        at the same table twice.
        '''
        if len(studentList) == 0: # base case
            return True
        
        nextStudent = random.choice(studentList)
        for x in range(len(tables)):
            if (tables[x].getRemainingSeats() > 0 and x not in nextStudent.getTablesSatAt()):
                addStudent(nextStudent, tables, x)
                studentList.remove(nextStudent)
                if seatRecursive(studentList, tables):
                    return True
                else:
                    removeStudent(nextStudent, tables, x)
                    studentList.append(nextStudent)
        return False
                  
    #set up tables
    tables = []
    weeksOfTables = []
    tableFile = open('staff_seats.txt', 'r')
    for line in tableFile:
        newTable = line.split(',')
        staffMember = newTable[0]
        numberOfSeats = newTable[1][:-1] # remove the newline character
        tables.append(Table(staffMember, numberOfSeats))
    tableFile.close()
        
    #set up students
    students = []
    internationalStudents = []
    studentFile = open('students.txt', 'r')
    for studentLine in studentFile:
        newStudent = studentLine.split(',')
        studentName = newStudent[0]
        studentCountry = newStudent[1][:-1]
        students.append(Student(studentName, studentCountry))
    studentFile.close()
    

    tempTableList = list(tables)

    outfile = open('seating.doc', 'a')

    for x in range(NUM_WEEKS):
        # clear the current students in the list to start with a blank slate
        for table in tempTableList:
            table.clearStudents()
    
        # create temp lists so the original lists are not modified
        tempTableList = list(tables)
        tempStudentList = list(students)
        seatRecursive(tempStudentList, tempTableList) # The actual recursive call
        
        # Once the table list is created, write it out to a file
        for table in tempTableList:
            outfile.write(table.getStaffMember() + "'s table:\n")
            for student in table.getTableSeating():
                outfile.write(student.getName() + ', ')
            outfile.write('\n' + '\n')
        outfile.write('\f')
    outfile.close()
    print("Done") # If this prints, all has gone well
   
        
        
        

        
        