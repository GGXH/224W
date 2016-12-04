import gc
import operator
#import numpy as np
import pickle
import random
#import snap

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
    elif method == 7 or method == 13 or method == 18:
        file = "result/deg_ctr_comm_only.pkl"
    elif method == 8 or method == 14 or method == 19:
        file = "result/eignv_commonly.pkl"
    elif method == 9 or method == 15 or method == 20:
        file = "result/pgrk_commonly.pkl"
    elif method == 10 or method == 16 or method == 21:
        file = "result/deg_ctr_comm_1st.pkl"
    elif method == 11 or method == 17 or method == 22:
        file = "result/pgrk_comm1st.pkl"
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
        for i in xrange(n):
            if sorted_id_comm_size[i] >= 0:
                sorted_id.append(ctr_map[sorted_id_comm_size[i]][0])
            else:
                sorted_id.append(-sorted_id_comm_size[i])
    print sorted_id
    return sorted_id

if __name__ == "__main__":
    gf_file = "data/com-lj.ungraph.txt"
    #gf = snap.LoadEdgeList(snap.PUNGraph, gf_file, 0, 1)
    #print "Load graph! With nodes ", gf.GetNodes(), " and edges ", gf.GetEdges()
    gf_map = get_graph_info(gf_file)
    gf_id_list = gf_map.keys()
    print "Load graph! With nodes ", len(gf_map)
    ##--get run the model with random initial
    mean_list = {}
    #std_list = {}
    total_iter = 1000
    mstep = 5
    method = 13
    id_max = 31
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
        if not (method != 1 and method != 12 ):
            del sorted_id_comm_size[:]
        if method == 12:
            for id in comm_map_usr:
                comm_size[id] = len(comm_map_usr[id])
            sorted_comm_size = sorted(comm_size.items(), key = operator.itemgetter(1), reverse=True)
            sorted_id_usr_size = [item[0] for item in sorted_comm_size]
            sorted_id_usr_size = sorted_id_usr_size[:50]
            comm_size.clear()
        if method >= 13 and method <= 17:
            file = "comm_deg_dist.pkl"
            with open(file, 'r') as fl:
                degr_centr_map = pickle.load(fl)
            sorted_dgc = sorted(degr_centr_map.items(), key = operator.itemgetter(1), reverse=True)
            sorted_id_comm_size = [ item[0] for item in sorted_dgc ]
        if method > 17 and method <= 22:
            file = "eignv_comm_gf.pkl"
            with open(file, 'r') as fl:
                sorted_id_comm_size = pickle.load(fl)
    ##--
    file_nm = "lnr_thrs_"
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
    elif method == 13:
        file_nm += "deg_deg_comm_only_"
    elif method == 14:
        file_nm += "deg_eig_comm_only_"
    elif method == 15:
        file_nm += "deg_pgrk_comm_only_"
    elif method == 16:
        file_nm += "deg_deg_com1st_"
    elif method == 17:
        file_nm += "deg_pgrk_com1st_"
    elif method == 18:
        file_nm += "eig_deg_comm_only_"
    elif method == 19:
        file_nm += "eig_eig_comm_only_"
    elif method == 20:
        file_nm += "eig_pgrk_comm_only_"
    elif method == 21:
        file_nm += "eig_deg_com1st_"
    elif method == 22:
        file_nm += "eig_pgrk_com1st_"
    file_nm += str(mstep) + "_" + str(total_iter) + ".pkl"
    id_list = []
    if method != 1 and method != 12:
        id_list = get_ntop_nd(method, id_max, sorted_id_comm_size)
    for init_set in xrange(3, 31, 3):
        total_influence = [0] * total_iter
        init_act_nod = set()
        if method != 1 and method != 12:
            init_act_nod = set(id_list[:init_set])
            i = 0
            while len(init_act_nod) != init_set:
                i += 1
                init_act_nod = set(id_list[:init_set+i])
            print init_act_nod
        elif method == 12:
            init_act_nod = set(sorted_id_usr_size[:init_set])
        for i in xrange(total_iter):
            gc.collect()
            new_act_nod = set()
            nd_prob_map = {}
            nbr_map = {}
            if method == 1: ##--random
                 random.shuffle(gf_id_list)
                 new_act_nod = set(gf_id_list[:init_set])
            else:
                new_act_nod = init_act_nod.copy()
            act_nod_list = new_act_nod.copy()
            step = 0
            while len(new_act_nod) != 0 and step < mstep:
                act_nod_list, new_act_nod = lnr_thres_mod_1step_v2(gf_map, act_nod_list, new_act_nod, nd_prob_map, nbr_map)
                step += 1
            if i % (total_iter / 10) == 0:
                print init_set, i, len(act_nod_list), len(new_act_nod)
            total_influence[i] = len(act_nod_list)
        #total_influence = pd.DataFrame(total_influence)
        mean_list[init_set] = float(sum(total_influence)) / max(len(total_influence), 1)
        #std_list[init_set] = total_influence.std()[0]
        print init_set, mean_list[init_set]
    ##--dump file
    with open(file_nm, 'wb') as fl:
        pickle.dump(mean_list, fl)
        #pickle.dump(std_list, fl)
