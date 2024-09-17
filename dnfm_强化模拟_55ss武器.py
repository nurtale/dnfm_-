import random
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

# start from level-10 ||| 从强化10级起算
enhance_success_proba = [0.2, 0.12, 0.09, 0.07, 0.04, 0.03, 0.03, 0.03, 0.03, 0.03]
ehance_eff = 50
#53,57,56,60,59,56,53,55,45,42,48,51,47
#53,51,51,47,42,49

def find_more(L, num):
    for i, x in enumerate(L):
        if num >= x: continue
        return i-1
    return 10

def GetHistogram(L, data_range, title):
    hist, bin_edges = np.histogram(L, bins=101, range=data_range)
    fig, ax = plt.subplots(dpi=300)
    plt.grid(alpha=0.5, linestyle="-.")
    plt.title(title, fontsize=13, fontweight="bold")
    ax.hist(bin_edges[:-1], bin_edges, weights=hist, color="blue", alpha=0.5)
    ax.set_xlabel('充能值(万)')
    ax.set_ylabel('计数')
    plt.show()
    
def GetCDF(L, title):
    fig, ax = plt.subplots(dpi=300)
    sns.ecdfplot(data=L, legend=True)
    ax.axvline(x=540.8471, color='r', linestyle='--')
    ax.axvline(x=761.3461, color='r', linestyle='--')
    ax.axvline(x=999.7614, color='r', linestyle='--')
    ax.axvline(x=1264.3711, color='r', linestyle='--')
    
    plt.grid(alpha=0.5, linestyle="-.")
    plt.title(title, fontsize=13, fontweight="bold")
    ax.set_xlabel('充能值(万)')
    ax.set_ylabel('累计频率')
    plt.show()  


class Weapon_ss:
    def __init__(self):
        self.total_charge = 0
        self.level = 0
        self.buff_eff = 3
        self.buff_cost = 1
        
        self.charge_thres = [151405, 246802, 408102, 728366, 1228004, 1940642, 3361784, 5408471, 7613461, 11155631, 14160000]
        self.enhance_cost = [170, 181, 205, 234, 255, 288, 307, 331, 359, 450]
    
    def update_level(self):
        self.level = find_more(self.charge_thres, self.total_charge)
    
    def inherit(self, from_weapon):
        self.total_charge = from_weapon.total_charge
        self.update_level()
    
    def getCost(self):
        return self.enhance_cost[self.level]

    def enhance(self, buff_bool=False):
        p = random.random()
        if buff_bool: p_thres, _ehance_eff = enhance_success_proba[self.level] * 2, ehance_eff * self.buff_eff
        else: p_thres, _ehance_eff = enhance_success_proba[self.level], ehance_eff
        
        if p < p_thres: self.total_charge += self.charge_thres[self.level+1] - self.charge_thres[self.level]
        else: self.total_charge += _ehance_eff * self.enhance_cost[self.level]
        
        self.update_level()

class Enhance_event:
    def __init__(self, total_coal, total_buff, weapon):
        self.total_coal = total_coal
        self.total_buff = total_buff
        self.weapon = weapon

    def Start(self):
        weapon = Weapon_ss()
        weapon.inherit(self.weapon)
        
        while (self.total_coal > 0) and (weapon.level < 10):
            self.total_coal = self.total_coal - weapon.getCost()
            weapon.enhance(False)
        self.weapon = weapon
        
        

total_coal, total_buff = 30000, 99999
iter_num = 10000

w1 = Weapon_ss()
w1.total_charge = 11155631 + (14160000 - 11155631) * 0.15
w1.update_level()

result_charge = []
result_level = []
for i in range(iter_num):
    e = Enhance_event(total_coal, total_buff, w1)   #两个参数分别是总碳量和总幸运符量
    e.Start()
    
    #print(e.weapon.total_charge)
    result_charge.append(e.weapon.total_charge)
    result_level.append(e.weapon.level)

GetHistogram(np.array(result_charge) / 10000, (1000, 2000), "{}碳+{}符".format(total_coal, total_buff))
GetCDF(np.array(result_charge) / 10000, "{}碳+{}符".format(total_coal, total_buff))
#GetHistogram(np.array(result_level) + 10, (15, 20))
    



