from langchain.chat_models import init_chat_model
from langchain.schema.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph,START,END 
from langgraph.graph.message import add_messages
from pydantic import BaseModel,Field
from typing_extensions import TypedDict,Annotated
from typing import Annotated, Literal,List
from environment import API_KEY,SUPABASE_URL,SUPABASE_KEY
from supabase import Client,create_client
import json
import warnings
import datetime
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")
##############################################################
#Data Collection(This will be different for an actual database)
##############################################################
supabase:Client=create_client(SUPABASE_URL,SUPABASE_KEY)
current_time = datetime.datetime.now()
def ConnNamesConnTypes():
    resp1=supabase.table("connector_types").select('name,type').execute()
    data=resp1.data 
    return data

def IdDataRetrieval(conn_name,conn_type):
    resp2=supabase.table("connector_types").select('id').ilike('name',conn_name).eq("type", conn_type).execute()
    id=resp2.data[0]['id']
    resp3=supabase.table("connector_attribute_definitions").select('key,label,data_type,required,description,default_value').eq("connector_type_id",id).execute()
    data=resp3.data
    return data

def Savingpayload(conn_name,conn_type,configuration,name):
    resp2=supabase.table("connector_types").select('id').ilike('name',conn_name).eq("type", conn_type).execute()
    id=resp2.data[0]['id']
    if(conn_type=='source'):
        res=supabase.table("connector_sources").insert({"name":name,"type":id,"configuration":configuration,"created_at":str(current_time),"updated_at":str(current_time)})
        res.execute()
        return 'Source connection created'
    elif(conn_type=='destination'):
        res=supabase.table("connector_destinations").insert({"name":name,"type":id,"configuration":configuration,"created_at":str(current_time),"updated_at":str(current_time)})
        res.execute()
        return 'Destination connection created'
basicinfo=ConnNamesConnTypes()
sample=str(IdDataRetrieval('Postgresql','source'))
###############################################################
# Chatbot Implementation
###############################################################
llm=init_chat_model("gemini-2.0-flash", model_provider="google_genai",google_api_key=API_KEY)
# Defined Output Frameworks
class UserReq(BaseModel):
   Conn_name: List[str]=Field(default_factory=list,description="Name of the connection(not users given name but the name of the storage)")
   Conn_type:List[str]=Field(default_factory=list,description="Type of connection whether source or destination")
   User_Info: List[str] = Field(default_factory=list,description='Store any inputted information from the user about the connection.')
class ClassifyingReq(BaseModel):
   Classify_Req: Literal['Task_Request','MoreInfo']=Field(description='Classify a request based on if they are')

class State(TypedDict):
    #First Part of the Network
    messages: Annotated[list, add_messages]
    assistant_messages: Annotated[list,add_messages]
    user_input:str
    Connection_Names:list
    Connection_Types:list
    User_Info:list
    #Second Part of the Network
    user_req:list 
    references:str|None
    config: dict
    question:str
    requiredparams:list
    collectedData:list
    missinginfo:list
    finalpayload:list
class PayloadFormatter(BaseModel):
   Required_Par:List[str] = Field(default_factory=list,description='''Store all the required parameters and subparameters as per the provided prompt.''')
   Collected_Info:List[str] = Field(default_factory=list,description='''To store extracted information.''')
class ExtractingMissingInfo(BaseModel):
   missingparams:List[str] = Field(default_factory=list,description='Store the additionally inputted parameters here')
   Keys:List[str] = Field(default_factory=list,description='Store the keys of each of the inputted parameter')
#Individual Function for conversational bot
#Has to be turned into a RAG Node 
def HelpNode(state:State):
   last_messages=state['messages'][-1]
   messages=[
      SystemMessage(f'''You are a chat assistant that will aid in answering queries from the user:
   -User will mostly ask questions on the sources and destination connections.
   -Ensure that your response is very polite and user friendly
   '''),
   last_messages
  ]
   reply=llm.invoke(messages)
   return reply.content

#Network for Handling User Request:
def UserRequest(state:State):
   try:
         last_message=state['messages'][-1]
         User_Input=state.get('user_input')

         if(User_Input==None):
            User_Input=last_message
         else:
            User_Input=HumanMessage(User_Input)
         exceptionshandler=False
         messages=[
         SystemMessage(
          f'''
        - You will be given an input string from the user regarding creating connections. 
        - Look through the user input and:
          1. Return a list of connections that the user specifed. Note: If the user specifies 2 connections of the same name
          and same type repeat that connection name on the list.
          2. Similarly return the connection type of the list. It can either be a source or destination
          3. If the user provides any information about the configurations of the connection return that information as a string.
          4. *Do not fill the list with values that are not from user input if the user hasnt specified something or has given you erroneous inputs then return an empty string for that parameter.*
          5. Also ensure that the connectors name can only be one of the names in this dictionary:{str(basicinfo)}
          6. *Ensure to include every connection inputted by the user.Do not skip anything*
          '''
        ),  
        User_Input
        ]
         struc_llm=llm.with_structured_output(UserReq)
         response=struc_llm.invoke(messages)
         conn_name=response.Conn_name
         conn_type=response.Conn_type 
         user_info=response.User_Info 
         connreq={}
         user_request=[]
         baseconditions=(len(conn_name)==len(conn_type)==len(user_info)) and ('' not in (conn_name and conn_type and user_info))
         if(baseconditions==True):
            exceptionshandler=True
            for i in range(len(conn_type)):
                if((conn_type[i]!='source' and conn_type[i]!='destination') or (conn_name[i].lower() not in user_info[i].lower())):
                  exceptionshandler=False
                  break 
                connreq['Conn_Name']=conn_name[i]
                connreq['Conn_Type']=conn_type[i]
                connreq['User_Info']=user_info[i]
                user_request.append(connreq)
                connreq={}
            if(exceptionshandler==False):
              # return {'next':'Diagnosis','user_input':User_Input,"Connection_Names":conn_name,"Connection_Types":conn_type,"User_Info":user_info}  
              print('Incorrect Information provided')
              return {'next':END}
            if(exceptionshandler==True):    
              return {'next':'Isconfigavailable','user_req':user_request}
         else:
              # return {'next':'Diagnosis','user_input':User_Input,"Connection_Names":conn_name,"Connection_Types":conn_type,"User_Info":user_info}  
              print('Incorrect Information provided')
              return {'next':END}  
   except Exception as e:
       print(e)

# Error handler needs further development
def Diagnosis(state:State):
   try:
     User_Input=state.get("user_input")
     conn_name=state.get("Connection_Names")
     conn_type=state.get("Connection_Types")
     user_info=state.get("User_Info")
     message=[
      SystemMessage(f'''         
            -Here are the results of extraction from the users request {conn_name},{conn_type} and {user_info}.
            -I want you to compare the users request with the results of the extraction and give possible reasons
            for why there are null values or incorrect fields in the results.
            1. Check if the user info for a specific connection is the right connection.
            Fo example: Conn_Name='Postgres' and User_Info='jdbc:mysql://lh:3306/db?method=STANDARD&useSSL=true&sslMode=PREFERRED'
            Here the user info given is for a mysql query.
            2.Check if any of the arrays has any null values because this means the user has not described the details of a specific connection.
            Fo example: Conn_Type='' 
            Here the user has not described whether they want a source or destination connector
                       '''),
      User_Input
      ]
     reply=llm.invoke(message)
     print(reply.content)
     User_Input=input("Would you like further details describing the problem?\n Type yes for more information \n Type no to if you want to just reinput information")
     return {'next':END}
   except Exception as e:
      print(e)
   
def Isconfigavailable(state:State):
   try:
      user_req=state.get("user_req")
      invalidconfigs=[]
      updated_list=[]
      s=[i['name']+' '+i['type'] for i in basicinfo]
      for i in user_req:
         if(i['Conn_Name']+' '+i['Conn_Type'] in s):
            i['Configref']=IdDataRetrieval(i['Conn_Name'],i['Conn_Type'])
            updated_list.append(i)
         else:
            invalidconfigs.append(i)
      if(len(invalidconfigs)!=0 and len(updated_list)!=0):
         print('The following configurations are not currently supported:')
         for i in invalidconfigs:
           print("->"+i['Conn_Name']+' '+i['Conn_Type'])
         user_input=input('Would you still like to continue creating the connections that work?')
         if(user_input.lower()=='yes'):
           return {'next':'InitialParsing','config':updated_list} 
         elif(user_input.lower()=='no'):
           return {'next':END}
         else:
           return {'next':END}
      elif(len(invalidconfigs)!=0 and len(updated_list)==0):
         print('Invalid Configuration')
         return {'next':END}
      elif(len(invalidconfigs)==0 and len(updated_list)!=0):
         return {'next':'InitialParsing','config':updated_list} 
   except Exception as e:
      print(e)

def Validation(Reqparams,collectedinfo):
    preproccolinfo=[]
    missing_params=[]
    for i in collectedinfo:
      s=i.find(':')
      w=i[:s]
      preproccolinfo.append(w)
    for n in Reqparams:
      if(n not in preproccolinfo):  
        missing_params.append(n) 
    return missing_params

def InitialParsing(state:State):
   try:
      configs=state.get('config')
      Req_par=state.get('requiredparams')
      Collected_info=state.get('collectedData')
      missing_info=state.get('missinginfo')
      if(Req_par==None):Req_par=[]
      if(Collected_info==None):Collected_info=[]
      if(missing_info==None):missing_info=[]
      if(len(Req_par)==0 and len(Collected_info)==0 and len(missing_info)==0):
            for i in configs:
                 message=f'''You are given payload {i} with the following information:
                  -Connection Name(Conn_Name).
                  -Connection Type(Conn_Type).
                  -Information given by the user for the connection(User_Info).
                  -Reference to the parameters and configuration for each attribute in that source(Configref):{i['Configref']}
                   Use this to do the following:
                   1.**Return a list of all required parameters and sub parameters. When you encounter a parameter refer to Configref and output the key.**
                   - Ensure there are only required parameters and sub parameters . Do not include optional parameters .
                   - Make sure to add only the parameters and sub-parameters where the required flag is set to true.
                   For example: 
                  -For a parameter with no subparameters: Append parameter_key.
                  -For a parameter with subparamters: Append parameter_key.subparameter_key
                  2.**Parse the user inputted (User_Info) into a list. Whatever input your provided you parse the input such that you return the parameter/subparameter key and the value as a pair.**
                 - In many of the inputs the value of the subparameter is given over the parameter. Using the configref make sure to fill the value as 'parameter.subparameter_val:(extracted value)'
                  For example:
                  User_Info:jdbc:mysql://lh:3306/db?method=STANDARD&useSSL=true&sslMode=PREFERRED.(Notice method=STANDARD)
                  Output:
                  Based on Configref you will output 'replication_method.method:STANDARD' and 'ssl_mode.mode=PREFERRED'
                 - Ignore parameters that are not present in configref.**Do not include attributes that are not present in configref these are supported by the application**.
                  For example:
                  User_Info:jdbc:postgresql://Lh:5432/Db?Schema=ab&sslmode=disable
                  Output:['database:Db','host:Lh','port:5432','schema:ab']  --Ignoring sslmode as it is not present in (configref) for postgres.
                 - ** Always ensure to extract and check the user provided information for all the required parameters**.
                  '''
                 struc_llm=llm.with_structured_output(PayloadFormatter)
                 reply=struc_llm.invoke(message)
                 Req_par.append(reply.Required_Par)
                 Collected_info.append(reply.Collected_Info)
            if(len(Req_par)==len(Collected_info)):
                for i in range(len(Req_par)):
                   v=Validation(Req_par[i],Collected_info[i])
                   missing_info.append(v)
                count=[len(i) for i in missing_info if i==[]]
                if(len(count)!=len(Req_par)):
                  return {'next':'Humaninputnode',"requiredparams":Req_par,"collectedData":Collected_info,"missinginfo":missing_info,'config':configs}
                else:
                 return {'next':"ParsingPayload","collectedData":Collected_info,'config':configs}
            else:
              print('System Error: LLM response volatile')
      elif(len(Req_par)!=0 and len(Collected_info)!=0 and len(missing_info)!=0):
         if(len(Req_par)==len(Collected_info)):
            missing_info=[]
            for i in range(len(Req_par)):
              v=Validation(Req_par[i],Collected_info[i])
              missing_info.append(v)
            count=[len(i) for i in missing_info if i==[]]
            if(len(count)!=len(Req_par)):
               return {'next':'Humaninputnode',"requiredparams":Req_par,"collectedData":Collected_info,"missinginfo":missing_info,'config':configs}
            else:
               print(Collected_info)
               return {'next':"ParsingPayload","collectedData":Collected_info,'config':configs}
         else:
            print('System Error: LLM response volatile')
            return {'next':END}
      else:
         print('System Error: LLM response volatile')
         return {'next':END}
   except Exception as e:
      print(e)   

def Humaninputnode(state:State):
   try:
      collecteddata=state.get('collectedData')
      requireddata=state.get('requiredparams')
      missingparams=state.get('missinginfo')
      configs=state.get('config')
      for i in range(len(missingparams)):
        flag=False
        if(len(missingparams[i])!=0):
          print('You are still missing the following details for this request: '+configs[i]['Conn_Name']+' '+configs[i]['Conn_Type']+str(i+1))
          s='You are still missing the following details for this request: '+configs[i]['Conn_Name']+' '+configs[i]['Conn_Type']+str(i+1)+'\n'
          for j in missingparams[i]:
            print('->'+j)
            s+='->'+j+'\n'
          missingp=input('Please add them:')
          message=f'''-Here is a checklist of missing parameters that has to be filled by a user:{s}
                      -Here are the user inputted values for each of these values:{missingp}                      
                      -Your first task is to extract the value of each parameter from the user input and return a list
                      of values in the order of {s}
                      - Also ensure you return a list of the keys of the values entered in the user inputted values
                      -**If the user does not input any information at all the return both lists created earlier as empty lists**.
                      **Do not add values which are not associated with the missing values**'''
          struc_llm=llm.with_structured_output(ExtractingMissingInfo)
          res=struc_llm.invoke(message)
          param_values=res.missingparams
          keys=res.Keys
          if(len(param_values)==len(missingparams[i]) and (len(param_values)!=0)):
            for j in range(len(missingparams[i])):
              collecteddata[i].append(missingparams[i][j]+':'+param_values[j])
          elif(len(param_values)!=len(missingparams) and (len(param_values)!=0)):
               for k in range(len(keys)):
                  collecteddata[i].append(keys[k]+':'+param_values[k])
               flag=True
          elif(len(param_values)==0):
             flag=True
          if(flag==True):
             break      
        else:
           continue
      return {'next':'InitialParsing',"requiredparams":requireddata,"collectedData": collecteddata}
   except Exception as e:
      print(e)

def ParsingPayload(state:State):
   try:
    config=state.get("config")
    Collected_info=state.get("collectedData")
    finalpayloads=[]
    finalpayloads1=[]
    payload={}
    for i in range(len(Collected_info)):
      s=str(config[i]['Configref'])
      message=f'''
       -Here is a list of configurational details {str(Collected_info[i])} given by the user.        
         -Your job is to take this payload and transform it into a json payload.
         - Perform this task in the following way step by step:
         1. Look through config structure: {s} and grasp the structure of each attribute in the user configurations
         2. Render the structure of each of these variables in the user input based on the references
         Here is an example for you:
         Data Given:
         User-Inputted-List:{{'database': 'db1', 'host': 'localhost', 'port': '3306', 'schema':'ab','username': 'user1', 'password':'password12'}} 
         Config-Structure:{sample}
         Output:
         {{
            'database': 'db1', 
            'host': 'localhost', 
            'port': '3306', 
            'schema':'ab',
            'username': 'user1',
            'password':'password12'
         }}
         3. Only output the json payload                  
     '''
      reply=llm.invoke(message)
      response=reply.content
      start=response.find('json')
      final_payload=json.loads(response[start+4:-3])
      finalpayloads1.append(final_payload) 
      payload['name']=input('Enter a name for the '+config[i]['Conn_Name']+' '+config[i]['Conn_Type']+' connection:')
      payload['workspacename']=input('Enter the name of the workspace in which you want to create the '+config[i]['Conn_Name']+' '+config[i]['Conn_Type']+' connection:')
      payload['configuration']=final_payload 
      message=Savingpayload(config[i]['Conn_Name'],config[i]['Conn_Type'],payload['configuration'],payload['name'])
      print(message)
      finalpayloads.append(payload)
      payload={}
    for i in finalpayloads:
      print(i)
    return {'next':END}
   except Exception as e:
      print(e)
#Initializing network:
#Adding Nodes
graph_builder = StateGraph(State)
graph_builder.add_node("UserRequest",UserRequest)
graph_builder.add_node("Diagnosis",Diagnosis)
graph_builder.add_node("Isconfigavailable",Isconfigavailable)
graph_builder.add_node("InitialParsing",InitialParsing)
graph_builder.add_node("Humaninputnode",Humaninputnode)
graph_builder.add_node("ParsingPayload",ParsingPayload)
#Adding edges
graph_builder.add_edge(START,"UserRequest")
graph_builder.add_conditional_edges("UserRequest",
                                    lambda state:state.get("next"))
graph_builder.add_edge("Diagnosis",END)
graph_builder.add_conditional_edges("Isconfigavailable",
                                    lambda state:state.get("next"))
graph_builder.add_conditional_edges("InitialParsing",
                                    lambda state:state.get("next"))
graph_builder.add_edge("Humaninputnode","InitialParsing")
graph_builder.add_edge("ParsingPayload",END)
graph = graph_builder.compile()
#Running the Chatbot
def run_chatbot():
    state={"messages":[]}
    while True:
         user_input = input("Message: ")
         if user_input == "exit":
            print("Bye")
            break
         message=f'''You have to classify the user input:{user_input} into either a request to create connections or a request for more information. 
         Grasp the users request based on their language . If they want to create connections then return Task_Request
         and if the input looks like they want a conversation or need assistance then return MoreInfo.
         - Sometimes the user would give very ambigous requests if you dont understand the request then return MoreInfo.'''
         struc_llm=llm.with_structured_output(ClassifyingReq)
         reply=struc_llm.invoke(message)
         if(reply.Classify_Req=='Task_Request'):
            state["messages"] = state.get("messages", []) + [
            {"role": "user", "content": user_input} ]
            state=graph.invoke(state)
            state={ "user_req":[],"Connection_Names":[],"Connection_Types":[],"User_Info":[],"config":{},"collectedData":[],"missinginfo":[],"finalpayload":[]}
         elif(reply.Classify_Req=='MoreInfo'):
            state["messages"] = state.get("messages", []) + [
            {"role": "user", "content": user_input} ]
            print(state['messages'][-1])
            reply1=HelpNode(state)
            print(reply1)
        # print(stage1)
        # state["messages"] = state.get("messages", []) + [
        #     {"role": "user", "content": user_input}
        # ]    
        # if state.get("messages") and len(state["messages"]) > 0:
        #     last_message = state["messages"][-1]
        #     print(f"Assistant: {last_message}")
    #         state = {"messages": [], "message_type": None,"basicconfigdet":None,"checklist":None, "references":None,"confirmation":None,"question":None,"config":{},"question":None
    # ,"key":[]}

if __name__ == "__main__":
    run_chatbot()

