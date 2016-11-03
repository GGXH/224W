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
def get_single_comm1st(gf, comm_map_comm, c_id):
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
            if not gf_comm.IsNode(nbr_id):
                gf_comm.AddNode(nbr_id)
            gf_comm.AddEdge(id, nbr_id)
    return gf_comm

if __name__ == "__main__":
    gf_file = "data/com-lj.ungraph.txt"
    gf = snap.LoadEdgeList(snap.PUNGraph, gf_file, 0, 1)
    print "Load graph! With nodes ", gf.GetNodes(), " and edges ", gf.GetEdges()
    comm_file = 'data/com-lj.all.cmty.txt'
    comm_map_usr, comm_map_comm = get_comm_info(comm_file)
    ##--get community size
    comm_size = {}
    for id in comm_map_comm:
        comm_size[id] = len(comm_map_comm[id])
    ##--sorted community by its size
    sorted_comm_size = sorted(comm_size.items(), key = operator.itemgetter(1), reverse=True)
    sorted_id_comm_size = [ item[0] for item in sorted_comm_size ]
    ##--find the node with highest degree centrality in each community, if we see each single community as a graph
    comm_high_eignv_cnt1st = {}
    for i in xrange(len(sorted_id_comm_size)):
        gc.collect()
        comm_gf = get_single_comm1st(gf, comm_map_comm, sorted_id_comm_size[i])
        tmp_NIdEigenH = snap.TIntFltH()
        snap.GetEigenVectorCentr(comm_gf, tmp_NIdEigenH)
        tmp_eignv_map = {}
        for key in tmp_NIdEigenH:
            tmp_eignv_map[key] = tmp_NIdEigenH[key]
        tmp_sorted_eignv = sorted(tmp_eignv_map.items(), key = operator.itemgetter(1), reverse=True)
        tmp_sorted_id_eignv = [ item[0] for item in tmp_sorted_eignv ]
        comm_high_eignv_cnt1st[sorted_id_comm_size[i]] = tmp_sorted_id_eignv
    ##--dump file
    eignv_file = "eignv_comm1st.pkl"
    with  open(eignv_file, "wb") as fl:
        pickle.dump(comm_high_eignv_cnt1st, fl)
