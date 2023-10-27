import fdb

def connect(year):
    cnx = fdb.connect(dsn=f"D:\\Fiorilli\\SCPI_8\\Cidades\\PM-FARTURA\\ARQ{year}\\SCPI{year}.FDB", user='xxxxx', password='xxxxx', 
                        port='3050', fb_library_name='C:\\Program Files\\Firebird\\Firebird_2_5\\bin\\fbclient.dll')
    return cnx

def commit(cnx):
    cnx.commit()
