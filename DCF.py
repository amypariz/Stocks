import numpy as np
import pandas as pd
from numpy.random import randn
import webbrowser
from urllib import request
from urllib.request import Request, urlopen


# those functions check if there is a M sign or a B in the input, its probably possible to join them.

def charcov3(word):
    num = ''
    for char in word:
        num += char
        if char == 'M':
            return float(num[:-1])
            break
        elif char == 'B':
            num2 = float(num[:-1]) * 1000
            return num2
            break


def charcov2(word):
    num = ''
    for char in word:
        num += char
        if char == 'M':
            return num
            break
        elif char == 'B':
            num2 = float(num[1:-1]) * 1000
            return num2
            break


def charcov(word):
    num = ''
    if "$" in word:
        for char in word:
            num += char
            if char == 'M':
                return num
                break
            elif char == 'B':
                num2 = float(num[1:-1]) * 1000
                return num2
                break


# goes to MacroTrends webside using the ticker and the name of the stock, takes the url, finds the current long term debt of the company.

def debt_equity_func(ticker1, name1):
    debt_equity1 = []
    num = ''
    de_response = request.urlopen(
        'https://www.macrotrends.net/stocks/charts/{}/{}/debt-equity-ratio'.format(ticker1, name1))
    de_page_source = de_response.read().decode('utf-8')
    de_parts = de_page_source.split('<th style="text-align:center;">')
    # print(de_parts)
    for de_part in de_parts:
        if 'Debt to Equity Ratio</th>' in de_part:
            de_part2 = de_part.split('<td style="text-align:center;">')
            for de_part3 in de_part2:
                debt_equity1.append(charcov(de_part3))
    return debt_equity1


# cuts the html tags from the results in the Cashflows Dictionary, leaves just a number(float).
def cash(word):
    numb = ''
    for char in word:
        if char == ',':
            continue
        numb += char
        if char == '<':
            break
    return float(numb[0:-1])


# gets a ticker, goes to MarketWatch website (financials page), takes the url, cuts the tags and finds
# the Interest Expense number. (still includs a charcov function for some reason...)

def interest_expence_func(word):
    exp_response = request.urlopen('https://www.marketwatch.com/investing/stock/{}/financials'.format(word).lower())
    exp_page_source = exp_response.read().decode('utf-8')
    expence_parts = exp_page_source.split(
        '<td class="rowTitle"><a href="#" data-ref="ratio_InterestExpenseGrowth"><span class="expand"></span></a>')
    num = ''
    for exp_part in expence_parts:
        if 'Interest Expense' in exp_part:
            exp_part2 = exp_part.split('</td><td class="miniGraphCell">')
            int_exp = exp_part2[0]
            for char in int_exp[-1::-1]:
                num += char
                if char == '>':
                    break
            num2 = num[:-1]
            if num2[:1] == 'M':
                num3 = num2[1:]
                return float(num3[::-1])
            elif num2[:1] == 'B':
                num3 = num2[1:]
                num4 = float(num3[::-1]) * 1000
                return num4


# gets a ticker, goes to MarketWatch website (again, main page), takes the url, cuts the tags and
# finds the Beta(the volatility of the stock compared to the rest of the stock market)
# the opening price of the last trading session (condition in the code with the tag '</small>'
# because there are other names in the page starting with the word open....
# and finds the number of Shares Outstanding (ownership parts of the company).
# returns a tuple.

def betadata(word):
    num = ''
    num3 = ''
    num5 = ''
    beta_response = request.urlopen('https://www.marketwatch.com/investing/stock/{}'.format(word))
    beta_page_source = beta_response.read().decode('utf-8')
    beta_parts = beta_page_source.split('<small class="label">')
    # print(expence_parts)
    for beta_part in beta_parts:
        if 'Beta' in beta_part:
            beta_part2 = beta_part.split('</span>')
            beta = beta_part2[0]
            for char in beta[::-1]:
                num += char
                if char == '>':
                    break
            num2 = num[:-1]
            # print(float(num2[::-1]))
        elif 'Open</small>' in beta_part:
            open_part2 = beta_part.split('</span>')
            open = open_part2[0]
            # print(open)
            for char in open[::-1]:
                num3 += char
                if char == '>':
                    break
            # print(num3)
            if num3[3:-2].isnumeric():
                num4 = num3[:-2]
            # print(float(num4[::-1]))
        if 'Shares Outstanding' in beta_part:
            shares_part2 = beta_part.split('</span>')
            shares = shares_part2[0]
            for char in shares[::-1]:
                num5 += char
                if char == '>':
                    break
            # num6 = num5[:-1]
            # print(float(num6[::-1]))
            if num5[:1] == 'M':
                num6 = num5[1:-1]
                num7 = float(num6[::-1])
                # print(num7)
            elif num5[:1] == 'B':
                num6 = num5[1:-1]
                num7 = float(num6[::-1]) * 1000
                # print(num7)
    data = (('price:', float(num4[::-1])), ('shares:', num7), ('beta:', float(num2[::-1])))
    return data


# gets the beta of the stock (volatility of risk for the investor) and calculates the return
# that the investor would like get in return for his investment (COE - cost of equity - equity: the
# money investend in the company)

def coe_func(beta1):
    coe1 = 0.03 + beta1 * 0.07
    return coe1


# WACC - weighted average cost of capital, makes an average of the COE and Interest expence (cost of debt).
# part of the DCF calculation

def wacc_func(debt2, equity2, interest_expence2, coe2):
    if interest_expence2 is None:
        wacc2 = (equity2 / (debt2 + equity2)) * coe2
    else:
        print(interest_expence2)
        wacc2 = ((debt2 * 0.85) / (debt2 + equity2)) * (interest_expence2 / debt2) + (
                equity2 / (debt2 + equity2)) * coe2
    return wacc2


# gets the Dictionary of the cashflows and calculates the annual growth in the last five years.
# part of the DCF calculation

def CGAR_fanc(dic):
    count = 0
    growth = 0
    # for i in range(2010,2019):
    # growth += (dic[i+1] - dic[i]) / dic[i]
    # count += 1
    # cgar = growth / count
    cgar = ((((dic[2019] - dic[2015]) / dic[2015]) + 1) ** 0.2) - 1
    return cgar


# gets the calculations of WACC and CGAR. also gets the cashflow of 2019 from the Dictionary
# calculates the worth of the future cash the company will make in the present (there is a risk that the company will fail making the cash).

def DCF5_func(cgar2, wacc2, flow):
    total = 0
    if wacc2 < 0.05:
        wacc2 = 0.06
    if cgar2 > 0.05 and cgar2 < 0.25:
        for i in range(1, 6):
            total += (flow * ((1 + cgar2 * 0.95) ** i) / (1 + wacc2) ** i)
    if cgar2 > 0.25:
        for i in range(1, 6):
            total += (flow * ((1 + cgar2 * 0.92) ** i)) / ((1 + wacc2) ** i)
    else:
        for i in range(1, 6):
            total += (flow * ((1 + cgar2) ** i) / (1 + wacc2) ** i)
    total += ((flow * ((1 + cgar2 * 0.75) ** 5)) / (wacc2 - (wacc2 / 2))) / ((1 + wacc2) ** 5)
    return total


# p/e model (P/E - price of the stock diveded by the ernings per share) this function gets ticker and name.
# goes to macrotrends website and gets the url, cuts the tags and gets the past P/E ratios in the last
# 5 years, then makes an average for all the numbers and returns it.

def past_pe_func(ticker1, name1):
    past_pe = []
    sum = 0
    count = 0
    ppe_response = request.urlopen('https://www.macrotrends.net/stocks/charts/{}/{}/pe-ratio'.format(ticker1, name1))
    ppe_page_source = ppe_response.read().decode('utf-8')
    ppe_parts = ppe_page_source.split('<th style="text-align:center;">')
    # print(de_parts)
    for ppe_part in ppe_parts:
        if 'PE Ratio</th>' in ppe_part:
            ppe_part2 = ppe_part.split('<td style="text-align:center;">')
            for ppe_part3 in ppe_part2[1:]:
                ppe_part4 = ppe_part3.split('</td>')
                past_pe.append(ppe_part4[0])
    #              past_pe.append(charcov2(ppe_part3))
    for i in range(3, (past_pe.index(past_pe[-1])), 4):
        if float(past_pe[i]) == 0:
            continue
        # print(float(past_pe[i]))
        sum += float(past_pe[i])
        count += 1
    average = sum / count
    print('Average {} P/E:{}'.format(name, average))
    return average


# another tags cutting function.

def finviz_data_func(pe_part5):
    num = ''
    pe_part2 = pe_part5.split('</span>')
    pe_part3 = pe_part2[0].split('</b>')
    pe_part4 = pe_part3[0]
    # print(pe_part4)
    for char in pe_part4[::-1]:
        num += char
        if char == '>':
            break
    num2 = num[::-1]
    # print(num2[1:])
    return num2[1:]


# this func gets a ticker and goes to Finviz website, gets the url and finds the numbers of the current
# P/E ratio, EPS (earnings per share), market capitalization (the price of each stock (share) times the
# number of Shares Outstanding. also known as the price of the whole company today)

def ticker_search(tick):
    pe_response = Request('https://finviz.com/quote.ashx?t={}'.format(tick), headers={'User-Agent': 'Mozilla/5.0'})
    pe_page_source = urlopen(pe_response).read().decode('utf-8')
    pe_parts = pe_page_source.split('offsetx=[10] offsety=[20] delay=[300]"')

    for pe_part in pe_parts:
        if '>P/E</td>' in pe_part:
            pe = finviz_data_func(pe_part)
        elif '>EPS (ttm)</td>' in pe_part:
            eps = finviz_data_func(pe_part)
        elif '>Market Cap</td>' in pe_part:
            mcap = finviz_data_func(pe_part)
    return (pe, eps, mcap)


# gets the P/E of all the compatitors and makes a weighted average (gives more weight to companies with a close
# market capitalization) returns the weighted average.

def WAPE_calculator(data, mcap1):
    sum = 0
    count = 0
    company_mcap = charcov3(mcap1)
    for company in data:
        mcap = charcov3(company[1][2])
        if company[1][0] == '-':
            continue
        if mcap * 5 > company_mcap and mcap * 0.2 < company_mcap:
            sum += mcap * float(company[1][0]) * 50
            count += mcap * 50
        else:
            sum += mcap * float(company[1][0])
            count += mcap
    print("weighted average P/E of competitors:{}".format(sum / count))
    return sum / count


def DCF(ticker, name):
    def calc_cashflow(ticker, name):
        global cashflows
        ticker = ticker.upper()
        name = name.lower()
        response = request.urlopen(
            "https://www.macrotrends.net/stocks/charts/{}/{}/free-cash-flow".format(ticker, name))
        cashflows = {}
        page_source = response.read().decode('utf-8')
        parts = page_source.split('<tr>')
        for part in parts:
            mini = part.split('>')
            for nimi in mini:
                ano = nimi.split('<')
                for year in range(2010, 2020):
                    if str(year) in ano:
                        date = int(ano[0])
                        data = part.split('<td style="text-align:center">')
                        num = cash(data[2])
                        cashflows[date] = num
        # return cashflows

    def interest_expense_betadata(ticker, name):
        global interest_expence
        global BetaPriceShares
        global debt
        global equity

        interest_expence = interest_expence_func(ticker)
        # print("Interest Expense for 2019: {}".format(interest_expence))
        heading = "Interest Expense for 2019: " + str(interest_expence)
        BetaPriceShares = betadata(ticker)  # TODO: prints a number in the function
        price = name + " " + str(BetaPriceShares[0][0]) + " " + str(BetaPriceShares[0][1])
        shares = name + " " + str(BetaPriceShares[1][0]) + " " + str(BetaPriceShares[1][1])
        beta = name + " " + str(BetaPriceShares[2][0]) + " " + str(BetaPriceShares[2][1])

        debt_equity = debt_equity_func(ticker, name)
        debt = float(debt_equity[2])
        # equity = float(debt_equity[3])
        equity = (BetaPriceShares[0][1] * BetaPriceShares[1][1]) - debt
        debt_res = name + " debt: " + str(debt)
        equity_res = name + " equity: " + str(equity)
        result = str(heading) + "," + str(price) + "," + str(shares) + "," + str(beta) + "," + str(
            debt_res) + "," + str(equity_res)
        return result

    def total_dcf(name):
        coe = coe_func(BetaPriceShares[2][1])
        coe_res = name + " coe: " + str(coe)
        wacc = wacc_func(debt, equity, interest_expence, coe)
        wacc_res = name + " wacc: " + str(wacc)
        CGAR = CGAR_fanc(cashflows)
        cgar_res = name + " CGAR: " + str(CGAR)
        DCF5 = DCF5_func(CGAR, wacc, cashflows[2019])
        dcf5_res = name + " DCF for 5 year's CGAR growth: $" + str(DCF5) + "M"
        share_price5 = DCF5 / BetaPriceShares[1][1]
        discount = "discounted share price: $" + str(share_price5)
        result = str(coe_res) + "," + str(wacc_res) + "," + str(cgar_res) + "," + str(dcf5_res) + "," + str(discount)
        return result

    calc_cashflow(ticker, name)
    inter_beta = interest_expense_betadata(ticker, name)
    total = total_dcf(name)
    return cashflows, inter_beta, total

#
##########################################################################################
# body(DCF)
#
# print("please enter ticker:")
# ticker = input(str().upper)
# print("please enter name:")
# name = input(str().lower)
#
# # makes the dictionary of the cashflows and prints it.
#
# print("https://www.macrotrends.net/stocks/charts/{}/{}/free-cash-flow".format(ticker, name))
# response = request.urlopen("https://www.macrotrends.net/stocks/charts/{}/{}/free-cash-flow".format(ticker, name))
# # response = request.urlopen('https://www.macrotrends.net/stocks/charts/LMT/lockheed-martin/free-cash-flow')
# print("*" * 80)
# print()
# print("DCF model:")
# print()
#
# cashflows = {}
# page_source = response.read().decode('utf-8')
# parts = page_source.split('<tr>')
# for part in parts:
#     mini = part.split('>')
#     for nimi in mini:
#         ano = nimi.split('<')
#         for year in range(2010, 2020):
#             if str(year) in ano:
#                 date = int(ano[0])
#                 data = part.split('<td style="text-align:center">')
#                 num = cash(data[2])
#                 cashflows[date] = num
# print("past free cash flows:")
# print(cashflows)
#
# # calls the funcs for interest_expense, betadata.
#
# interest_expence = interest_expence_func(ticker)
# print("Interest Expence for 2019: {}".format(interest_expence))
# BetaPriceShares = betadata(ticker)
# print('{} {} {}'.format(name, BetaPriceShares[0][0], BetaPriceShares[0][1]))
# print('{} {} {}'.format(name, BetaPriceShares[1][0], BetaPriceShares[1][1]))
# print('{} {} {}'.format(name, BetaPriceShares[2][0], BetaPriceShares[2][1]))
# debt_equity = debt_equity_func(ticker, name)
# debt = float(debt_equity[2])
# # equity = float(debt_equity[3])
# equity = (BetaPriceShares[0][1] * BetaPriceShares[1][1]) - debt
# print("{} debt: {}".format(name, debt))
# print("{} equity: {}".format(name, equity))
#
# # calls the calculation funcs
#
#
# coe = coe_func(BetaPriceShares[2][1])
# print("{} coe: {}".format(name, coe))
# wacc = wacc_func(debt, equity, interest_expence, coe)
# print("{} wacc: {}".format(name, wacc))
# CGAR = CGAR_fanc(cashflows)
# print("{} CGAR: {}".format(name, CGAR))
# DCF5 = DCF5_func(CGAR, wacc, cashflows[2019])
# print("{} DCF for 5 year's CGAR growth: ${}M".format(name, DCF5))
# share_price5 = DCF5 / BetaPriceShares[1][1]
# print("discounted share price: ${}".format(share_price5))
# # df = pd.DataFrame.from_dict(cashflows)
# # print(df)
# print("*" * 80)
# print()
#
# # body (P/E)
# print("P/E model:")
# print()
# sec_data = []
# numm = ''
#
# # calls past P/E func
#
# past_pes = past_pe_func(ticker, name)
# pe_numbers = ticker_search(ticker)
# print(pe_numbers)
# pe_response = Request('https://finviz.com/quote.ashx?t={}'.format(ticker), headers={'User-Agent': 'Mozilla/5.0'})
# pe_page_source = urlopen(pe_response).read().decode('utf-8')
#
# # finds the company's sector.
#
# pe_parts = pe_page_source.split('offsetx=[10] offsety=[20] delay=[300]">')
# comp_list = []
# comp_data_list = []
# sector_parts = pe_page_source.split('<a href="screener.ashx?v=111&f=ind_')
# sector_parts2 = sector_parts[-1].split('" class="tab-link">')
# print(sector_parts2[0])
#
# # finds compatitors
#
# sector_response = Request('https://finviz.com/screener.ashx?v=111&f=ind_{}&o=-marketcap'.format(sector_parts2[0]),
#                           headers={'User-Agent': 'Mozilla/5.0'})
# sector_page_source = urlopen(sector_response).read().decode('utf-8')
# all_sec_parts = sector_page_source.split('<a href=')
# for all_sec_parts2 in all_sec_parts:
#     if 'class="screener-link">' and '</a></td>' in all_sec_parts2:
#         all_sec_parts3 = all_sec_parts2.split('class="screener-link">')
#         for all_sec_parts4 in all_sec_parts3:
#             all_sec_parts5 = all_sec_parts4.split('</a></td>')
#             if '"screener-link-primary">' in all_sec_parts5[0]:
#                 all_sec_parts6 = all_sec_parts5[0].split('"screener-link-primary">')
#                 comp_list.append(all_sec_parts6[1])
# for competitor in comp_list:
#     comp_data_list.append([competitor, ticker_search(competitor)])
# print('ticker, (P/E,EPS,Market Cap):')
# print(comp_data_list)
#
# # calls caculating func
#
# WAPE = WAPE_calculator(comp_data_list, pe_numbers[2])
# pemodel_price = (0.7 * past_pes + 0.3 * WAPE) * float(pe_numbers[1])
# print("Estimated price by model:{}".format(pemodel_price))
# print("*" * 80)
# print()
# print(" model:")
# print()
