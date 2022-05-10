import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib
from scipy import special


class PureAloha():

    def __init__(self, **kwargs):
   
        self.m = kwargs['m']                               # number of nodes
        self.total_arr_rate = kwargs['total_arr_rate']     # total arrival rate
        self.retrans_prob = kwargs['retrans_prob']         # retransmission probability


    def prob_a(self):                
        # Probability of transmission from unbacklogged node
        return 1 - math.exp(-self.total_arr_rate/self.m)


    def get_prob_a(self, i, n):
        # Probability of i unbacklogged notes attempt a transmission, given n as a size of a backlog
        return special.binom(self.m-n, i) * ((1-self.prob_a()) ** (self.m-n-i)) * (self.prob_a() ** i)


    def get_retrans_prob(self, i, n):
        # Probability of i backlogged notes attempt a transmission, given n as a size of a backlog
        return special.binom(n, i) * ((1-self.retrans_prob) ** (n-i)) * (self.retrans_prob ** i)


    def get_P_n_nplusi(self, n, nplusi):
        # Calculate transition probabilities
        i = nplusi - n
        if (i >= 2) and (i <= (self.m-n)):
            return self.get_prob_a(i, n)
        elif i == 1:
            return self.get_prob_a(1, n)*(1 - self.get_retrans_prob(0, n))
        elif i == 0:
            return self.get_prob_a(1, n)*self.get_retrans_prob(0, n) + \
                   self.get_prob_a(0, n)*(1 - self.get_retrans_prob(1, n))
        elif i == -1:
            return self.get_prob_a(0, n)*self.get_retrans_prob(1, n)
        else:
            return 0.0
        
        

    def get_p_n(self, n, p_values):
        # current probability
        
        assert (len(p_values) == n)  

        base0 = (1.0/self.get_P_n_nplusi(n, n-1))
        base1 = p_values[n-1] * (1 - self.get_P_n_nplusi(n-1, n-1))

        for j in range(n-1):
            base1 -= p_values[j]*self.get_P_n_nplusi(j, n-1)

        return base0*base1

    def get_p_success(self, n):
        # Probability of a successful transmission given backlog state
        return (self.get_prob_a(1, n)*self.get_retrans_prob(0, n)) + \
               (self.get_prob_a(0, n)*self.get_retrans_prob(1, n))


    def get_p_values(self):
        # normalize 
        p_0 = 0.1

        # initialize 
        p_values = [p_0]

        for i in range(1, self.m+1):
            p_values.append(self.get_p_n(i, p_values))

        # get normalized values
        p_values = [v/sum(p_values) for v in p_values]

        return p_values

    def get_G(self, n):
        v = (self.m-n)*self.prob_a() + n*self.retrans_prob        
        return v

    def get_P_succ_appr_n(self, n):
        return self.get_G(n)*math.exp(-self.get_G(n))

    def get_P_succ_appr_G(self, G):
        return G*math.exp(-G)

    def get_D_n(self, n):
        return (self.m-n)*self.prob_a() - self.get_P_succ_appr_n(n)



def create_figure_with_params():

    matplotlib.rcParams.update({'font.size': 14})
    matplotlib.rcParams.update({'figure.autolayout': True})

    plt.figure(figsize=(7, 4.5))    


def plot_performance(metric="throughput"):
    create_figure_with_params()

    # simulation parameters:
    m = 10
    retrans_prob_all = [0.05, 0.2, 0.3, 0.5]
    total_arr_rate_all = [0.01+0.01*x for x in range(100)]

    # plots
    p = []

    for retrans_prob in retrans_prob_all:

        # metrics
        expected_ns = []
        throughput = []

        # for all loads
        for total_arr_rate in total_arr_rate_all:

            pure_aloha = PureAloha(m=m, total_arr_rate=total_arr_rate, retrans_prob=retrans_prob)

            # get steady-state probabilities
            p_values = pure_aloha.get_p_values()
          
            # number of backlogged nodes
            expected_n = sum([p_values[i]*i for i in range(len(p_values))])
            expected_ns.append(expected_n)
          
            # throughput
            T = sum([p_values[i]*pure_aloha.get_p_success(i) for i in range(len(p_values))])
            throughput.append(T)
       

        if metric == "throughput":        
            p.append(plt.plot(total_arr_rate_all, throughput, '-'))
    


    plt.grid(True)
    plt.xlabel('Total load '+r'$\lambda$')
    if metric == "throughput":
        plt.ylabel('Throughput '+r'$T$')
    
    
    plt.legend((r'$retrans_prob$='+str(retrans_prob_all[0]), r'$retrans_prob$='+str(retrans_prob_all[1]), r'$retrans_prob$='+str(retrans_prob_all[2]), r'$retrans_prob$='+str(retrans_prob_all[3])), loc=0)


if __name__=='__main__':
    
    plot_performance("throughput")    
    plt.show()    
