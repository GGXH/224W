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
    load_gf = True
    load_comm = True
    ##--build undirect graph
    if load_gf:
        gf_file = "data/com-lj.ungraph.txt"
        gf = snap.LoadEdgeList(snap.PUNGraph, gf_file, 0, 1)
        print "Load graph!"
    ##--load community information
    if load_comm:
        comm_file = "data/com-lj.all.cmty.txt"
        comm_map_usr, comm_map_comm = get_comm_info(comm_file)
        print "Load community information"
        print len(comm_map_usr), len(comm_map_comm)
    ##--further coding
