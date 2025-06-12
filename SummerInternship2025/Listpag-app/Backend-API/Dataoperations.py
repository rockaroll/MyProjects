from environment import SUPABASE_URL,SUPABASE_KEY 
from supabase import create_client,Client
import datetime
class Dataops:
    def __init__(self,url,key):
        self.url=url 
        self.key=key 
    def Connection(self):
        supabase:Client = create_client(self.url, self.key)
        self.cli=supabase

    def dsplitter1(self,date):  
        datesplt=date.split('-')
        year=int(datesplt[0])
        month=int(datesplt[1])
        day=int(datesplt[2])
        x=datetime.datetime(year,month,day)
        fin=x.strftime("%b")+" "+str(day)+","+str(year)
        return fin
    
    def Titlesplitter(self):
        for i in range(len(self.data)):
            s=self.data[i]['title'].split('\n')
            self.data[i]['title']=s

    def Dateconverter(self):
        for i in range(len(self.data)):
            self.data[i]['deadline']=self.dsplitter1(self.data[i]['deadline'])
            self.data[i]['Submit']=self.dsplitter1(self.data[i]['Submit'])
            
    def Retrieve(self):
        self.Connection()
        response = self.cli.table("rfps").select("*").execute()
        self.data=response.data
        self.Dateconverter()
        self.Titlesplitter()
        self.count=len(self.data)
    def exec(self):
        self.Retrieve()

# s1=Dataops(SUPABASE_URL,SUPABASE_KEY)
# s1.exec()
# print(s1.data)
