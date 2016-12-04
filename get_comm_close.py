import operator
import pickle
import snap

if __name__ == "__main__":
    gf_file = "comm_graph_edge.txt"
    gf = snap.LoadEdgeList(snap.PUNGraph, gf_file, 0, 1)
    ##--Get closeness centrality
    cl_centr_map = {}
    for ni in gf.Nodes():
        cl_centr_map[ni.GetId()] = snap.GetClosenessCentr(gf, ni.GetId())
    ##--dump file
    cl_centr_file = "cl_ctr.pkl"
    with  open(cl_centr_file, "wb") as fl:
        pickle.dump(cl_centr_map, fl)
