from tkinter import*
from tkinter import Tk, messagebox
import requests
import json
import sqlite3

pycrypto = Tk()
pycrypto.title("My Crypto Portfolio")
pycrypto.iconbitmap('favicon.ico')

con = sqlite3.connect('coin.db')
cObj=con.cursor()
cObj.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY,symbol TEXT,amount owend INTEGER,price REAl)")
con.commit()

def reset():
    for cell in pycrypto.winfo_children():
        cell.destroy()
    my_portfolio()
    app_header()
def my_portfolio():

    api_requests = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=dc2a5c0a-4209-4baa-9364-f84862921e69")
    api=json.loads(api_requests.content)

    cObj.execute("SELECT*FROM coin")
    coins = cObj.fetchall()
    def font_colour(amount):
        if amount>=0:
            return "green"
        else:
            return "red"

    def insert_coin():
        cObj.execute("INSERT INTO coin(symbol,price,amount)VALUES(?,?,?)",(symbol_text.get(),price_text.get(),amount_text.get()))
        con.commit()

        messagebox.showinfo("Portfolio Notification","Coin Added To Portfolio Successfully!")
        reset()
    def update_coin():
        cObj.execute("UPDATE coin SET symbol=?,price=?,amount=? WHERE id=?",(symbol_update.get(),price_update.get(),amount_update.get(),portid_update.get()))
        con.commit()
        messagebox.showinfo("Portfolio Notification","Coin Updated Successfully!")

        reset()
    def delete_coin():
        cObj.execute("DELETE FROM coin WHERE id=?",(portid_delete.get(),))
        con.commit()
        messagebox.showinfo("Portfolio Notification","Coin Deleted From Portfolio")
        reset()
   
    total_pl = 0 
    row_coin = 1  
    total_current_value = 0
    total_amount_paid = 0
    for i in range(0,300):
        for coin in coins:
            if api["data"][i]["symbol"] == coin[1]:
                total_paid= coin[2]*coin[3]
                current_value = coin[2]*api["data"][i]["quote"]["USD"]["price"]
                pl_percoin = api["data"][i]["quote"]["USD"]["price"]-coin[3]
                total_pl_coin = pl_percoin*coin[2]
                total_pl+=total_pl_coin
                total_current_value+=current_value
                total_amount_paid+=total_paid

                ##print(api["data"][i]["name"] + "-" + api["data"][i]["symbol"])
                ##print("price-${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]))
                ##print("Number of coin:",coin[2])
               
                portfolio_id= Label(pycrypto,text = coin[0],bg="#F3F4F6",fg="black")
                portfolio_id.grid(row=row_coin,column=0,sticky=S+W)
                name = Label(pycrypto,text = api["data"][i]["symbol"],bg="#F3F4F6",fg="black")
                name.grid(row=row_coin,column=1,sticky=S+W)

                price = Label(pycrypto,text = "${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]),bg="#F3F4F6",fg="black")
                price.grid(row=row_coin,column=2,sticky=S+W)

                no_coins= Label(pycrypto,text = coin[2],bg="#F3F4F6",fg="black")
                no_coins.grid(row=row_coin,column=3,sticky=S+W)

                amount_paid= Label(pycrypto,text = "${0:.2f}".format(total_paid),bg="#F3F4F6",fg="black")
                amount_paid.grid(row=row_coin,column=4,sticky=S+W)

                current_val= Label(pycrypto,text = "${0:.2f}".format(current_value),bg="#F3F4F6",fg="black")
                current_val.grid(row=row_coin,column=5,sticky=S+W)

                pl_coin= Label(pycrypto,text = "${0:.2f}".format(pl_percoin),bg="#F3F4F6",fg=font_colour(float("{0:.2f}".format(pl_percoin))))
                pl_coin.grid(row=row_coin,column=6,sticky=S+W)

                totalpl = Label(pycrypto,text = "${0:2f}".format(total_pl_coin),bg="#F3F4F6",fg=font_colour(float("{0:.2f}".format(total_pl_coin))))
                totalpl.grid(row=row_coin,column=7,sticky=S+W)

                row_coin+=1
    
    #insert data
    symbol_text = Entry(pycrypto,borderwidth=2,relief = "groove")
    symbol_text.grid(row=row_coin+1,column=1)
    price_text = Entry(pycrypto,borderwidth=2,relief = "groove")
    price_text.grid(row=row_coin+1,column=2)
    amount_text = Entry(pycrypto,borderwidth=2,relief = "groove")
    amount_text.grid(row=row_coin+1,column=3)
    add_coin = Button(pycrypto,text = "ADD COIN",command=insert_coin,bg="#F3F4F6",fg="red")
    add_coin.grid(row=row_coin+1,column=4,sticky=S+W)

    #update coin
    portid_update = Entry(pycrypto,borderwidth=2,relief = "groove")
    portid_update.grid(row=row_coin+2,column=0)
    symbol_update = Entry(pycrypto,borderwidth=2,relief = "groove")
    symbol_update.grid(row=row_coin+2,column=1)
    price_update= Entry(pycrypto,borderwidth=2,relief = "groove")
    price_update.grid(row=row_coin+2,column=2)
    amount_update = Entry(pycrypto,borderwidth=2,relief = "groove")
    amount_update.grid(row=row_coin+2,column=3)

    update_coin_text = Button(pycrypto,text = "UPDATE COIN",command=update_coin,bg="#F3F4F6",fg="red")
    update_coin_text.grid(row=row_coin+2,column=4,sticky=S+W)
    #delete coin
    portid_delete = Entry(pycrypto,borderwidth=2,relief = "groove")
    portid_delete.grid(row=row_coin+3,column=0)
    delete_coin_text= Button(pycrypto,text = "DELETE COIN",command=delete_coin,bg="#F3F4F6",fg="red")
    delete_coin_text.grid(row=row_coin+3,column=4)
    

    totalpl = Label(pycrypto,text = "${0:2f}".format(total_pl),bg="#F3F4F6",fg=font_colour(float("{0:.2f}".format(total_pl))))
    totalpl.grid(row=row_coin,column=7,sticky=S+W)
    totalap = Label(pycrypto,text = "${0:2f}".format(total_amount_paid),bg="#F3F4F6",fg="black")
    totalap.grid(row=row_coin,column=4,sticky=S+W)
    totalcv = Label(pycrypto,text = "${0:2f}".format(total_current_value),bg="#F3F4F6",fg="black")
    totalcv.grid(row=row_coin,column=5,sticky=S+W)
    api = ""
   
    refresh = Button(pycrypto,text = "refresh",bg="#F3F4F6",fg="red",command=reset)
    refresh.grid(row=row_coin+1,column=7,sticky=S+W)
    
def app_header():
    portfolioid = Label(pycrypto,text = "Portfolio ID",bg="#142E54",fg="white",font="Lato 12",padx ="5",pady="5",borderwidth=2,relief="groove")
    portfolioid.grid(row=0,column=0,sticky=S+W)

    name = Label(pycrypto,text = "coin name",bg="#142E54",fg="white",font="Lato 12",padx ="5",pady="5",borderwidth=2,relief="groove")
    name.grid(row=0,column=1,sticky=S+W)

    price = Label(pycrypto,text = "Price",bg="#142E54",fg="white",font="Lato 12",padx ="5",pady="5",borderwidth=2,relief="groove")
    price.grid(row=0,column=2,sticky=S+W)

    no_coins= Label(pycrypto,text = "Coin Owend",bg="#142E54",fg="white",font="Lato 12",padx ="5",pady="5",borderwidth=2,relief="groove")
    no_coins.grid(row=0,column=3,sticky=S+W)

    amount_paid= Label(pycrypto,text = "Total amount paid",bg="#142E54",fg="white",font="Lato 12",padx ="5",pady="5",borderwidth=2,relief="groove")
    amount_paid.grid(row=0,column=4,sticky=S+W)

    current_val= Label(pycrypto,text = "Current Value",bg="#142E54",fg="white",font="Lato 12",padx ="5",pady="5",borderwidth=2,relief="groove")
    current_val.grid(row=0,column=5,sticky=S+W)

    pl_coin= Label(pycrypto,text = "P/L Per Coin",bg="#142E54",fg="white",font="Lato 12",padx ="5",pady="5",borderwidth=2,relief="groove")
    pl_coin.grid(row=0,column=6,sticky=S+W)

    totalpl = Label(pycrypto,text = "Total P/L with coin",bg="#142E54",fg="white",font="Lato 12",padx ="5",pady="5",borderwidth=2,relief="groove")
    totalpl.grid(row=0,column=7,sticky=S+W)
app_header()
my_portfolio()
pycrypto.mainloop()
print("End programe")
cObj.close()
con.close()

#pyinstaller --onefile --windowed --icon=favicon.ico main.py
#command for converting py file to exe

        

