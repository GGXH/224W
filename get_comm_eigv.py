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
    gf_file = "comm_graph_edge.txt"
    gf = snap.LoadEdgeList(snap.PUNGraph, gf_file, 0, 1)
    print "Load graph! With nodes ", gf.GetNodes(), " and edges ", gf.GetEdges()
    tmp_NIdEigenH = snap.TIntFltH()
    snap.GetEigenVectorCentr(gf, tmp_NIdEigenH)    
    tmp_eignv_map = {}
    for key in tmp_NIdEigenH:
        tmp_eignv_map[key] = tmp_NIdEigenH[key]
    tmp_sorted_eignv = sorted(tmp_eignv_map.items(), key = operator.itemgetter(1), reverse=True)
    tmp_sorted_id_eignv = [ item[0] for item in tmp_sorted_eignv ]
    ##--dump file
    eignv_file = "eignv_comm_gf.pkl"
    with open(eignv_file, "wb") as fl:
        pickle.dump(tmp_sorted_id_eignv, fl)    
