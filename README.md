# SRC_RCC
Race cost calculator for the Spartan Running Club @ CWRU.

## What do it do?
The Race Cost Calculator (RCC) is tailored to calculate race expenses for the Spartan Running Club @ CWRU. It is mostly made for calculating Run Signup race registration as it can (relatively) accurately take into account [Run Signups's specific processing fee calculations](https://info.runsignup.com/pricing/) and [Campus Groups's Stripe processing fee of 2.9% + $0.3 per transaction](https://case.edu/studentlife/services/campusgroups/online-payments).

The main use of the calculator is estimating the cost group members have to pay in order for SRC to register everybody for the race! This previously tedious, stress-inducing, and confusing calculation has now been greatly simplified and streamlined through advances in complex mathematics ~~elementary school algebra~~ and computer science ~~basic python~~ by yours truly to take the guesswork and headache out of the SRC treasurer's job.

## Hurry up and tell me how to use it--I need to go for a run
Okay, Forrest, gosh I'll tell you how--it'll only take a minute or two.

Usage: python3.6 findingsgRNAs.py [options] race_cost_pperson n_people amount_allocated

Positional arguments:
race_cost_pperson       base cost of signing up one person for the race--not accounting for processing fees or sales tax

n_people                number of people (including drivers) signed up for the race

amount_allocated        the amount of money allocated for the race by USG

Optional arguments:
-d, --driver_discount   discount for drivers range (0, infinity], although SRC definitely will never have the amount of money to satisfy the upper bound; default is 0 (no discount)
-n, --n_drivers         number of drivers; default = 0
-p, --profit_margin     amount of revenue left over from race registration from ticket sales; default is 0
-r, --runsignup         is the race registration through run signup? True/False; default = True
-s, --sales_tax         estimated sales tax for one transaction; default = $5/transaction
