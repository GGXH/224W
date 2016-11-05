import operator
import pandas as pd
import pickle
import random
import snap

##--get graph map
def get_graph_info(gf_file):
    '''
    get graph information as a map
    key: user id, value: list of friend id
    '''
    gf_map = {}
    with open(gf_file, 'r') as cf:
        for line in cf:
            if line[0] != '#':
                node_list = line.split('\t')
                if len(node_list) == 2:
                    node_list = [int(id) for id in node_list]
                    if node_list[0] in gf_map:
                        gf_map[node_list[0]].add(node_list[1])
                    else:
                        gf_map[node_list[0]] = set([node_list[1]])
                    if node_list[1] in gf_map:
                        gf_map[node_list[1]].add(node_list[0])
                    else:
                        gf_map[node_list[1]] = set([node_list[0]])                    
                else:
                    print "wrong format line: ", line
    return gf_map

def ind_cas_mod_1step_v2(gf_map, act_nod_list, new_act_nod, prob):
    '''
    perform 1 step independent cascade model
    '''
    new_pre_nod = set()
    for id in new_act_nod:
        for nbr_id in gf_map[id]:
            if nbr_id not in act_nod_list:
                lim = random.random()
                if lim < prob:
                    new_pre_nod.add(nbr_id)
                    act_nod_list.add(nbr_id)
    return act_nod_list, new_pre_nod

if __name__ == "__main__":
    gf_file = "data/com-lj.ungraph.txt"
    gf_map = get_graph_info(gf_file)
    gf_file = "data/com-lj.ungraph.txt"
    gf = snap.LoadEdgeList(snap.PUNGraph, gf_file, 0, 1)
    print "Load graph! With nodes ", gf.GetNodes(), " and edges ", gf.GetEdges()
    ##--get run the model with random initial
    prob = 0.01
    mean_list = {}
    std_list = {}
    total_iter = 1000000
    for init_set in xrange(1, 31):
        total_influence = [0] * total_iter
        for i in xrange(total_iter):
            new_act_nod = set()
            for j in xrange(init_set):
                new_act_nod.add(gf.GetRndNId())
            act_nod_list = new_act_nod.copy()
            step = 0
            while len(new_act_nod) != 0 and step < 10:
                act_nod_list, new_act_nod = ind_cas_mod_1step_v2(gf_map, act_nod_list, new_act_nod, prob)
                step += 1
            if i % (total_iter / 10) == 0:
                print init_set, i, len(act_nod_list), len(new_act_nod)
            total_influence[i] = len(act_nod_list)
        total_influence = pd.DataFrame(total_influence)
        mean_list[init_set] = total_influence.mean()[0]
        std_list[init_set] = total_influence.std()[0]
        print init_set, mean_list[init_set], std_list[init_set]
    ##--dump to file
    with open('indp_cas_rnd_10.pkl', 'wb') as fl:
        pickle.dump(mean_list, fl)
        pickle.dump(std_list, fl)
    
