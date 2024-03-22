import argparse
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument('-d', '--driver_discount', type = float, help = 'float; discount for drivers range (0, infinity], although SRC definitely will never have the amount of money to satisfy the upper bound; default is 0 (no discount)', default = 0)
parser.add_argument('-n', '--n_drivers', type = int, help = 'int; number of drivers; default = 0', default = 0)
parser.add_argument('-p', '--profit_margin', type = float, help = 'float; amount of revenue left over from race registration from ticket sales; default is 0', default = 0)
parser.add_argument('-r', '--runsignup', type = bool, help = 'boolean; is the race registration through run signup? True/False; default = True', default = True)
parser.add_argument('-s', '--sales_tax', type = int, help = 'int; estimated sales tax for one transaction; default = 5', default = 5)
parser.add_argument('race_cost_pperson', type = float, help = 'float; base cost of signing up one person for the race--not accounting for processing fees or sales tax')
parser.add_argument('n_people', type = int, help = 'int; number of people (including drivers) signed up for the race')
parser.add_argument('amount_allocated', type = float, help = 'float; the amount of money allocated for the race by USG')

args = parser.parse_args()

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
        # ##############################################
        # print(j)
        # ##############################################
        race_cost_transactions = []
        if n_people % max_people_for_runsignup == 0:
            for i in range (0, j):
                race_cost_transactions.append(race_cost_pperson * max_people_for_runsignup)
                race_cost_transactions[i] = race_cost_transactions[i] + runsignup_processing_fee(race_cost_transactions[i]) + sales_tax
        else:
            for i in range(0, j):
                # ##############################################
                # print(i)
                # print('what')
                # ##############################################
                if i < j - 1:
                    race_cost_transactions.append(race_cost_pperson * max_people_for_runsignup)
                    race_cost_transactions[i] = race_cost_transactions[i] + runsignup_processing_fee(race_cost_transactions[i]) + sales_tax
                    # ##############################################
                    # print(race_cost_transactions)
                    # print('hi')
                    # ##############################################
                else:
                    race_cost_transactions.append(race_cost_pperson * (n_people % max_people_for_runsignup))
                    race_cost_transactions[i] = race_cost_transactions[i] + runsignup_processing_fee(race_cost_transactions[i]) + sales_tax
        #             ##############################################
        #             print(race_cost_transactions)
        #             print('bye')
        #             ##############################################
        # ##############################################
        # print(race_cost_transactions)
        # ##############################################
        race_cost = sum(race_cost_transactions)
    else:
        race_cost = race_cost_pperson * n_people
    return race_cost

def discount_cost_per_person(race_cost_pperson, n_people, amount_allocated, driver_discount = 0, n_drivers = 0, runsignup = True, profit = 0, sales_tax = 5):
    cost_not_covered_by_funding = race_cost(race_cost_pperson, n_people, runsignup, sales_tax) - amount_allocated
    total_race_cost = race_cost(race_cost_pperson, n_people, runsignup, sales_tax)
    if profit == 0:
        cost_not_covered_by_funding = cost_not_covered_by_funding
    else:
        cost_not_covered_by_funding += profit
    
    if driver_discount == 0:
        cost_pperson = cost_not_covered_by_funding / n_people
        adj_cost_pperson = (cost_pperson + 0.3) / 0.971
        return adj_cost_pperson, adj_cost_pperson, total_race_cost
    else:
        cost_pnondriver = (((cost_not_covered_by_funding + n_drivers * ((driver_discount))) / n_people) + 0.3) / 0.971
        cost_pdriver = cost_pnondriver - driver_discount
        return cost_pnondriver, cost_pdriver, total_race_cost

adj_cost_pnondriver, adj_cost_pdriver, total_race_cost = discount_cost_per_person(race_cost_pperson = args.race_cost_pperson, n_people = args.n_people, amount_allocated = args.amount_allocated, driver_discount = args.driver_discount, n_drivers = args.n_drivers, runsignup = args.runsignup, profit = args.profit_margin, sales_tax = args.sales_tax)

print('\n')
print('The estimated total cost of the race registration is $' + str(float(np.round(total_race_cost, 2))) + ', which includes an estimated sales tax of $' + str(args.sales_tax) + ' per transaction and processing fees.\n')
print('Given that the cost per person registered for this race is $' + str(float(np.round(args.race_cost_pperson, 2))) + ', there are ' + str(args.n_people) + ' people to register, we received $' + str(args.amount_allocated) + ' from USG, and we want to make a $' + str(args.profit_margin) + ' profit:')
print('Non-drivers need to pay ~$' + str(float(np.round(adj_cost_pnondriver, 2))) + ', and drivers need to pay ~$' + str(float(np.round(adj_cost_pdriver, 2))) + ', which is a $' + str(args.driver_discount) + ' discount for drivers.')
print('This is an estimated overall discount of {:.0%}'.format(1 - (adj_cost_pnondriver / args.race_cost_pperson)) + ' for non-drivers and {:.0%}'.format(1 - (adj_cost_pdriver / args.race_cost_pperson)) + ' for drivers.\n')
