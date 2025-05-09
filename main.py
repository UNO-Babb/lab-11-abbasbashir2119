# GroceryStoreSim.py
# Name: Abbas Bashir
# Date: [05/09]
# Assignment: Lab 11 - Grocery Store Simulation

import simpy
import random

eventLog = []
waitingShoppers = []
idleTime = 0

def shopper(env, id):
    arrive = env.now
    items = random.randint(5, 20)
    shoppingTime = items // 2 + random.randint(0, 2)  # added slight fluctuation
    yield env.timeout(shoppingTime)
    waitingShoppers.append((id, items, arrive, env.now))  # (id, items, arrival, doneShopping)

def checker(env):
    global idleTime
    while True:
        if len(waitingShoppers) == 0:
            idleTime += 1
            yield env.timeout(1)
        else:
            customer = waitingShoppers.pop(0)
            items = customer[1]
            checkoutTime = items // 10 + 1
            yield env.timeout(checkoutTime)
            eventLog.append((customer[0], customer[1], customer[2], customer[3], env.now))
            # (id, items, arrival, doneShopping, doneCheckout)

def customerArrival(env):
    customerNumber = 0
    while True:
        customerNumber += 1
        env.process(shopper(env, customerNumber))
        yield env.timeout(2)  # New shopper every 2 minutes

def processResults():
    totalWait = 0
    totalShoppers = 0
    totalItems = 0
    totalShoppingTime = 0
    maxWait = 0

    for e in eventLog:
        waitTime = e[4] - e[3]  # checkoutDone - doneShopping
        shoppingTime = e[3] - e[2]  # doneShopping - arrival
        totalWait += waitTime
        totalShoppingTime += shoppingTime
        totalItems += e[1]
        totalShoppers += 1
        if waitTime > maxWait:
            maxWait = waitTime

    avgWait = totalWait / totalShoppers
    avgItems = totalItems / totalShoppers
    avgShopping = totalShoppingTime / totalShoppers

    print("Total shoppers processed:", totalShoppers)
    print("The average wait time was %.2f minutes." % avgWait)
    print("The average number of items was %.2f" % avgItems)
    print("The average shopping time was %.2f minutes." % avgShopping)
    print("The maximum wait time was %.2f minutes." % maxWait)
    print("The total idle time was %d minutes." % idleTime)

def main():
    numberCheckers = 5
    env = simpy.Environment()

    env.process(customerArrival(env))

    for i in range(numberCheckers):
        env.process(checker(env))

    env.run(until=180)  # run for 3 hours (180 minutes)

    print("\n--- Simulation Results ---")
    print("Shoppers still in queue (not checked out):", len(waitingShoppers))
    processResults()

if __name__ == '__main__':
    main()
