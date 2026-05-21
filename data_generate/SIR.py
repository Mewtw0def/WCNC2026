import random
import networkx as nx
import matplotlib.pyplot as plt
import copy

class IPPool:
    def __init__(self):
        head = "127.0.0."
        self.pool = []
        for i in range(255):
            self.pool.append(head + str(i + 1))
        random.shuffle(self.pool)
    def allocate_ip(self):
        if len(self.pool) != 0:
            return self.pool.pop(0)

class Package:
    def __init__(self, value, ip, status='normal'):
        self.status = status
        self.value = value
        self.ip = ip
class InfectiousAgent:
    def __init__(self, ip, attack_feature=None, status='S', attack_rate = 0.3, msg_nums = 100, beta = 0.1):
        if attack_feature is None:
            attack_feature = []
        self.status = status  # S: susceptible, I: infected, R: recovered
        self.ip = ip
        self.attack_feature = attack_feature
        self.attack_rate = attack_rate
        self.msg_nums = msg_nums
        self.beta = beta

    def send_pkg(self, length):
        pkg_list = []
        """
        if self.status != 'I':
            for i in range(5):
                pkg_list.append(Package(value=random.randbytes(length), ip = self.ip))
        else:
            for i in range(5):
                pkg_list.append(Package(value=random.randbytes(length), ip = self.ip))
            for i in range(5):
                pkg_list.append(Package(self.attack_feature[random.randint(0,99)], ip = self.ip, status='attack'))
        """
        if self.status == 'I':
            self.attack_rate += 0.02
        elif self.status == 'R':
            self.attack_rate -= 0.03

        for i in range(self.msg_nums):
            if random.random() < self.attack_rate:
                pkg_list.append(Package(value=self.attack_feature[random.randint(0, len(self.attack_feature) - 1)], ip=self.ip, status='attack'))
            else:
                pkg_list.append(Package(value=random.randbytes(length), ip=self.ip))

        return pkg_list

class SIRModel:
    def __init__(self, graph, beta, gamma, attack_feature = None, attack_rate = 0, initial_node_num = 5, begin_round = 0):
        self.graph = graph  # 使用networkx图表示节点和连接
        self.ip_pool = IPPool()
        self.agents = {node: InfectiousAgent(self.ip_pool.allocate_ip(), attack_feature, 'S', attack_rate = attack_rate, beta = beta) for node in graph.nodes()}
        self.ini_status = copy.deepcopy(self.agents)
        self.beta = beta  # 感染率
        self.gamma = gamma  # 康复率
        self.initial_node_num = initial_node_num
        self.begin_round = begin_round

    def re_initial(self):
        self.agents = copy.deepcopy(self.ini_status)

    def initial_I(self):
        # 随机选择一些节点感染
        for i in range(self.initial_node_num):
            initial_infected = random.choice(list(self.graph.nodes()))
            self.agents[initial_infected].status = 'I'
    def step(self, round = 0):

        if round == self.begin_round:
            self.initial_I()

        new_statuses = {}

        for node in self.graph.nodes():
            agent = self.agents[node]
            if agent.status == 'I':
                # 感染过程
                for neighbor in self.graph.neighbors(node):
                    if (self.agents[neighbor].status == 'S' or self.agents[neighbor].status == 'R') and random.random() < self.agents[neighbor].beta:
                        new_statuses[neighbor] = 'I'
                # 康复过程
                if random.random() < self.gamma:
                    new_statuses[node] = 'R'
                    agent.beta = agent.beta / 2
        
        # 更新状态
        for node, status in new_statuses.items():
            self.agents[node].status = status

        attack_rate_results = []
        attack_nums = []
        tot_nums = []

        for node in self.graph.nodes():
            agent = self.agents[node]
            pkg_list = agent.send_pkg(50)

            tot_num = 0
            attack_num = 0

            for pkg in pkg_list:
                if pkg.status == 'attack':
                    attack_num += 1

                tot_num += 1

            attack_nums.append(attack_num)
            tot_nums.append(tot_num)

            attack_rate_results.append(attack_num / tot_num if tot_num > 0 else 0)

        return attack_nums, tot_nums, attack_rate_results

        #return pkg_list
            #if agent.status == 'S':
             #   print(agent.status, pkg_list)


    def get_status_counts(self):
        counts = {'S': 0, 'I': 0, 'R': 0}
        for agent in self.agents.values():
            counts[agent.status] += 1
        return counts


    def isEnd(self):
        for agent in self.agents.values():
            if agent.status == 'I':
                return False
        return True

if __name__ == '__main__':
    # 创建一个随机图
    num_nodes = 50
    prob_edge = 0.1
    graph = nx.erdos_renyi_graph(num_nodes, prob_edge)
    
    attack_feature = []
    for i in range(100):
        attack_feature.append(random.randbytes(50))
        
    # 初始化SIR模型
    model = SIRModel(graph, beta=0.2, gamma=0.2, attack_feature = attack_feature)
    susceptible_counts = []
    infected_counts = []
    recovered_counts = []

    while not model.isEnd():
        counts = model.get_status_counts()
        susceptible_counts.append(counts['S'])
        infected_counts.append(counts['I'])
        recovered_counts.append(counts['R'])
        model.step()
    print(model.get_status_counts())
"""
# 运行模拟
steps = 50
susceptible_counts = []
infected_counts = []
recovered_counts = []

for _ in range(steps):
    counts = model.get_status_counts()
    susceptible_counts.append(counts['S'])
    infected_counts.append(counts['I'])
    recovered_counts.append(counts['R'])
    model.step()

# 绘制结果
plt.plot(susceptible_counts, label='Susceptible')
plt.plot(infected_counts, label='Infected')
plt.plot(recovered_counts, label='Recovered')
plt.xlabel('Time Steps')
plt.ylabel('Number of Individuals')
plt.legend()
plt.title('SIR Model Simulation')
plt.show()
"""