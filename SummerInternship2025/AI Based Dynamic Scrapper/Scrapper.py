from google import genai
from environment import gkey
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import json
driver=webdriver.Chrome()
url='INSERT AIRBYTE SOURCE OR DESTINATION API'
def LT(container,visited=set()):
    buttons1=container.find_elements(By.CSS_SELECTOR,"button.headerItem_or_5.clickable_IVfe.propertyName_Fta7")
    if(len(buttons1)!=0):
      for i in range(len(buttons1)):
        buttons1[i].click()
        panel_id=buttons1[i].get_attribute("aria-controls")
        WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.ID,panel_id))
        )
        container2=driver.find_element(By.ID,panel_id)
        LT(container2)
def DynamicLayercount(url1):
    driver.get(url1)
    button=driver.find_elements(By.CSS_SELECTOR,"button.headerItem_or_5.clickable_IVfe.propertyName_Fta7")
    for i in range(len(button)):
        selectedButton=button[i]
        selectedButton.click()
        panel_id=selectedButton.get_attribute("aria-controls")
        WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.ID,panel_id))
        )
        container1=driver.find_element(By.ID,panel_id)
        LT(container1)

def MainExtraction(url2):
  try:
    DynamicLayercount(url2)
    page=driver.find_element(By.CLASS_NAME,"grid_eKW9")
    page_html=page.get_attribute('outerHTML')
    return page_html,page.text
  except Exception as e:
     print(e)
     return None,None
  finally:
     driver.quit()

pg_html,pg_text=MainExtraction(url)
client = genai.Client(api_key=gkey)
def cusgemni(input_t):
  response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=input_t,
  )
  return response.text
prompt=f'''
You are  agent that parses raw text data into a valid format. Your job is to look at the provided text data:{pg_text} and convert them into the given output. Think step by step.
Make sure to look at the section of the site to fill in all these details.'''+'''
Output is like this:
[
    {
    
        "label": (Label Name),
        "requiredParam": (Values can be:TRUE OR FALSE),
        "key": (Key Value),
        "data_type": (Data Type value),
        "Description":(Look for description of parameter)
        "Options(Include this section if this specific variable has subparameters)":[
                     {
                        "SubParameter-Label":(Fill in the subparameters label),
                        "SubParameter-Type":(If there is a type value then include it otherwise if it is blank do not include this parameter),
                        "SubParameter-Key":(If there is a key value then include it otherwise if it is blank do not include this parameter)
                        "SubParameter-Description":(Include the description of the values)
                        "Options(Include Include this section if this specific subparameters has more subparameters )":{
                                      # Follow the given structure

                                           
                                      }
 
                                    }
 
                      ]
    },
]

'''
response=cusgemni(prompt)
start=response.find('json')
# print(response[start+4:-3])
final_payload=json.loads(response[start+4:-3])
with open("payloadfinal-mysqldest.json", "w") as outfile:
  json.dump(final_payload,outfile,indent=4)