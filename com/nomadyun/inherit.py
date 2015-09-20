# -*- coding: utf-8 -*-
'''
Created on 2014.10.3

@author: nomadyun
'''


class SchoolMember:
    '''Reprents any school member.'''
    def __init__(self,name,age):
        self.name = name
        self.age = age
        print '(Initialized SchoolMember:%s)' %self.name
        
    def tell(self):
        '''Tell my details.'''
        print 'Name:"%s" Age:"%s"' %(self.name,self.age),
class Teacher(SchoolMember):
    '''Reprents a teacher.'''
    def __init__(self,name,age,salary):
        SchoolMember.__init__(self, name, age)
        self.salary = salary
        print '(Initialized Teacher:%s)' %self.name
        
    def tell(self):
        SchoolMember.tell(self)
        print 'Salary:"%d"' %self.salary
        
class Student(SchoolMember):
    '''Reprents a student.'''
    def __init__(self,name,age,marks):
        SchoolMember.__init__(self, name, age)
        self.marks = marks
        print '(Initialized Student:%s)' %self.name
        
    def tell(self):
        SchoolMember.tell(self)
        print 'Marks:"%d"' %self.marks
        
if __name__ == '__main__':
    t = Teacher('Mrs.Shrividya',40,30000)
    s = Student('Swaroop',22,75)
    print #prints a blank Line
    
    members = [t,s]
    for member in members:
        member.tell()#work for both Teachers and Students