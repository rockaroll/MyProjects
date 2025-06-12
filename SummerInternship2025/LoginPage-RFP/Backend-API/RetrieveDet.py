import psycopg2
from configparser import ConfigParser
##Class to implement authorization on the backend
class Authorization:
   #Takes in details of the environment, username and passsword
    def __init__(self,path,Username,Password):
        self.path=path 
        self.Username=Username 
        self.Password=Password
   #Returns parameters of database configuration
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
   #Defines connection with database
    def connection(self):
       self.params=self.config()
       self.conn=psycopg2.connect(**self.params)
       self.cur=self.conn.cursor()
   #Closing connection and cursor of the database
    def endconncurs(self):
      self.cur.close()
      self.conn.close()
   #Retrieval of usernames and encrypted passwords to make comparison with user inputs      
    def recordretrieval(self):
       Command='select username,passwordfield from userdetailsmd5'
       self.connection()
       self.cur.execute(Command)
       details=self.cur.fetchall()
       username_list=[i[0] for i in details]
       password_list=[i[1] for i in details]
       return username_list,password_list
    #Final comparison to complete authentication
    def Authorization(self,unamelist,passwordlist):
      if((self.Username in unamelist) and (self.Password in passwordlist)):
         message='You are registered in database'
      else:
         message='You are not registered in database' 
      return message
   #Execution of main pipeline
    def exec(self):
        usernames,passwords=self.recordretrieval()
        self.message=self.Authorization(usernames,passwords)
        self.endconncurs()
    