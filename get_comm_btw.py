import operator
import pickle
import snap

if __name__ == "__main__":
    gf_file = "comm_graph_edge.txt"
    gf = snap.LoadEdgeList(snap.PUNGraph, gf_file, 0, 1)
    ##--get betweenness centrality
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
    ##--dump file
    cl_centr_file = "comm_btw_ctr.pkl"
    with  open(cl_centr_file, "wb") as fl:
        pickle.dump(ni_btw_c_map, fl)
        pickle.dump(edg_btw_c_map, fl)
