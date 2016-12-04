
if __name__ == "__main__":
    file = "output_get_twolayer.txt"
    file_out = "comm_graph_edge.txt"
    with open(file, "r") as fl:
        with open(file_out, "w") as fl_o:
            for line in fl:
                line_array = line.split(">")
                if len(line_array) == 2:
                    fl_o.write(line_array[1])
                
