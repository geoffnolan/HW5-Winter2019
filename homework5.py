import os
import filecmp
from dateutil.relativedelta import *
from datetime import date
import unittest


def getData(file):
    students = []
    inFile = open(file,"r")
    linelist = inFile.readlines()
    #read the keys from the file and put them in a list
    line = linelist[0]
    strippy = line.strip("\r\n")
    keyList = strippy.split(",")
    #loop reading the rest of the lines and create a dictionary for each
    for index in range(1,len(linelist)):
        line = linelist[index]
        studentDict = dict() 
        strippy = line.strip("\r\n")
        valueList = line.split(",")
        for index in range(len(valueList)):
            key = keyList[index]
            studentDict[key] = valueList[index]
        students.append(studentDict)
    inFile.close()

    return students

def mySort(data,col):
    newList = sorted(data, key = lambda x: x[col])
    firstDict = newList[0]
    return "{} {}".format(firstDict['First'], firstDict['Last'])

def classSizes(data):
    classDict = dict()
    for studentDict in data:
        theClass = studentDict['Class']
        classDict[theClass] = classDict.get(theClass,0) + 1
    classList = classDict.items()
    return sorted(classList, key=lambda tup: tup[1], reverse = True)


def findMonth(data):
    monthDict = dict()
    for studentDict in data:
        date = studentDict['DOB']
        valList = date.split("/")
        theMonth = valList[0]
        monthDict[theMonth] = monthDict.get(theMonth,0) + 1
    monthList = monthDict.items()
    monthList = sorted(monthList, key=lambda tup: tup[1], reverse = True)
    first = monthList[0]
    return int(first[0])

def calculateAgeFromDOB(dob):
    today = date.today()
    dateValues = dob.split("/")
    birth = date(int(dateValues[2]),int(dateValues[0]),int(dateValues[1]))
    age = relativedelta(today, birth)
    yearsOld = age.years
    return yearsOld

def findAge(data):
    total = 0
    count = 0
    for studentDict in data:
        age = calculateAgeFromDOB(studentDict['DOB'])
        total += age
        count = count + 1
        average = total / count
    return int(round(average))


##############################################################################
## DO NOT MODIFY ANY CODE BELOW THIS - These are the test cases you must pass
##############################################################################

class TestHomework5(unittest.TestCase):
    def setUp(self):
        # Creates file path which will work in debugger
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        self.data = getData(os.path.join(script_dir, 'H5Data.csv'))

    def test_data_read_in_correctly(self):
        # Test that data has been read in correctly and is being stored as a list of dictionaries
        self.assertEqual(type(self.data),type([]))

    def test_mySort_first_name(self):
        #Test that mySort function works correctly sorting by First Name
        self.assertEqual(mySort(self.data,'First'),'Abbot Le')
    
    def test_mySort_last_name(self):
        #Test that mySort function works correctly sorting by Last Name
        self.assertEqual(mySort(self.data,'Last'),'Elijah Adams')

    def test_mySort_email(self):
        #Test that mySort function works correctly sorting by Email
        self.assertEqual(mySort(self.data,'Email'),'Hope Craft')

    def test_each_grade_ordered_by_size(self):
        self.assertEqual(classSizes(self.data),[('Junior', 28), ('Senior', 27), ('Freshman', 23), ('Sophomore', 22)])

    def test_most_common_birth_month(self):
        self.assertEqual(findMonth(self.data),3)

    def test_calculate_age_from_DOB(self):
        self.assertEqual(calculateAgeFromDOB("08/11/1994"), 24)

    def test_calculate_average_age(self):
        self.assertEqual(findAge(self.data), 40)

# Provided main() calls the above test cases
def main():
    unittest.main(verbosity=2)

# Standard boilerplate to call the main() function that tests all your code
if __name__ == '__main__':
    main()
