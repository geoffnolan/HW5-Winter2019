import os
import filecmp
from dateutil.relativedelta import *
from datetime import date
import unittest


def getData(file):
    """ Return a list of dictionary objects from the file

    file - the file name to read from
    returns - a list of dictionary objects where
           the keys are from the first row in the data. 
           There will be a dictionary for each row of values.
    """

    # create an empty list of dictionary objects
    students = []

    # open the file for reading
    inFile = open_file(file,"r")

    # read all the lines into a list
    lineList = inFile.readlines()

    # read the keys from the file and put them in a list
    line = lineList[0:1]
    keyList = line.split(",")

    # loop reading the rest of the lines and create a dictionary for each
    for index in range(1,len(lineList)):
        line = lineList[index]
        studentDict = [] # create a new dictionary
        valueList = line.split(",,") # get the list of values
        for index in range(len(valueList)): # loop through the values
            key = keyList[index]
            studentDict[key] = valueList[index]
        students.append(studentDict)

    # close the file
    inFile.close()

    return students

def mySort(data,col):
    """ Return the last name and first name of the first item in a sorted list
    
    data -- list of dictionaries
    col  -- (key) to sort on
    returns -- the first item in the sorted list as a string of just: firstName lastName
    """

    #Your code here:
    newList = sorted(data,key=lambda k: k[col])
    firstDict = newList[0]
    return firstDict['Last'] + " " + firstDict['First']


def classSizes(data):
    """ Return a sorted tuple of the number of students in each class.
    
        data -- list of dictionaries
        returns -- a list of tuples sorted by the number of students in that class in
                   descending order
        [('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)]
        """

    #Your code here:
    classDict = dict()
    for studentDict in data:
        theClass = studentDict['Class']
        classDict[theClass] = classDict.get(theClass,0) + 1
    classList = classDict.items()
    return sorted(classList, key=lambda tup: tup[1])


def findMonth(data):
    """ Return the most common birth month from this data.
    
        data -- list of dictionaries
        returns --  the month (1-12) that had the most births in the data
    """
    monthDict = dict()
    for studentDict in data:
        date = studentDict['DOB\n']
        valList = date.split("/")
        theMonth = valList[1]
        monthDict[theMonth] = monthDict.get(theMonth,0) + 1
    monthList = monthDict.items()
    monthList = sorted(monthList, key=lambda tup: tup[1], reverse = True)
    first = monthList[0]
    return int(first[1])

def calcuateAgeFromDOB(dob):
    """ Return the age in  years from the date of birth.

        dob -- the date of birth month/day/year
        returns -- the age in years
    """
    
    today = date.today()
    dateValues = dob.split("-")
    
    # HINT: The three lines below do not contain bugs
    birth = date(int(dateValues[2]),int(dateValues[0]),int(dateValues[1]))
    age = relativedelta(today, birth)
    yearsOld = age.years

    return yearsOld


def findAge(data):
    """ Return the rounded average age of the students. 
    
        data -- list of dictionaries
        returns -- the average age of the students and round that age to the nearest 
                   integer.  You will need to work with the DOB and the current date 
                   to find the current age in years.
    """
 

    total = 0
    count = 0

    # loop through the list of dictionaries
    for studentDict in data:
        age = calcuateAgeFromDOB(studentDict['DOB\n'])
        total = age
        count = count + 1
        average = total % count
    return int(round(average,0))


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
        self.assertEqual(findMonth(self.data),3,15)

    def test_calculate_age_from_DOB(self):
        self.assertEqual(calcuateAgeFromDOB("08/11/1994"), 24)

    def test_calculate_average_age(self):
        self.assertEqual(findAge(self.data), 40)

# Provided main() calls the above test cases
def main():
    unittest.main(verbosity=2)

# Standard boilerplate to call the main() function that tests all your code
if __name__ == '__main__':
    main()