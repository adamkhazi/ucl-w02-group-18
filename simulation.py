from random import randint
import math
import pdb

class Simulation:
    def ortb2(self, p_ctr, base_ctr, alpha, const):
        return int(const * (math.pow((p_ctr + math.sqrt(const**2*alpha**2 + p_ctr**2))/(const*alpha), 1/3)) - math.pow(((const*alpha)/(p_ctr + math.sqrt(const**2*alpha**2 + p_ctr**2))), 1/3))

    def ortb(self, p_ctr, base_ctr, alpha, const):
        return int(math.sqrt(((const/alpha)*p_ctr) + (const*const)) - const)

    def linear_bidding(self, bid_base, p_ctr, avg_ctr):
        return int(p_ctr * bid_base/avg_ctr)

    def run(self, data, algorithm, bid_base, p_ctr, avg_ctr, alpha, c):
        bid_values=[]
        if algorithm=="linear":
            for p in p_ctr:
                p=p[1]
                new_bid=self.linear_bidding(bid_base, p, avg_ctr)
                bid_values.append(new_bid)

        elif algorithm=="constant":
            bid_values=[bid_base for i in range(data.shape[0])]

        elif algorithm=="random":
            bid_values=[randint(bid_base[0], bid_base[1]) for i in range(data.shape[0])]

        elif algorithm=="ortb":
            for pred_ctr in p_ctr:
                pred_ctr=pred_ctr[1]
                new_bid=self.ortb(pred_ctr, avg_ctr, alpha, c)
                bid_values.append(new_bid)

        elif algorithm=="ortb2":
            for pred_ctr in p_ctr:
                pred_ctr=pred_ctr[1]
                new_bid=self.ortb2(pred_ctr, avg_ctr, alpha, c)
                bid_values.append(new_bid)

        elif algorithm=="ortb-modified":
            t=0.95
            for pred_ctr in p_ctr:
                pred_ctr=pred_ctr[1]
                if pred_ctr >= t:
                    new_bid=self.ortb(pred_ctr, avg_ctr, alpha, c)
                else:
                    new_bid=0
                bid_values.append(new_bid)

        return bid_values

    def evaluate(self, data, bids_made, budget, y_val):
        clicks = 0
        cost = 0
        for index, bid_price, pay_price in data:
            if bids_made[index] >= bid_price and pay_price+cost <= budget:
                cost+=pay_price
                #if y_val[index] == 1:
                clicks+=1
            #if y_val[index] == 1:
                #print(bids_made[index], bid_price, cost)
            if cost == budget:
                break

        ctr=100.0*(float(clicks)/float(data.shape[0]))
        print("campaign cost:", cost, "clicks:", clicks)
        print("click-through rate:", ctr)
        return (clicks, cost, ctr)
