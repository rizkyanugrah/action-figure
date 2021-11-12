import os
import time
import pandas
import pwinput
import locale
from tabulate import tabulate
from termcolor import colored


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
                print(colored('Username atau password salah!', 'red'))
                time.sleep(2)
                return self.main()
        except:
            print(colored('Maaf data tidak tersedia!', 'yellow'))
            time.sleep(2)
            self.main()

    def showAll(self):
        print(colored('[+] DAFTAR ACTION FIGURE [+]\n', 'green'))

        df = pandas.read_csv(self.CSV_FILE)

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

        newData = pandas.DataFrame(data)

        newData.to_csv('data.csv', index=False, mode='a', header=False)

        return

    def changeData(self):
        self.showAll()
        code = int(input("\nPilih data dengan kode : "))

        df = pandas.read_csv(self.CSV_FILE)

        # select row of data based on code variable
        selectedData = df.loc[df.KODE == code]
        index = selectedData.index.values[0]

        print('Note: Ketik Enter jika data tidak ingin diubah')

        codeInput = input("\nMasukkan Kode : ")
        nameInput = input("Masukkan Nama : ")
        priceInput = input("Masukkan Harga : ")
        stockInput = input("Masukkan Stok : ")

        # change the data based on user input
        # there is a null coalesce 'feature'
        df.at[index, 'KODE'] = self.coalesce(
            codeInput, selectedData.values[0][0])
        df.at[index, 'NAMA'] = self.coalesce(
            nameInput, selectedData.values[0][1])
        df.at[index, 'HARGA'] = self.coalesce(
            priceInput, selectedData.values[0][2])
        df.at[index, 'STOK'] = self.coalesce(
            stockInput, selectedData.values[0][3])

        df.to_csv(self.CSV_FILE, index=False)

        return

    def coalesce(self, value_one, value_two):
        if value_one == "":
            return value_two
        else:
            return value_one

    def deleteData(self):
        self.showAll()

        code = int(input("\nPilih data dengan kode : "))

        df = pandas.read_csv(self.CSV_FILE)

        selectedData = df[df['KODE'] == code].index

        if selectedData.empty:
            print(colored('Data tidak ditemukan!', 'red'))
            time.sleep(2)

            return

        # if KODE row based on data frame same as code variable, delete it
        df.drop(df[df['KODE'] == code].index, inplace=True)

        # making change to csv file
        df.to_csv(self.CSV_FILE, index=False)

        return

    def menuList(self):
        print(colored('[====================]', 'green'))
        print(colored('[+] Menu List User [+]', 'yellow'))
        print(colored('[====================]', 'green'))
        print(colored('[1]', 'magenta'), 'Daftar Action Figure')
        print(colored('[99]', 'red'), 'Keluar Aplikasi')

        menu = int(input('Masukan menu yang ingin dipilih : '))

        return menu

    def menuListAdmin(self):
        print(colored('[====================]', 'green'))
        print(colored('[+] Menu List Admin [+]', 'yellow'))
        print(colored('[====================]', 'green'))
        print(colored('[1]', 'magenta'), 'Daftar Action Figure')
        print(colored('[2]', 'blue'), 'Tambah Action Figure')
        print(colored('[3]', 'green'), 'Ubah Action Figure')
        print(colored('[4]', 'red'), 'Hapus Action Figure')
        print(colored('[5]', 'yellow'), 'Transaksi')
        print(colored('[99]', 'red'), 'Keluar Aplikasi')

        menu = int(input('\nMasukan menu yang ingin dipilih : '))

        return menu

    def transaction(self):
        self.showAll()

        code = int(input("\nPilih data dengan kode : "))

        df = pandas.read_csv(self.CSV_FILE, index_col=False)

        selectedData = df.loc[df['KODE'] == code]

        if selectedData.empty:
            print(colored('Data tidak ditemukan!', 'red'))
            time.sleep(2)

            return

        code = selectedData.values[0][0]
        name = selectedData.values[0][1]
        price = selectedData.values[0][2]
        stock = selectedData.values[0][3]

        print(f'\nData dengan KODE {code} tersedia.\n')

        print(tabulate({'KODE': [code],
                        'NAMA': [name],
                        'HARGA': [price],
                        'STOK': [stock],
                        }, headers='keys'))

        coloredName = colored(name, 'cyan')
        coloredPrice = colored(price, 'green')

        print(f'\nHarga satuan dari {coloredName} adalah {coloredPrice}.')

        amount = int(input('\nBerapa yang ingin dibeli : '))

        summary = colored(price * amount, 'green')

        print(f'\nTotal = {price} x {stock} = {summary}')

        print(f'Total pembayaran adalah : {summary}')

        paid = input('\nApakah sudah selesai membayar (Y/N) : ').lower()

        if paid == 'n':
            print(colored('Pembayaran tidak dilanjutkan!', 'red'))
            time.sleep(3)

            return

        # substraction the existing stock based on stock input
        df.loc[df.KODE == code, 'STOK'] -= stock

        df.to_csv('data.csv', index=False)

        print(colored('\nTerima kasih sudah membayar! ^^', 'green'))
        time.sleep(3)

        return

    def main(self):
        self.cls()

        print(
            colored('[========================================================]', 'green'))
        print(
            colored("[+] Silahkan login jika sudah punya akun \t\t[+]", 'yellow'))
        print(
            colored("[+] Silahkan register jika anda belum memiliki akun \t[+]", 'yellow'))
        print(
            colored('[========================================================]', 'green'))

        option = input("\n(Login/Register) : ").lower()

        if (option == "login"):
            username = input("\nMasukkan Username Anda : ")
            password = pwinput.pwinput()
            role = self.login(username, password)

        elif (option == "register"):
            role = self.register()

        else:
            print(colored('Masukkan inputan dengan benar!', 'red'))
            time.sleep(2)

            return self.main()

        self.cls()
        terminate = False

        self.showAll()

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
                    elif menu == 5:
                        self.cls()
                        self.transaction()

                        time.sleep(2)

                        self.cls()

                    elif menu == 99:
                        print(
                            colored(print("\nTerima Kasih Telah Mencoba Aplikasi Action-Figure", 'green')))
                        terminate = True

                elif role == "user":
                    menu = self.menuList()
                    if menu == 1:
                        self.cls()
                        self.showAll()
                    elif menu == 99:
                        print(
                            colored(print("\nTerima Kasih Telah Mencoba Aplikasi Action-Figure", 'green')))
                        terminate = True

        except KeyboardInterrupt:
            print("\nSampai nanti!")


application = Application()
application.main()
