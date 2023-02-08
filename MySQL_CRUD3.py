import streamlit as st
#import pymysql
import pandas as pd
import mysql-connector

st.title("CRUD v3 en tablas de MySQL v8") 

st.markdown("Esta Streamlit app permite la Insercion(Create),\
            Consulta(Read), Actualizacion(Update) y Borrado(Delete)\
                en un par de tablas (paygrades,persons)\
                    de una BD(companydata)")
                    
st.image('ERDcompanydata.png')
#@st.cache(allow_output_mutation=True,
#          hash_funcs={"_thread.RLock": lambda _: None})

# proceso para establecer conexion con mysql y la bd
# especificada en archivo secrets.toml
#'C:\\Users\\conza\\WEB\\StreamlitKhorasani\\Chapter_5\\.streamlit\\secrets.toml'
def init_connection():
    #return pymysql.connect(**st.secrets["mysql"])
    return mysql-connector.connect(**st.secrets["mysql"])

# llama funcion de conexion y la regresa a la variable "conn"
conn = init_connection()


def consulta(query_str):
    cur = conn.cursor()
    cur.execute(query_str)
    data = cur.fetchall()
    cur.close()
    return data

def petcom(query_str):
    cur = conn.cursor()
    cur.execute(query_str)
    conn.commit()
    cur.close()
    

def muestra_paygrades():
    cur = conn.cursor()
    cur.execute("SELECT * FROM paygrades;")
    data = cur.fetchall()
    cur.close()
    df1=pd.DataFrame(data,columns=["id","base_salary",
                                  "reimbursement","bonuses"])
    return df1

def muestra_persons():
    cur = conn.cursor()
    cur.execute("SELECT * FROM persons;")
    data = cur.fetchall()
    cur.close()
    df2=pd.DataFrame(data,columns=["id","name",
                                    "date_of_birth","paygrade_id"])
    return df2
     

#Defining Columns
col1, col2 = st.columns(2)

with col1:
    CRUD1 = st.selectbox("Selecciona tipo consulta en tabla paygrades:",
                               ['Consultar','Insertar',
                                'Actualizar','Borrar'])
    if (CRUD1 == 'Consultar'):
        query = st.text_input("Escribe o modifica tu query de Consulta a\
                              MySQL v8","SELECT * FROM paygrades;")
        button1 = st.button("Ejecutar peticion de consulta en paygrades")
        
        if button1:
            try:
                output = consulta(query)
                df=pd.DataFrame(output,columns=["id","base_salary",
                                              "reimbursement","bonuses"])
                st.info("La tabla mostrada permite con el mouse\
                        ajustar el ancho de las columnas")
                st.dataframe(df)
            except:
                st.error('Error en la ejecucion de consulta en paygrades')
    
    elif (CRUD1 == 'Insertar'):
        query = st.text_input("Escribe o modifica tu query de INSERCION a\
                              MySQL v8",
        "INSERT INTO paygrades(base_salary,reimbursement,bonuses) VALUES('L1','L2','L3');")
        button2 = st.button("Ejecutar peticion de insercion en paygrades")
        if button2:
            try:
                petcom(query)
                st.success('Insercion exitosa')
                st.dataframe(muestra_paygrades())
            except:
                conn.rollback()
                st.error('Error en la ejecucion de insercion en paygrades')
    
    elif (CRUD1 == 'Actualizar'):
        query = st.text_input("Escribe o modifica tu query de Actualizacion\
                              a MySQL v8",
                              "UPDATE paygrades SET base_salary='L0' WHERE id=5;")
        button3 = st.button("Ejecutar peticion de Actualizacion en paygrades")
        if button3:
            try:
                petcom(query)
                st.success('Actualizacion exitosa')
                st.dataframe(muestra_paygrades())
            except:
                conn.rollback()
                st.error('Error en la ejecucion de actualizacion de paygrades')
    
    
    elif (CRUD1 == 'Borrar'):
        query = st.text_input("Escribe o modifica tu query de Borrado en\
                              MySQL v8",
                              "DELETE FROM paygrades WHERE id = 14;")
        button4 = st.button("Ejecutar peticion de insercion en paygrades")
        if button4:
            try:
                petcom(query)
                st.success('Borrado exitoso')
                st.dataframe(muestra_paygrades())
            except:
                conn.rollback()
                st.error('Error en la ejecucion de borrado en paygrades')

with col2:
    CRUD2 = st.selectbox("Selecciona tipo consulta en tabla persons:",
                               ['Consultar','Insertar',
                                'Actualizar','Borrar'])
    if (CRUD2 == 'Consultar'):
        query = st.text_input("Escribe o modifica tu query de Consulta a\
                              MySQL v8","SELECT * FROM persons;")
        button5 = st.button("Ejecutar peticion de consulta en persons")
        if button5:
            try:
                output = consulta(query)
                df2=pd.DataFrame(output,columns=["id","name",
                                                "date_of_birth","paygrade_id"])
                st.info("La tabla mostrada permite con el mouse\
                        ajustar el ancho de las columnas")
                st.dataframe(df2)
            except:
                st.error('Error en la ejecucion de consulta a persons')
        
    elif (CRUD2 == 'Insertar'):
        st.warning("La insercion de un nuevo registro requiere forzosamente un 'id' existente en paygrades")
        query = st.text_input("Escribe o modifica tu query de INSERCION a\
                              MySQL v8","INSERT INTO persons(id,name,date_of_birth,paygrade_id) VALUES(12,'Roger','10/11/1968',2);")
        
        button6 = st.button("Ejecutar peticion de insercion en persons")
        if button6:
            try:
                petcom(query)
                st.success('Insercion exitosa en persons')
                st.dataframe(muestra_persons())
            except:
                conn.rollback()
                st.error('Error en la ejecucion de insercion en persons')
    
    elif (CRUD2 == 'Actualizar'):
        query = st.text_input("Escribe o modifica tu query de Actualizacion\
                              a MySQL v8",
                              "UPDATE persons SET base_salary='L0' WHERE id=5;")
        button7 = st.button("Ejecutar peticion de Actualizacion en persons")
        if button7:
            try:
                petcom(query)
                st.success('Actualizacion exitosa en persons')
                st.dataframe(muestra_persons())
            except:
                conn.rollback()
                st.warning('Error en la ejecucion de actualizacion en persons')
    
    
    elif (CRUD2 == 'Borrar'):
        query = st.text_input("Escribe o modifica tu query de Borrado en\
                              MySQL v8",
                              "DELETE FROM persons WHERE id = 14;")
        button8 = st.button("Ejecutar peticion de borrado en persons")
        if button8:
            try:
                petcom(query)
                st.success('Borrado exitoso')
                st.dataframe(muestra_persons())
            except:
                conn.rollback()
                st.warning('Error en la ejecucion de borrado en persons')
                    
