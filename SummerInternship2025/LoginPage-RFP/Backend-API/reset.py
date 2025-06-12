 
import psycopg2
from configparser import ConfigParser
#For the changing password page
class ChangePassword:
    def __init__(self,path,password,email):
        self.email=email
        self.password=password 
        self.path=path
    #Establishing Connection with database
    def config(self,section='postgresql'):
       parser=ConfigParser()
       parser.read(self.path)
       db={}
       if parser.has_section(section):
          params=parser.items(section)  
          for param in params:
              db[param[0]]=param[1] 
       else:
         raise Exception('Section {0} not found in the {1} file'.format(section, self.path))
       return db
    #Establishing connection and cursors
    def connection(self):
       self.params=self.config()
       self.conn=psycopg2.connect(**self.params)
       self.cur=self.conn.cursor()
    #Ending connection and cursors
    def endconncurs(self):
       self.cur.close()
       self.conn.close()
    #Validation of emails
    def Validation(self):
        verquer="select email from userdetailsmd5"
        self.connection()
        self.cur.execute(verquer)
        details=self.cur.fetchall()
        self.endconncurs()
        d=[i[0] for i in details]
        if(self.email in d):
           return 1 
        else:
           return 0
   #Password Changing
    def PasswordChange(self):
        updatequery="update userdetailsmd5 set "+"passwordfield="+"'"+self.password+"'"+" where email="+"'"+self.email+"'"
        self.connection()
        self.cur.execute(updatequery)
        self.conn.commit()
        self.endconncurs()
   #Execution func of class
    def exec(self):
       s=self.Validation()
       if(s==1):
          self.PasswordChange()
          self.message='Password has been changed'
       else:
          self.message='Email is not registered with us create an account'
       
        
        



        

