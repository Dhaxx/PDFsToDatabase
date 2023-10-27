'''
1 - Discover how to rename the files like the example "0001/23";
2 - Convert the PDF file to blob format;
3 - Insert the files in the DB. The table's name is transp_contratos;
'''
import os
from connection import connect, commit

def renameFile(year):
    directory = f'D:\\Programação\\PDFsToDatabase\\venv\\Contratos\\{year}'
    duplicateds = []
    for file in os.listdir(directory):
        if '@' in file:
            continue

        if file[0].isdigit():
            number, year = file.split('.', 1)
            number = number.zfill(4)
            new_name = f'{number}@{year[:2]}.pdf'

            old_name = os.path.join(directory, file).replace('\\', '/')
            new_name_file = os.path.join(directory, new_name).replace('\\', '/')

            try:
                os.rename(old_name, new_name_file)
            except:
                duplicateds.append(file)

    print('contrats renamed with sucess!')
    print(f'duplicateds: {duplicateds}',sep=' ')

def insertFile(year):
    cnx = connect(year)
    cur = cnx.cursor()
    directory = f'D:\\Programação\\PDFsToDatabase\\venv\\Contratos\\{year}'

    cur.execute('DELETE  FROM TRANSP_CONTRATOS tc ')
    commit(cnx)

    insert = cur.prep("insert into transp_contratos (id_contrato, codigo, empresa, arquivo, arquivo_tipo, sobre_covid, FK_CONTRATOSADITAMENTO, ARQUIVO_DESCRICAO) values (?,?,?,?,?,?,?,?)")
    insert_publi = cur.prep("insert into contratos_publicacoes (contrato, veicpub, dtpub, descr, pubveioficial, tipo) values(?,?,?,?,?,?)")
    empresa = cur.execute("select empresa from cadcli").fetchone()[0]

    for i, file in enumerate(os.listdir(directory)):
        i += 1
        with open(os.path.join(directory, file), 'rb') as file_stream:
            if file[0].isdigit():
                id = file.replace('@','/').split('.')
                dtpub = cur.execute(f"select dtpubl from contratos where codigo = '{id[0]}'").fetchone()
                dtpub = dtpub[0] if dtpub is not None else f'31.12.{year}'
                cur.execute(insert,(i,id[0],empresa,file_stream.read(), 'PDF', 'N', None, 'CONTRATO'))
                cur.execute(insert_publi,(id[0],3,dtpub,'PUBLICAÇÃO DE CONTRATO','N','C'))
            else:
                name_file = file.replace('(A','').replace(')','')
                additive, id = name_file.replace('.pdf','').split(" ")
                id = id.replace('.1','/1').replace('@','/')
                additive = str(additive.zfill(5))
                term_number = cur.execute(f"select PK_CONTRATOSADITAMENTO from contratosaditamento where contrato = '{id}' and termo containing '{additive}'").fetchone()
                try:
                    term_number = term_number[0]
                except:
                    print(f'Contrato: {id} - Termo {additive} não encontrado!')
                    continue
                cur.execute(insert,(i,id,empresa,file_stream.read(), 'PDF', 'N', term_number, f'TERMO {additive}'))
        commit(cnx)