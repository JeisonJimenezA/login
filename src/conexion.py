import pyodbc

server = '(localdb)\\Lucy'
bd_name= 'login_user'
usuarios= 'lucy'
contraseña= '123456'

try:
    conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL server};SERVER='+server+';DATABASE='+bd_name+';UID='+usuarios+';PWD='+contraseña)
    print('CONEXION EXITOSA')

except:
    print('error  en la conexion')