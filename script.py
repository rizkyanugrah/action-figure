import os
import time
import pandas as pd
from tabulate import tabulate


class Application:
    CSV_FILE = 'data.csv'

    users = {
        "role": ['user', 'admin'],
        "username":  ["user", "admin"],
        "password": ["user", "admin"],
        "ID": [1, 2]
    }

    def cls(self):
        os.system('cls')
        return

    def register(self):
        Create_Username = input("\nMasukan Username : ")
        if Create_Username in self.users.get("username"):
            print("Username Telah Terdaftar, Silahkan Pilih Username Yang Lain")
            return self.register()
        else:
            Create_Password = input("Masukan Password : ")
            self.users.get("role").append("user")
            self.users.get("username").append(Create_Username)
            self.users.get("password").append(Create_Password)
            ID = len(self.users.get("ID"))
            self.users.get("ID").append(ID+1)
            print("\nData Berhasil Di Tambahkan")
            return self.login(Create_Username, Create_Password)

    def login(self, name, password):
        try:
            search_user = self.users.get("username").index(name)

            if self.users.get("username")[search_user] and password == self.users.get("password")[search_user]:
                if self.users.get("role")[search_user] == "admin":
                    return "admin"
                else:
                    return "user"
            else:
                print("\nGagal Login Password Anda Salah!")
                time.sleep(2)
                return self.main()
        except:
            print("\nMaaf Data Tidak Tersedia!")
            time.sleep(2)
            self.main()

    def showAll(self):
        print('DAFTAR ACTION FIGURE')

        df = pd.read_csv(self.CSV_FILE)

        print(tabulate(df, headers='keys', showindex='never', tablefmt='pretty'))

        return

    def insertData(self):
        code = input("\nMasukkan Kode : ")
        name = input("Masukkan Nama : ")
        price = input("Masukkan Harga : ")
        stock = input("Masukkan Stok : ")

        data = [
            [code, name, price, stock]
        ]

        newData = pd.DataFrame(data)

        newData.to_csv('data.csv', index=False, mode='a', header=False)

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
        df = pd.read_csv(self.CSV_FILE)
        df = df[df['KODE'] != code]

        df.to_csv(self.CSV_FILE, index=False)

        return

    def menuList(self):
        print('\nMenu List User ')
        print('\n[1] Daftar Action Figure')
        print('[99] Selesai')

        menu = int(input('Masukan menu yang ingin dipilih : '))

        return menu

    def menuListAdmin(self):
        print('\nMenu List Admin ')
        print('\n[1] Daftar Action Figure')
        print('[2] Tambah Action Figure')
        print('[3] Ubah Action Figure')
        print('[4] Hapus Action Figure')
        print('[99] Selesai')

        menu = int(input('Masukan menu yang ingin dipilih : '))

        return menu

    def main(self):
        self.cls()

        print("Silahkan login jika sudah punya akun")
        print("Silahkan register jika anda belum memiliki akun")

        option = input("\n(Login/Register) : ").lower()

        if (option == "login"):
            username = input("\nmasukan username anda : ")
            password = input("masukan password anda : ")
            role = self.login(username, password)

        elif (option == "register"):
            role = self.register()

        else:
            print("\nMasukan Inputan Yang Benar")
            time.sleep(2)
            return self.main()

        self.cls()
        terminate = False

        try:
            while terminate == False:
                if role == "admin":
                    menu = self.menuListAdmin()
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
                    elif menu == 99:
                        print("\nTerima Kasih Telah Mencoba Aplikasi Action-Figure")
                        terminate = True

                elif role == "user":
                    menu = self.menuList()
                    if menu == 1:
                        self.cls()
                        self.showAll()
                    elif menu == 99:
                        print("\nTerima Kasih Telah Mencoba Aplikasi Action-Figure")
                        terminate = True

        except KeyboardInterrupt:
            print("\nSampai nanti!")


application = Application()
application.main()
