import gc
import pickle

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

def get_comm_map(gf_map, comm_map_usr, comm_map_comm):
    '''
    get community map
    '''
    comm_map = {}
    for comm_id in comm_map_comm:
        comm_map[comm_id] = {}
    comm_map_comm.clear()
    for id in gf_map:
        if id not in comm_map_usr:
            comm_map[-id] = {}
    fl = open("comm_graph_edge.txt", "w")
    for id in gf_map:
        nid = id
        if id not in comm_map_usr:
            nid = -id
        for nbr_id in gf_map[id]:
            nnbr_id = nbr_id
            if nbr_id not in comm_map_usr:
                nnbr_id = -nbr_id
            if nid > 0 and nnbr_id > 0:
                for c_id in comm_map_usr[id]:
                    line = str(c_id)
                    for c_nbr_id in comm_map_usr[nbr_id]:
                        line += " " + str(c_nbr_id)
                    fl.write(line)
                    fl.write("\n")
                        # if c_nbr_id in comm_map[c_id]:
                            # comm_map[c_id][c_nbr_id] += 0.5
                        # else:
                            # comm_map[c_id][c_nbr_id] = 0.5
            elif nid > 0:
                line = str(nnbr_id)
                for c_id in comm_map_usr[id]:
                    line += " " + str(c_id) 
                fl.write(line)
                fl.write("\n")
                    # if nnbr_id in comm_map[c_id]:
                        # comm_map[c_id][nnbr_id] += 0.5
                    # else:
                        # comm_map[c_id][nnbr_id] = 0.5
            elif nnbr_id > 0:
                line = str(nid)
                for c_nbr_id in comm_map_usr[nbr_id]:
                    line += " " + str(c_nbr_id)
                fl.write(line)
                fl.write("\n")
                    # if c_nbr_id in comm_map[nid]:
                        # comm_map[nid][c_nbr_id] += 0.5
                    # else:
                        # comm_map[nid][c_nbr_id] = 0.5            
            else:
                line = str(nid) + " " + str(nnbr_id)
                fl.write(line)
                fl.write("\n")
                # if nnbr_id in comm_map[nid]:
                    # comm_map[nid][nnbr_id] += 0.5
                # else:
                    # comm_map[nid][nnbr_id] = 0.5
    gf_map.clear()
    fl.close()
    return comm_map


if __name__ == "__main__":
    ##--get graph map
    # gf_file = "data/com-lj.ungraph.txt"
    # gf_map = get_graph_info(gf_file)
    # gc.collect()
    # print "Get graph map"
    gf_file = "whole_graph_map.pkl"
    # with open(gf_file, 'wb') as fl:
        # pickle.dump(gf_map, fl)
    gf_map = ""
    with open(gf_file, 'r') as fl:
        gf_map = pickle.load(fl)
    print "Dump the whole graph map to pickle"
    gc.collect()
    ##--get community information
    comm_file = 'data/com-lj.all.cmty.txt'
    comm_map_usr, comm_map_comm = get_comm_info(comm_file)
    print "Get community user and community map"
    gc.collect()
    ##--get community graph
    comm_map = get_comm_map(gf_map, comm_map_usr, comm_map_comm)
    gf_file = "comm_graph.pkl"
    with open(gf_file, "wb") as fl:
        pickle.dump(comm_map, fl)
        pickle.dump(comm_map_usr, fl)
