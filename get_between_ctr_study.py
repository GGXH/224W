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


if __name__ == "__main__":
    gf_file = "data/com-lj.ungraph.txt"
    gf = snap.LoadEdgeList(snap.PUNGraph, gf_file, 0, 1)
    print "Load graph! With nodes ", gf.GetNodes(), " and edges ", gf.GetEdges()
    ##--Betweenness Centrality
    ni_btw_c_ary = snap.TIntFltH()
    edg_btw_c_ary = snap.TIntPrFltH()
    snap.GetBetweennessCentr(gf, ni_btw_c_ary, edg_btw_c_ary)
    ##--convert to map
    ni_btw_c_map = {}
    for key in ni_btw_c_ary:
        ni_btw_c_map[key] = ni_btw_c_ary[key]
    edg_btw_c_map = {}
    for key in edg_btw_c_ary:
        key_str = "_".join(key)
        edg_btw_c_map[key_str] = edg_btw_c_ary[key]
    ##--dump betweenness centrality
    btw_centr_file = "btw_ctr_comm_1st.pkl"
    with  open(btw_centr_file, "wb") as fl:
        pickle.dump(ni_btw_c_map, fl)
        pickle.dump(edg_btw_c_map, fl)
