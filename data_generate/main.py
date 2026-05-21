from tqdm import tqdm

from SIR import *

import pandas as pd

def run_single_SIR(graph, round_num = 400):
    attack_feature = []
    for i in range(100):
        attack_feature.append(random.randbytes(50))


    begin_round = random.randint(0, 350)

    # 初始化SIR模型
    model = SIRModel(graph, beta=0.1, gamma=0.05, attack_feature=attack_feature, begin_round=begin_round)

    attack_num_changes = []
    tot_num_changes = []

    for i in range(len(graph.nodes())):
        attack_num_changes.append([])
        tot_num_changes.append([])

    #while not model.isEnd():
    for i in range(round_num):
        attack_nums, tot_nums, _ = model.step(round = i)
        for ue in range(len(attack_nums)):
            attack_num_changes[ue].append(attack_nums[ue])
            tot_num_changes[ue].append(tot_nums[ue])

    return attack_num_changes, tot_num_changes


def run_all_SIR(graph, round_num = 400):

    attack_types = ['SQL Inject', 'XSS', 'Unser', 'CSRF', 'SSRF', 'DDOS', 'File Upload', 'Sandbox', 'Prompt', 'Poison']

    attack_num_changes = []
    tot_num_changes = []

    for i in range(len(graph.nodes())):
        attack_num_changes.append([])
        tot_num_changes.append([])

    for _ in range(len(attack_types)):
        attack_num_changes_round, tot_num_changes_round= run_single_SIR(graph, round_num=round_num)
        if len(attack_num_changes_round[0]) > len(attack_num_changes[0]):
            for i in range(len(attack_num_changes_round[0]) - len(attack_num_changes[0])):
                for j in range(len(attack_num_changes_round)):
                    attack_num_changes[j].append(0)
                    tot_num_changes[j].append(0) # 暂时先加0，后面再考虑更改
        for ue in range(len(attack_num_changes_round)):
            for j in range(len(attack_num_changes_round[ue])):
                attack_num_changes[ue][j] += attack_num_changes_round[ue][j]
                tot_num_changes[ue][j] += tot_num_changes_round[ue][j]
    return attack_num_changes, tot_num_changes

def calculate_rates(attack_num_changes, tot_num_changes):
    attack_rate_results = []
    for ue in range(len(attack_num_changes)):
        attack_rate = []
        for j in range(len(attack_num_changes[ue])):
            if tot_num_changes[ue][j] > 0:
                attack_rate.append(attack_num_changes[ue][j] / tot_num_changes[ue][j])
            else:
                attack_rate.append(0)
        attack_rate_results.append(attack_rate)
    return attack_rate_results


def plot_attack_rates(attack_rate_results):
    import matplotlib.pyplot as plt
    attack_rate_results = attack_rate_results[:3]
    for ue, rates in enumerate(attack_rate_results):
        plt.plot(rates, label=f'UE {ue}')

    plt.xlabel('Time Steps')
    plt.ylabel('Attack Packages')
    plt.title('Attack Packages Over Time')
    plt.legend()
    plt.show()


def handle_SIRs_round_by_round(num_nodes, prob_edge, round_num, beta=0.1, gamma=0.05):
    attack_feature = []
    for i in range(100):
        attack_feature.append(random.randbytes(50))

    graph = nx.erdos_renyi_graph(num_nodes, prob_edge)

    SIR_models = []

    next_round = 0

    tot_attack_pkgs = []
    for i in range(num_nodes):
        tot_attack_pkgs.append([])

    for round in tqdm(range(round_num)):
        if round == next_round:

            model = SIRModel(graph, beta=beta, gamma=gamma, attack_feature=attack_feature, begin_round=round)
            SIR_models.append(model)
            next_round += random.randint(20, 50)


        tot_attack_nums = [0] * num_nodes

        pop_idx = []


        for model in SIR_models:


            attack_nums, tot_nums, _ = model.step(round=round)
            for ue in range(num_nodes):
                tot_attack_nums[ue] += attack_nums[ue]
            if model.get_status_counts()['I'] == 0:
                pop_idx.append(SIR_models.index(model))

        pop_idx.sort(reverse=True)

        for idx in pop_idx:
            SIR_models.pop(idx)

        for ue in range(num_nodes):
            tot_attack_pkgs[ue].append(tot_attack_nums[ue])
    return tot_attack_pkgs

def main():
    # 创建一个随机图
    num_nodes = 100
    prob_edge = 0.1
    tot = 20000 * 50 * 2
    beta = 0.1
    gamma = 0.05

    round_num = tot // (num_nodes)

    #
    # num_nodes = 50
    # prob_edge = 0.1
    # round_num = 400

    tot_attack_pkgs = handle_SIRs_round_by_round(num_nodes, prob_edge, round_num, beta, gamma)
    plot_attack_rates(tot_attack_pkgs)

    # 将数据保存为csv
    dic1 = {}
    date = []
    for i in range(round_num):
        date.append(i)
    dic1["date"] = date

    for ue in range(len(tot_attack_pkgs)):
        dic1[str(ue)] = tot_attack_pkgs[ue]

    df = pd.DataFrame(dic1, index=range(0, round_num))
    df.to_csv('100.csv', index=False, encoding='gbk')
    print("end")


if __name__ == '__main__':
    main()
    """
    # 创建一个随机图
    num_nodes = 50
    prob_edge = 0.1
    round_num = 400

    graph = nx.erdos_renyi_graph(num_nodes, prob_edge)
    attack_num_changes, tot_num_changes = run_all_SIR(graph, round_num)

    #print(attack_num_changes)
    attack_rate_results = calculate_rates(attack_num_changes, tot_num_changes)

    plot_attack_rates(attack_rate_results)

    # 将数据保存为csv
    dic1 = {}
    date = []
    for i in range(round_num):
        date.append(i)
    dic1["date"] = date

    for ue in range(len(attack_rate_results)):
        dic1[str(ue)] = attack_rate_results[ue]

    df = pd.DataFrame(dic1, index=range(0, round_num))
    df.to_csv('data.csv', index=False, encoding='gbk')
    print("end")
    """
    """
    # 初始化SIR模型
    model = SIRModel(graph, beta=0.2, gamma=0.2, attack_feature=attack_feature)
    susceptible_counts = []
    infected_counts = []
    recovered_counts = []

    rates_changes = []
    for idx in range(num_nodes):
        rates_changes.append([])


    while not model.isEnd():
        counts = model.get_status_counts()
        susceptible_counts.append(counts['S'])
        infected_counts.append(counts['I'])
        recovered_counts.append(counts['R'])
        attack_rate_results = model.step()
        for ue in range(len(attack_rate_results)):
            rates_changes[ue].append(attack_rate_results[ue])

    print(rates_changes)

    print(model.get_status_counts())
    """