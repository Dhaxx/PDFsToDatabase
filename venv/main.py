import functions

directory = "D:\\Programação\\PDFsToDatabase\\venv\\Contratos\\2022\\"

def main():
    functions.renameFile(2022)
    functions.insertFile(2022)
    print('finalizado')

if __name__ == '__main__':
    main()