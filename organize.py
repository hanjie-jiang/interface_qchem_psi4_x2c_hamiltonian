def open_psi4_output():
    fname = input(' Enter the Psi4 output file name that you have in this directory: ') 
    op = open(fname)

    with op as file:
        data = file.readlines()
        if (len(data) > 0):
            print("\n found " + fname + " in the directory\n")
        else:
            print("\n Sorry, unable to find the " + fname + " file needed in the current directory\n") 
    return data

#  header of each matrices
#  ## Relativistic Potential (Symmetry 0) ##
#  Irrep: 1 Size: 40 x 40
#
#                 1                   2                   3                   4                   5
def output_interpreter(matrix_type, end_matrix_type, data, size):
    matrix = "  ## SO-basis " + matrix_type + " Ints (Symmetry 0) ##\n"
    if (matrix_type != "Potential Energy"):
        end_matrix = "  ## SO-basis " + end_matrix_type + " Ints (Symmetry 0) ##\n"
    else:
        end_matrix = end_matrix_type
    after_matrix = []
    matrix_index = data.index(matrix)+2
    end_matrix_index = data.index(end_matrix)
    if matrix in data:
        print(" found the " + matrix_type + " matrix in Psi4 output\n")
        if (matrix_type != "Potential Energy"):           
            after_matrix = data[matrix_index:end_matrix_index]
        else:
            after_matrix = data[matrix_index:]

        # splits up all the elements in the list
        new_data = [line.split(" ") for line in after_matrix]
        for i in range(len(new_data)):
            while '' in new_data[i]:
                # removing all the empty elements in the list
                new_data[i].remove('')
                # getting rid of the "\n" characters at the end of each line
                new_data[i] = [s.strip("\n") for s in new_data[i]]
        if (matrix_type == "Potential Energy"):
            flat_data = []
            for sublist in new_data:
                for item in sublist:
                    flat_data.append(item)
            #print(flat_data)
            ending_potential = "Comparing"
            ending_potential_index = flat_data.index(ending_potential)
            #print(ending_potential_index)
            after_potential = []
            after_potential = flat_data[:ending_potential_index]
            after_potential = [x for x in after_potential if len(x) > 3]
            return after_potential 
        else:
            # getting rid of the numbers in the front of each line
            for i in range(len(new_data)):
                new_data[i] = [x for x in new_data[i] if len(x) > 3]
            #print(clean_data)
            result = [ele for ele in new_data if ele != []] 
    
            flat_list = []
            for sublist in result:
                for item in sublist:
                    flat_list.append(item)
            
            # for debugging purposes
       #     f = open("output.txt","a")
       #     for item in flat_list:
       #         f.write("%s\n" % item)
       #     f.close()
            
            return result,flat_list
    else:
        print(" no " + matrix_type + " matrix was detected\n") 
        return 0



def indexing(data):
    # in order to get the number of basis; Irreps and matrix sizes are needed
    basic_info = []
    overlap = "  ## SO-basis Overlap Ints (Symmetry 0) ##\n"
    kinetic = "  ## SO-basis Kinetic Energy Ints (Symmetry 0) ##\n"
    potential = "  ## SO-basis Potential Energy Ints (Symmetry 0) ##\n"
    index1 = data.index(overlap)+1
    index2 = data.index(kinetic)+1
    index3 = data.index(potential)+1
    return index1,index2,index3

def irrep_and_size(matrix_type, index, data):
    matrix = "  ## SO-basis " + matrix_type + " Ints (Symmetry 0) ##\n"
    print(matrix)
    if matrix in data:
        basic_info = data[index]
        info_split = basic_info.split(" ")
        keyword_irrep = "Irrep:"
        keyword_size = "Size:"
        matching_irrep = [s for s in info_split if keyword_irrep in s]
        if len(matching_irrep) != 0:
            irrep_index = info_split.index(keyword_irrep)
            irrep = info_split[irrep_index+1]
            print("The irrep of this molecule is " + irrep + "\n")
        else:
          print("Not found!")

        matching_size = [s for s in info_split if keyword_size in s]                
        if len(matching_size) != 0:
            size_index = info_split.index(keyword_size)
            # assuming the output in format "Irrep: 1 Size: 40 x 40"
            size = info_split[size_index+1]
            if (info_split[size_index + 2] == "x"):
                size2 = info_split[size_index + 3].replace("\n","")
                if (size2 != size):
                  print( matrix_type + " has to be a square matrix\n")
                  print( "Warning: setting the row and column of " + matrix + "matrix to be equal\n")
                  size2 = size
                else:
                  print("Found a " + size + " x " + size2 + " matrix\n")
            else:
                print("Unable to read in matrix info; Can only read info in 'Irrep: 1 Size: 40 x 40' format\n")
            # assuming that all the matrices are squared matrices
        else:
          print("Not found!")
        #irrep = matching 
        return irrep, size

    else:
        print(" the search of irrep and size is not supported when the " + matrix + "matrix is not found\n")
        return 0

def reorder_1doutput_write_to_file(matrix1d, name, size):
    #create a 2d array:
    size_int = int(size)
    new_matrix = [[0 for x in range(size_int)] for y in range(size_int)] 
    
    # deal with the number of loops for this reorder process
 
    loop = int(size_int/5)
    if (loop*5 < size_int):
        loop = loop + 1
    for k in range(loop):
        for i in range(size_int):
            for j in range(5):
                # for debugging
                #print("matrix[" + str(i) + "][" + str(j+k*5) + "] = old[" + str(i*5+j+k*200) + "]")
                new_matrix[i][j+k*5] = matrix1d[i*5+j+k*size_int*5]

    fname = name + ".txt" 
    f = open(fname,"a")
    f.write(str(size_int) + " " + str(size_int) + "\n")
    for i in range(size_int):
        for j in range(size_int):
            f.write("".join(new_matrix[i][j]) + " ")
        f.write("\n")
    f.close()
    return 0


def organize_2doutput_to_file(matrix2d,name):
    fname = name + ".txt"
    f = open(fname,"a")
    
    for line in matrix2d:
        #for element in line:
        f.write("%s\n" % line)
    f.close()
    return

def main():
    print("\n Start organizing the Psi4 output file...\n")
    data = open_psi4_output() 
    ioverlap, ikinetic, ipotential = indexing(data)
    overlap = "Overlap"
    kinetic = "Kinetic Energy"
    potential = "Potential Energy"
    ending_data = "\n"
    irrep_overlap, size_overlap = irrep_and_size(overlap,ioverlap,data)
    irrep_kinetic, size_kinetic = irrep_and_size(kinetic,ikinetic,data)
    irrep_potential, size_potential = irrep_and_size(potential,ipotential,data)
    # can do auto-detect in the future
    overlap2d,overlap1d = output_interpreter(overlap, kinetic, data, size_overlap)
    kinetic2d,kinetic1d = output_interpreter(kinetic, potential, data, size_kinetic)
    potential1d = output_interpreter(potential,ending_data,data,size_potential) 

    reorder_1doutput_write_to_file(overlap1d, "overlap1d", size_overlap)
    reorder_1doutput_write_to_file(kinetic1d, "kinetic1d", size_kinetic)
    reorder_1doutput_write_to_file(potential1d, "potential1d", size_potential)

if __name__ == '__main__':
    main()
