#!/usr/bin/python3
import os
import pandas as pd
from tabulate import tabulate


class Application:
    CSV_FILE = 'data.csv'

    def cls(self):
        os.system('cls||clear')

        return

    def showAll(self):
        print('DAFTAR ACTION FIGURE')

        df = pd.read_csv(self.CSV_FILE)

        print(tabulate(df, headers='keys'))

        return

    def insertData(self):
        code = input("\nMasukkan Kode : ")
        name = input("Masukkan Nama : ")
        price = input("Masukkan Harga : ")
        stock = input("Masukkan Stok : ")

        df = pd.read_csv(self.CSV_FILE)

        df.loc[len(df)] = [code, name, price, stock]

        df.to_csv(self.CSV_FILE, index=False)

        return

    def changeData(self):
        self.showAll()
        code = int(input("Pilih data dengan kode : "))

        df = pd.read_csv(self.CSV_FILE)
        df = df[df['KODE'] != code]

        codeInput = input("\nMasukkan Kode : ")
        nameInput = input("Masukkan Nama : ")
        priceInput = input("Masukkan Harga : ")
        stockInput = input("Masukkan Stok : ")

        df.loc[len(df)] = [codeInput, nameInput, priceInput, stockInput]

        df.to_csv(self.CSV_FILE, index=False)

        return

    def deleteData(self):
        self.showAll()

        code = int(input("\nPilih data dengan kode : "))
        df = pd.read_csv(self.CSV_FILE
                         )
        df = df[df['KODE'] != code]

        df.to_csv(self.CSV_FILE, index=False)

        return

    def menuList(self):
        print('\nMenu')
        print('[1] Daftar Action Figure')
        print('[2] Tambah Action Figure')
        print('[3] Ubah Action Figure')
        print('[4] Hapus Action Figure')
        print('[8] Selesai')

        menu = int(input('Masukan menu yang ingin dipilih : '))

        return menu

    def main(self):
        self.cls()
        terminate = False

        self.showAll()

        try:
            while terminate == False:
                menu = self.menuList()

                if menu == 1:
                    self.cls()
                    self.showAll()
                elif menu == 2:
                    self.cls()
                    self.showAll()

                    self.insertData()
                    self.cls()
                    self.showAll()
                elif menu == 3:
                    self.cls()
                    self.changeData()

                    self.cls()
                    self.showAll()
                elif menu == 4:
                    self.cls()
                    self.deleteData()

                    self.cls()
                    self.showAll()
                elif menu == 0:
                    terminate = True
                else:
                    print('Masukan pilihan yang tersedia')
        except KeyboardInterrupt:
            print("\nSampai nanti!")


application = Application()
application.main()
