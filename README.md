# SRC_RCC
Race cost calculator for the Spartan Running Club @ CWRU

## What do it do?
The Race Cost Calculator (RCC) is tailored to calculate race expenses for the Spartan Running Club @ CWRU. It is mostly made for calculating Run Signup race registration as it can (relatively) accurately take into account [Run Signups's specific processing fee calculations](https://info.runsignup.com/pricing/) and [Campus Groups's Stripe processing fee of 2.9% + $0.3 per transaction](https://case.edu/studentlife/services/campusgroups/online-payments). It can also factor in a price difference between drivers and non-drivers if a driver discount is offered. Additionally, a desired profit can be specified if extra money for the club is needed for something, like merch or an extra bonding event for example. 

The main use of the calculator is estimating the cost group members have to pay in order for SRC to register everybody for the race! This previously tedious, stress-inducing, and confusing calculation has now been greatly simplified and streamlined through advances in complex mathematics ~~elementary school algebra~~ and computer science ~~introductory python~~ by yours truly to take the guesswork and headache out of the SRC treasurer's job.

## Hurry up and tell me how to use it--I need to go for a run
Okay, Pheidippides, gosh I'll tell you how--it'll only take a minute or two. That's like nothing compared to the amount of time it takes to run the (first ever) marathon...

You'll need to download the `argparse` and `numpy` packages using your favorite installer. (Mine is `pip`.)
```
Usage: python RCC.py [options] race_cost_pperson n_people amount_allocated

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

Note: choosing False for [-r, --runsignup] simply results in not taking into account Run Signups's processing fee calculation linked earlier. 
```

## Make sure to look both ways when crossing the street, or else the days-without-almost-being-hit-by-a-car counter might go to 0 (again)
There are many assumptions that RCC uses when calculating all the costs. Run Signup usually caps the amount of people you can register in a single transaction at 25. This is hard-coded into the script so that if you have >25 people you need to register, the calculator will account for the fact that you will need to do two separate transactions. I haven't found a good way to estimate the sales tax yet, which is why the default value for sales tax is at $5 per transaction (not per person). Run Signup seems to have absrudly low sales tax values (usually around ~0.5%), which is kinda odd but whatever. Also, [Run Signups's processing fee calculation](https://info.runsignup.com/pricing/), for some reason, is actually usually a few cents too low compared to when you actually try to register people and see the processing fee charge. To account for this, I simply added an extra dollar to the processing fee calculation. So instead of the processing fee being '4% of the cart total + $1' as is listed in the link for cart totals >$1000, RCC uses '4% of the cart total + $2' to account for the observed discrepancy noted previously. Who knows if it's a good assumption though. In general though, the calculator for these two reasons usually overestimates the amount that people need to pay--but also it's better to have money left over than to be blacklisted by USG for overspending. The math I did that adjusts for the stripe processing fee in the final recommended payment SRC should charge per person is also kinda sketch because I did it at like 4am, but it's a resonable estimate. If anything, I recommended to just round the RCC's recommended payment value up to the nearest dollar--that's like less than the cost of a single running gel.