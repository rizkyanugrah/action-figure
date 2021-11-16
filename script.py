import os
import time
import pandas
import pwinput
import random
from tabulate import tabulate
from termcolor import colored
from datetime import datetime


class Application:
    ACTION_FIGURE_CSV = 'data.csv'
    TRANSACTION_HISTORY_CSV = 'history.csv'

    USERS = {
        "role": ['user', 'admin'],
        "username":  ["user", "admin"],
        "password": ["user", "admin"],
        "ID": [1, 2]
    }

    # Clear Terminal
    def cls(self):
        os.system('cls')
        return
    
    # Format Rupiah
    def formatrupiah(self, uang):
        y = str(uang)
        if len(y) <= 3 :
            return 'Rp ' + y     
        else :
            p = y[-3:]
            q = y[:-3]
            return   self.formatrupiah(q) + '.' + p
            print ('Rp ') +  self.formatrupiah(q) + '.' + p
        
    # Slice money
    def Regex(self, uang):
        money = uang
        get_int_only = ''.join(x for x in money if x.isdigit())
        return int(get_int_only)
        
    def register(self):
        Create_Username = input("\nMasukan Username : ")
        if Create_Username in self.USERS.get("username"):
            print("Username Telah Terdaftar, Silahkan Pilih Username Yang Lain")
            return self.register()
        else:
            Create_Password = input("Masukan Password : ")
            self.USERS.get("role").append("user")
            self.USERS.get("username").append(Create_Username)
            self.USERS.get("password").append(Create_Password)
            ID = len(self.USERS.get("ID"))
            self.USERS.get("ID").append(ID+1)
            print("\nData Berhasil Di Tambahkan")
            return self.login(Create_Username, Create_Password)

    def login(self, name, password):
        try:
            search_user = self.USERS.get("username").index(name)

            if self.USERS.get("username")[search_user] and password == self.USERS.get("password")[search_user]:
                if self.USERS.get("role")[search_user] == "admin":
                    return "admin"
                else:
                    return "user"
            else:
                print(colored('Password Anda salah!', 'red'))
                time.sleep(2)
                return self.main()
        except:
            print(colored('Maaf data tidak tersedia!', 'yellow'))
            time.sleep(2)
            self.main()

    def showAll(self):
        print(colored('[+] DAFTAR ACTION FIGURE [+]\n', 'green'))

        df = pandas.read_csv(self.ACTION_FIGURE_CSV)

        print(tabulate(df, headers='keys', showindex='never', tablefmt='pretty'))

        return

    def insertData(self):
        code = input("\nMasukkan Kode : ")
        name = input("Masukkan Nama : ")
        price = input("Masukkan Harga : ")        
        stock = input("Masukkan Stok : ")
        
        data = [
            [code, name, self.formatrupiah(price), stock]
        ]

        newData = pandas.DataFrame(data)

        newData.to_csv('data.csv', index=False, mode='a', header=False)

        return

    def changeData(self):
        self.showAll()
        code = int(input("\nPilih data dengan kode : "))

        df = pandas.read_csv(self.ACTION_FIGURE_CSV)

        # select row of data based on code variable
        selectedData = df.loc[df.KODE == code]

        if selectedData.empty:
            print(colored('Data tidak ditemukan!', 'red'))
            time.sleep(2)

            return

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
            self.formatrupiah(priceInput), selectedData.values[0][2])
        df.at[index, 'STOK'] = self.coalesce(
            stockInput, selectedData.values[0][3])

        df.to_csv(self.ACTION_FIGURE_CSV, index=False)

        return

    def coalesce(self, value_one, value_two):
        if value_one == "":
            return value_two
        else:
            return value_one

    def deleteData(self):
        self.showAll()

        code = int(input("\nPilih data dengan kode : "))

        df = pandas.read_csv(self.ACTION_FIGURE_CSV)

        selectedData = df[df['KODE'] == code].index

        if selectedData.empty:
            print(colored('Data tidak ditemukan!', 'red'))
            time.sleep(2)

            return

        # if KODE row based on data frame same as code variable, delete it
        df.drop(df[df['KODE'] == code].index, inplace=True)

        # making change to csv file
        df.to_csv(self.ACTION_FIGURE_CSV, index=False)

        print(colored('Data berhasil di Hapus!', 'green'))
        time.sleep(2)
        
        return

    def transaction(self):
        self.showAll()

        code = int(input("\nPilih data dengan kode : "))

        df = pandas.read_csv(self.ACTION_FIGURE_CSV, index_col=False)

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

        amount = int(
            input('\nBerapa yang ingin dibeli (tidak boleh lebih dari stok yang ada) : '))

        if amount >= stock:
            print(colored('\nTidak boleh lebih dari stok!', 'red'))

            return
        
        priceWithOutRP = self.Regex(price)
        
        summary = priceWithOutRP * amount
        summaryRP = self.formatrupiah(summary)
        summary = colored(summaryRP,'green')

        print(f'\nTotal = {price} x {amount} = {summary}')

        print(f'Total pembayaran adalah : {summary}')

        customer_name = input('\nMasukkan nama pembeli : ')

        paid = input('\nApakah sudah selesai membayar (Y/N) : ').lower()

        if paid == 'n':
            print(colored('Pembayaran tidak dilanjutkan!', 'red'))
            time.sleep(2)

            return

        # substraction the existing stock based on stock input
        df.loc[df.KODE == code, 'STOK'] -= amount

        self.addToTransactionHistory(
            selectedData, customer_name, amount, summaryRP)

        df.to_csv(self.ACTION_FIGURE_CSV, index=False)

        print(colored('\nTerima kasih sudah membayar! ^^', 'green'))
        time.sleep(2)

        return

    def addToTransactionHistory(self, data, customer_name, quantity, total):
        # generate transaction code. random number 100000-500000 and concat with datetime today take the year
        # example = TRX28695221
        transaction_code = f"TRX{random.randint(100000, 500000)}{datetime.today().strftime('%Y')}"
        action_figure_name = data.values[0][1]
        action_figure_price = data.values[0][2]

        data = [
            [
                transaction_code, customer_name, action_figure_name,
                action_figure_price, quantity, total
            ]
        ]

        newData = pandas.DataFrame(data)

        newData.to_csv(self.TRANSACTION_HISTORY_CSV,
                    index=False, mode='a', header=False)

        return
    
    def transactionHistory(self):
        print(colored('[+] DAFTAR HISTORI TRANSAKSI [+]\n', 'green'))

        df = pandas.read_csv(self.TRANSACTION_HISTORY_CSV)

        print(tabulate(df, headers='keys', showindex='never', tablefmt='pretty'))

        return
    
    def menuList(self):
        print(colored('[====================]', 'green'))
        print(colored('[+] Menu List User [+]', 'yellow'))
        print(colored('[====================]', 'green'))
        print(colored('[1]', 'magenta'), 'Daftar Action Figure')
        print(colored('[2]', 'yellow'), 'Transaksi')
        print(colored('[99]', 'red'), 'Keluar Aplikasi')

        menu = int(input('\nMasukan menu yang ingin dipilih : '))

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
        print(colored('[6]', 'cyan'), 'Daftar Histori Transaksi')
        print(colored('[99]', 'red'), 'Keluar Aplikasi')

        menu = int(input('\nMasukan menu yang ingin dipilih : '))

        return menu
    
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

                    elif menu == 6:
                        self.cls()
                        self.transactionHistory()

                    elif menu == 99:
                        print(
                            colored("\nTerima Kasih Telah Mencoba Aplikasi Action-Figure", 'green'))
                        terminate = True

                elif role == "user":
                    menu = self.menuList()
                    if menu == 1:
                        self.cls()
                        self.showAll()
                    elif menu == 2:
                        self.cls()
                        self.transaction()

                        time.sleep(2)

                        self.cls()
                    elif menu == 99:
                        print(
                            colored("\nTerima Kasih Telah Mencoba Aplikasi Action-Figure", 'green'))
                        terminate = True

        except KeyboardInterrupt:
            print("\nSampai nanti!")


application = Application()
application.main()
