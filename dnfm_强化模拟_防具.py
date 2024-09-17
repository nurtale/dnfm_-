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
    ax.axvline(x=5408471*0.75/10000, color='r', linestyle='--')
    ax.axvline(x=7613461*0.75/10000, color='r', linestyle='--')
    ax.axvline(x=9997614*0.75/10000, color='r', linestyle='--')
    ax.axvline(x=12643711*0.75/10000, color='r', linestyle='--')
    
    plt.grid(alpha=0.5, linestyle="-.")
    plt.title(title, fontsize=13, fontweight="bold")
    ax.set_xlabel('充能值(万)')
    ax.set_ylabel('累计频率')
    plt.show()  

class Weapon_rare:
    def __init__(self):
        self.total_charge = 0
        self.level = 0
        self.buff_eff = 3
        self.buff_cost = 1
        
        self.charge_thres = [45761, 74575, 122965, 219045, 368936, 582727, 1009070, 1623076, 2284645, 2999891, 3793720]
        self.enhance_cost = [51, 54, 62, 70, 77, 86, 92, 99, 107, 119]
    
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

class Weapon_ss:
    def __init__(self):
        self.total_charge = 0
        self.level = 0
        self.buff_eff = 3
        self.buff_cost = 1
        
        self.charge_thres = [151405*0.75, 246802*0.75, 306075, 546273, 921001, 1455480, 2521336, 5408471*0.75, 7613461*0.75, 9997614*0.75, 12643711*0.75]
        self.enhance_cost = [170*0.75, 181*0.75, 205*0.75, 234*0.75, 255*0.75, 288*0.75,
                             307*0.75, 331*0.75, 359*0.75, 398*0.75]
    
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
            if self.total_buff > 0:
                self.total_coal = self.total_coal - weapon.getCost()
                self.total_buff = self.total_buff - weapon.buff_cost
                weapon.enhance(True)
            else:
                self.total_coal = self.total_coal - weapon.getCost()
                weapon.enhance(False)
        self.weapon = weapon
        
        

total_coal, total_buff = 10000, 99999
iter_num = 10000

w1 = Weapon_ss()
w1.total_charge = 2521336
w1.update_level()

result_charge = []
result_level = []
for i in range(iter_num):
    e = Enhance_event(total_coal, total_buff, w1)   #两个参数分别是总碳量和总幸运符量
    e.Start()
    
    #print(e.weapon.total_charge)
    result_charge.append(e.weapon.total_charge)
    result_level.append(e.weapon.level)

GetHistogram(np.array(result_charge) / 10000, (500, 1600), "{}碳+{}符".format(total_coal, total_buff))
GetCDF(np.array(result_charge) / 10000, "{}碳+{}符".format(total_coal, total_buff))
#GetHistogram(np.array(result_level) + 10, (15, 20))
    

