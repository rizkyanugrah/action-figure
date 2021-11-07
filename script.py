def register(name,password):
    file = open('action-figure/akun.csv','a')
    file.write(f"{name},{password}")

def access(option):
    if (option == "login"):
        username = input("masukan ussername anda : ")
        password = input("masukan password anda : ")
        login(username,password)
    else:
        print("masukan username yang ingin anda tambahkan! ")
        username = input("masukan username : ")
        password = input('masukan password : ')
        register(username,password) 
        print("sukses, silahakan login >_<")
        access("login")
        
def login(name,password):
    login = False
    file = open ("action-figure/akun.csv","r")
    for i in file:
        print()
        a,b = i.split(",")
        b = b.strip()
        if(a==name and b==password):
            login = True
            break
    file.close()
    if(login == True):
        print("sukses, silahkan masuk")

def start():
    print("Silahkan login jika sudah punya akun")
    print("Silahkan register jika anda belum memiliki akun")

    option = input( "(Login/register) : ")

    if(option!="login" and option!="register"):
        start()
    else:
        access(option)


start()