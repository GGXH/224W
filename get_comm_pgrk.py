import operator
import pickle
import snap

if __name__ == "__main__":
    gf_file = "comm_graph_edge.txt"
    gf = snap.LoadEdgeList(snap.PUNGraph, gf_file, 0, 1)
    ##--Get page rank centrality (may need to calibrate the parameter)
    pgrk_H = snap.TIntFltH()
    snap.GetPageRank(gf, pgrk_H)
    ##--convert hash to map and dump to pkl file
    pgrk_map = {}
    for key in pgrk_H:
        pgrk_map[key] = pgrk_H[key]
    pgrk_file = "pgrk_comm_gf.pkl"
    with  open(pgrk_file, "wb") as fl:
        pickle.dump(pgrk_map, fl)
