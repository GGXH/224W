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

def lnr_thres_mod_1step_v2(gf_map, act_nod_list, new_act_nod, nd_prob_map, nbr_map):
    '''
    perform 1 step linear threshold model model
    '''
    new_pre_nod = set()
    for id in new_act_nod:
        for nbr_id in gf_map[id]:
            if nbr_id not in act_nod_list:
                if nbr_id not in nbr_map:
                    count = 0
                    for nbr_nbr_id in gf_map[nbr_id]:
                        if nbr_nbr_id in act_nod_list:
                            count += 1
                    nbr_map[nbr_id] = count
                else:
                    nbr_map[nbr_id] += 1
                if nbr_id not in nd_prob_map:
                    nd_prob_map[nbr_id] = random.randint(1, len(gf_map[nbr_id]))
                if nbr_map[nbr_id] >= nd_prob_map[nbr_id]:
                    new_pre_nod.add(nbr_id)
                    act_nod_list.add(nbr_id)
                    nd_prob_map.pop(nbr_id)
                    nbr_map.pop(nbr_id)
    return act_nod_list, new_pre_nod


if __name__ == "__main__":
    gf_file = "data/com-lj.ungraph.txt"
    gf = snap.LoadEdgeList(snap.PUNGraph, gf_file, 0, 1)
    print "Load graph! With nodes ", gf.GetNodes(), " and edges ", gf.GetEdges()
    gf_map = get_graph_info(gf_file)
    ##--get run the model with random initial
    mean_list = {}
    std_list = {}
    for total_iter in [10, 100, 1000, 10000, 100000, 1000000]:
        total_influence = [0] * total_iter
        for i in xrange(total_iter):
            init_set = 1
            new_act_nod = set()
            nd_prob_map = {}
            nbr_map = {}
            for j in xrange(init_set):
                new_act_nod.add(gf.GetRndNId())
            act_nod_list = new_act_nod.copy()
            while len(new_act_nod) != 0:
                act_nod_list, new_act_nod = lnr_thres_mod_1step_v2(gf_map, act_nod_list, new_act_nod, nd_prob_map, nbr_map)
            if i % (total_iter / 10) == 0:
                print total_iter, i, len(act_nod_list), len(new_act_nod)
            total_influence[i] = len(act_nod_list)
        total_influence = pd.DataFrame(total_influence)
        mean_list[total_iter] = total_influence.mean()[0]
        std_list[total_iter] = total_influence.std()[0]
        print total_iter, mean_list[total_iter], std_list[total_iter]
