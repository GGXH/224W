import gc
import operator
import pickle
import snap


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

##--we see a single community and its immediate friend as a graph
def get_single_commonly(gf, comm_map_comm, c_id):
    '''
    return a graph from a community in a graph
    '''
    node_id_list = comm_map_comm[c_id]
    gf_comm = snap.TUNGraph.New()
    for id in node_id_list:
        gf_comm.AddNode(id)
    for id in node_id_list:
        ni = gf.GetNI(id)
        deg = ni.GetDeg()
        for nbr_i in xrange(deg):
            nbr_id = ni.GetNbrNId(nbr_i)
            if gf_comm.IsNode(nbr_id):
                gf_comm.AddEdge(id, nbr_id)
    return gf_comm

if __name__ == "__main__":
    gf_file = "data/com-lj.ungraph.txt"
    gf = snap.LoadEdgeList(snap.PUNGraph, gf_file, 0, 1)
    print "Load graph! With nodes ", gf.GetNodes(), " and edges ", gf.GetEdges()
    ##--Betweenness Centrality
    #ni_btw_c_ary = snap.TIntFltH()
    #edg_btw_c_ary = snap.TIntPrFltH()
    #snap.GetBetweennessCentr(gf, ni_btw_c_ary, edg_btw_c_ary)
    ##--convert to map
    #ni_btw_c_map = {}
    #for key in ni_btw_c_ary:
    #    ni_btw_c_map[key] = ni_btw_c_ary[key]
    #edg_btw_c_map = {}
    #for key in edg_btw_c_ary:
    #    key_str = "_".join(key)
    #    edg_btw_c_map[key_str] = edg_btw_c_ary[key]
    ##--dump betweenness centrality
    #btw_centr_file = "btw_ctr_comm_1st.pkl"
    #with  open(btw_centr_file, "wb") as fl:
    #    pickle.dump(ni_btw_c_map, fl)
    #    pickle.dump(edg_btw_c_map, fl)
    ##--
    comm_file = 'data/com-lj.all.cmty.txt'
    comm_map_usr, comm_map_comm = get_comm_info(comm_file)
    ##--get community size
    comm_size = {}
    for id in comm_map_comm:
        comm_size[id] = len(comm_map_comm[id])
    ##--sorted community by its size
    sorted_comm_size = sorted(comm_size.items(), key = operator.itemgetter(1), reverse=True)
    sorted_id_comm_size = [ item[0] for item in sorted_comm_size ]
    ##--find the between center in each community, if we see each single community as a graph
    comm_high_nibwt_cnt = {}
    comm_high_edgbwt_cnt = {}    
    for i in xrange(len(sorted_id_comm_size)):
        gc.collect()
        comm_gf = get_single_commonly(gf, comm_map_comm, sorted_id_comm_size[i])
        ni_btw_c_ary = snap.TIntFltH()
        edg_btw_c_ary = snap.TIntPrFltH()        
        snap.GetBetweennessCentr(comm_gf, ni_btw_c_ary, edg_btw_c_ary)
        ##--convert to map
        ni_btw_c_map = {}
        for key in ni_btw_c_ary:
            ni_btw_c_map[key] = ni_btw_c_ary[key]
        edg_btw_c_map = {}
        for key in edg_btw_c_ary:
            key_str = "_".join(key)
            edg_btw_c_map[key_str] = edg_btw_c_ary[key]        
        tmp_sorted_nibtw = sorted(ni_btw_c_map.items(), key = operator.itemgetter(1), reverse=True)
        tmp_sorted_id_nibtw = [ item[0] for item in tmp_sorted_nibtw ]
        tmp_sorted_edgbtw = sorted(edg_btw_c_map.items(), key = operator.itemgetter(1), reverse=True)
        tmp_sorted_id_edgbtw = [ item[0] for item in tmp_sorted_edgbtw ]
        comm_high_nibtw_cnt1st[sorted_id_comm_size[i]] = tmp_sorted_id_nibtw
        comm_high_edgbtw_cnt1st[sorted_id_comm_size[i]] = tmp_sorted_id_edgbtw
    ##--dump file
    btw_file = "btw_commonly.pkl"
    with  open(btw_file, "wb") as fl:
        pickle.dump(comm_high_nibtw_cnt1st, fl)
        pickle.dump(comm_high_edgbtw_cnt1st, fl)
