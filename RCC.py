import pandas as pd
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("path")

args = parser.parse_args()
group = parser.add_mutually_exclusive_group()

parser.add_argument('race_cost_pperson', help = 'int; base cost of signing up one person for the race--not accounting for processing fees or sales tax')
parser.add_argument('n_people', help = 'int; number of people (including drivers) signed up for the race')
parser.add_argument('amount_allocated', help = 'int; the amount of money allocated for the race by USG')
parser.add_argument('-dd', '--driver_discount', help = 'boolean; will there be a discount for drivers? True/False', action = 'store_true') # might be optional
# parser.add_argument('')

def ceildiv(a, b):
    return -(a // -b)

def runsignup_processing_fee(race_cost):
    if race_cost == 0:
        rsu_processing_fee = 0
    elif 0 < race_cost < 250:
        rsu_processing_fee = (race_cost * 0.06) + 2
    elif 250 <= race_cost < 1000:
        rsu_processing_fee = (race_cost * 0.05) + 2
    else:
        rsu_processing_fee = (race_cost * 0.04) + 2
    return rsu_processing_fee

def race_cost(race_cost_pperson, n_people, runsignup, sales_tax):
    max_people_for_runsignup = 25
    if runsignup == True:
        j = ceildiv(n_people, max_people_for_runsignup)
        print(j)
        race_cost_transactions = []
        for i in range(0, j):
            if i < j - 1:
                race_cost_transactions.append(race_cost_pperson * max_people_for_runsignup)
                race_cost_transactions[i] = race_cost_transactions[i] + runsignup_processing_fee(race_cost_transactions[i]) + sales_tax
                print(race_cost_transactions)
            else:
                print(n_people % max_people_for_runsignup)
                race_cost_transactions.append(race_cost_pperson * (n_people % max_people_for_runsignup))
                print(race_cost_transactions)
                race_cost_transactions[i] = race_cost_transactions[i] + runsignup_processing_fee(race_cost_transactions[i]) + sales_tax
                print(race_cost_transactions)
        race_cost = sum(race_cost_transactions)
    else:
        race_cost = race_cost_pperson * n_people
    return race_cost

def discount_cost_per_person(race_cost_pperson, n_people, amount_allocated, bool_driver_discount = False, driver_discount = 0, n_drivers = 0, runsignup = True, profit = False, profit_margin = 0, sales_tax = 5):
    cost_not_covered_by_funding = race_cost(race_cost_pperson, n_people, runsignup, sales_tax) - amount_allocated
    print(race_cost(race_cost_pperson, n_people, runsignup, sales_tax))
    if profit == False:
        cost_not_covered_by_funding = cost_not_covered_by_funding
    else:
        cost_not_covered_by_funding += profit_margin
    
    if bool_driver_discount == False:
        cost_pperson = cost_not_covered_by_funding / n_people
        adj_cost_pperson = (cost_pperson + 0.3) / 0.971
        return adj_cost_pperson, adj_cost_pperson
    else:
        cost_pnondriver = (((cost_not_covered_by_funding + n_drivers * ((driver_discount))) / n_people) + 0.3) / 0.971
        cost_pdriver = cost_pnondriver - driver_discount
        return cost_pnondriver, cost_pdriver

adj_cost_pnondriver, adj_cost_pdriver = discount_cost_per_person(race_cost_pperson = 35, n_people = 30, amount_allocated = 703.5, bool_driver_discount = True, driver_discount = 5, n_drivers = 7, runsignup = True, profit = True, profit_margin = 100)

print(adj_cost_pnondriver, adj_cost_pdriver)

