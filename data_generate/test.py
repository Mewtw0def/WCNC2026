if __name__ == '__main__':
    from SIR import SIRModel
    import networkx as nx
    import random

    # 创建一个随机图
    num_nodes = 50
    prob_edge = 0.1
    graph = nx.erdos_renyi_graph(num_nodes, prob_edge)

    attack_feature = []
    for i in range(1000):
        attack_feature.append(random.randbytes(50))

    # 初始化SIR模型
    model = SIRModel(graph, beta=0.2, gamma=0.2, attack_feature=attack_feature)
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