from DCF import *
from tkinter import *

HEIGHT = 800
WIDTH = 600


def calc_dcf(ticker_and_name):
    name, ticker = split_ticker_name(ticker_and_name)

    print("https://www.macrotrends.net/stocks/charts/{}/{}/free-cash-flow".format(ticker, name))
    entry.delete(0, END)

    label1['text'] = name.upper()
    cashflow, inter_beta, total = DCF(ticker, name)
    calc_cashflow(cashflow)
    calc_interest_expense_betadata(inter_beta)
    calc_total_dcf(total)


def split_ticker_name(ticker_and_name):
    ticker_and_name = ticker_and_name.split(",")
    ticker = ticker_and_name[0].strip()
    name = ticker_and_name[1].strip()
    return name, ticker


def calc_cashflow(cashflow):
    by_date = "Past free cash flows:\n"
    for year, flow in cashflow.items():
        by_date += (str(year) + ": " + str(flow) + "\n")

    label2['text'] = by_date


def calc_interest_expense_betadata(inter_beta):
    # heading, price, shares, beta, debt_res, equity_res = interest_expense_betadata(ticker, name)
    # label3['text'] = heading + "\n" + price + "\n" + shares + "\n" + beta + "\n" + debt_res + "\n" + equity_res

    info = inter_beta.replace(",", "\n")
    label3['text'] = info


def calc_total_dcf(total):
    info = total.replace(",", "\n")
    label4['text'] = info


root = Tk()

canvas = Canvas(root, height=HEIGHT, width=WIDTH).pack()

background_image = PhotoImage(file='money3.png')
background_label = Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

frame = Frame(root, bg='#615f57', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

entry = Entry(frame, font=40)
entry.place(relwidth=0.65, relheight=1)

button = Button(frame, text="Enter: ticker, name", font=('Ariel', 10), command=lambda: calc_dcf(entry.get()))
button.place(relx=0.7, relwidth=0.3, relheight=1)

lower_frame = Frame(root, bg='#615f57', bd=5)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

label1 = Label(lower_frame, font=('Ariel', 16, 'bold'), anchor='nw', justify='left', pady=10)
label1.pack(fill=BOTH)
label2 = Label(lower_frame, font=('Ariel', 13), anchor='nw', justify='left', fg='#615f57')
label2.pack(fill=BOTH, expand='true', side='left')

label3 = Label(lower_frame, font=('Ariel', 13), anchor='nw', justify='left', fg='#615f57')
label3.pack(fill=BOTH, expand='true')

label4 = Label(lower_frame, font=('Ariel', 13), anchor='nw', justify='left', fg='#615f57')
label4.pack(fill=BOTH, expand='true')

root.mainloop()
