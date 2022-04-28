from selenium import webdriver
import pandas as pd
import json


url = "https://www.sii.cl/servicios_online/1047-nomina_inst_financieras-1714.html"
driver = webdriver.Chrome(executable_path='D:\Carpeta Personal\Python\desafio-postulantes\chromedriver.exe')
driver.get(url)

# element = driver.find_element_by_xpath("//div[@class='col-sm-9 contenido']")
# print(element.get_attribute('innerHTML'))

element_title = driver.find_element_by_xpath('//*[@id="my-wrapper"]/div[2]/div/div/div[2]/h2')

element_p = driver.find_element_by_xpath('//*[@id="my-wrapper"]/div[2]/div/div/div[2]/p[2]')

html = driver.page_source

list_of_dfs = pd.read_html(html)

df = list_of_dfs[0]

df = df.dropna()

df = df.astype({"No.":int},errors= 'raise')

df = df.set_index('No.')

df_datos_inscripcion = df.iloc[:,2].str.split('/',expand=True)

# df_datos_inscripcion.columns = ['DATOS INSCRIPCIÓN (DR)', 'DATOS INSCRIPCIÓN (RES. No)', 'DATOS INSCRIPCIÓN (FECHA)']

df_datos_actualizacion = df.iloc[:,4].str.split('/',expand=True)

# df_datos_actualizacion.columns = ['DATOS ÚLTIMA ACTUALIZACIÓN (DR)', 'DATOS ÚLTIMA ACTUALIZACIÓN(RES. No)', 'DATOS ÚLTIMA ACTUALIZACIÓN (FECHA)']


df = df.drop(df.columns[[2,4]],axis=1)

df.insert(2,'DATOS INSCRIPCIÓN (FECHA)',df_datos_inscripcion.iloc[:,2],True)

df.insert(2,'DATOS INSCRIPCIÓN (RES. No)',df_datos_inscripcion.iloc[:,1],True)

df.insert(2,'DATOS INSCRIPCIÓN (DR)',df_datos_inscripcion.iloc[:,0],True)

df.insert(6,'DATOS ÚLTIMA ACTUALIZACIÓN (FECHA)',df_datos_actualizacion.iloc[:,2],True)

df.insert(6,'DATOS ÚLTIMA ACTUALIZACIÓN (RES. No)',df_datos_actualizacion.iloc[:,1],True)

df.insert(6,'DATOS ÚLTIMA ACTUALIZACIÓN (DR)',df_datos_actualizacion.iloc[:,0],True)

df_dict = df.to_dict("index")

output = {"Titulo":element_title.text,"Parrafo":element_p.text,"Tabla": df_dict}


with open("sample.json", "w", encoding='utf-8') as outfile:
    json.dump(output, outfile,ensure_ascii=False)


# with open("sample.json", "w", encoding='utf-8') as outfile:
#     json.dump(output, outfile,ensure_ascii=False)

driver.quit()

# col-sm-9 contenido
# //*[@id="my-wrapper"]/div[2]/div/div/div[2]/h2/text()
# //*[@id="my-wrapper"]/div[2]/div/div/div[2]/p[2]
# //*[@id="tabledatasii"]



