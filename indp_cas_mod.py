import gc
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


def get_ntop_nd(method, n, sorted_id_comm_size):
    '''
    get top n node id
    method:
    2: degree centrality
    '''
    file = ""
    if method == 2:
        file = "result/deg_ctr.pkl"
    elif method == 3:
        file = "result/pgrk.pkl"
    elif method == 4:
        file = "result/eignv.pkl"
    elif method == 5 or method == 6:
        file = "result/hit.pkl"
    elif method == 7:
        file = "result/deg_ctr_comm_only.pkl"
    elif method == 8:
        file = "result/eignv_commonly.pkl"
    elif method == 9:
        file = "result/pgrk_commonly.pkl"
    elif method == 10:
        file = "result/deg_ctr_comm_1st.pkl_red"
    elif method == 11:
        file = "result/pgrk_comm1st.pkl_red"
    ctr_map = {}
    with open(file, 'r') as fl:
        ctr_map = pickle.load(fl)
        if method == 6:
            ctr_map = pickle.load(fl)
    sorted_id = []
    sorted_dgc = []
    if method < 7:
        sorted_dgc = sorted(ctr_map.items(), key = operator.itemgetter(1), reverse=True)
        sorted_id = [ sorted_dgc[i][0] for i in xrange(n) ]
        print sorted_dgc[:n+10]
    else:
        sorted_id = [ ctr_map[sorted_id_comm_size[i]][0] for i in xrange(n) ]
    print sorted_id
    return sorted_id

def get_comm_info(comm_file):
    '''
    get community information, two maps
    map1: key: user id, value: community id array
    map2: key: community id, value: user id array
    '''
    comm_map_usr = {}
    comm_map_comm = {}
    comm_id = 0
    with open(comm_file, 'r') as cf:
        for line in cf:
            node_list = line.split('\t')
            node_list = [int(id) for id in node_list]
            for id in node_list:
                if id in comm_map_usr:
                    comm_map_usr[id].append(comm_id)
                else:
                    comm_map_usr[id] = [comm_id]
            comm_map_comm[comm_id] = node_list[:]
            comm_id += 1
    return comm_map_usr, comm_map_comm


if __name__ == "__main__":
    gf_file = "data/com-lj.ungraph.txt"
    gf_map = get_graph_info(gf_file)
    print "Load graph! With nodes ", len(gf_map)
    #gf_file = "data/com-lj.ungraph.txt"
    #gf = snap.LoadEdgeList(snap.PUNGraph, gf_file, 0, 1)
    #print "Load graph! With nodes ", gf.GetNodes(), " and edges ", gf.GetEdges()
    ##--get run the model with random initial
    prob = 0.01
    mean_list = {}
    std_list = {}
    total_iter = 1000
    mstep = 5
    method = 12
    ##--
    sorted_id_comm_size = []
    sorted_id_usr_size = []
    if method > 6:
        comm_file = 'data/com-lj.all.cmty.txt'
        comm_map_usr, comm_map_comm = get_comm_info(comm_file)
        ##--get community size
        comm_size = {}
        for id in comm_map_comm:
            comm_size[id] = len(comm_map_comm[id])    
        ##--sorted community by its size
        sorted_comm_size = sorted(comm_size.items(), key = operator.itemgetter(1), reverse=True)
        sorted_id_comm_size = [ item[0] for item in sorted_comm_size ]
        comm_size.clear()
        if method == 12:
            for id in comm_map_usr:
                comm_size[id] = len(comm_map_usr[id])
            sorted_comm_size = sorted(comm_size.items(), key = operator.itemgetter(1), reverse=True)
            sorted_id_usr_size = [item[0] for item in sorted_comm_size]
            sorted_id_usr_size = sorted_id_usr_size[:50]
    ##--
    file_nm = "indp_cas_"
    if method == 1:
        file_nm += "rnd_"
    elif method == 2:
        file_nm += "deg_ctr_"
    elif method == 3:
        file_nm += "pgrk_"
    elif method == 4:
        file_nm += "eigv_"
    elif method == 5:
        file_nm += "hub_"
    elif method == 6:
        file_nm += "aut_"
    elif method == 7:
        file_nm += "deg_comm_only_"
    elif method == 8:
        file_nm += "eigenv_comm_only_"
    elif method == 9:
        file_nm += "pgrk_commonly_"
    elif method == 10:
        file_nm += "deg_comm1st_"
    elif method == 11:
        file_nm += "pgrk_comm1st_"
    elif method == 12:
        file_nm += "more_comm_"
    file_nm += str(mstep) + "_" + str(total_iter) + ".pkl"
    for init_set in xrange(3, 31, 3):
        total_influence = [0] * total_iter
        if method != 1 and method != 12:
            init_act_nod = set(get_ntop_nd(method, init_set, sorted_id_comm_size))
        elif method == 12:
            init_act_nod = set(sorted_id_usr_size[:init_set])
        for i in xrange(total_iter):
            gc.collect()
            new_act_nod = set()
            if method == 1:
                for j in xrange(init_set):
                    new_act_nod.add(gf.GetRndNId())
            else:
                new_act_nod = init_act_nod.copy()
            act_nod_list = new_act_nod.copy()
            step = 0
            while len(new_act_nod) != 0 and step < mstep:
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
    with open(file_nm, 'wb') as fl:
        pickle.dump(mean_list, fl)
        pickle.dump(std_list, fl)
    
