def interprete_qchem():
    fname = input(' Enter file name you wish to open: ') #raw_input for python2.7
    op = open(fname)
    
    with op as file:
        data = file.readlines()
        if (len(data) > 0):
            print("found " + fname + " in the directory")
            #print(data)
        else: 
            print("Sorry, unable to find the " + fname + "file needed in the current directory")

    molecule ='$molecule\n'
    end = '$end\n'
    after_molecule = []
    if molecule in data:
        print("found the molecule geometry in the Q-Chem input file")
    else:
        print("molecule geomtry is missing in the Q-Chem input") 
    

    molecule_index = data.index(molecule)+1 #only the first occurrence
    after_molecule = []
    before_molecule = []
    after_molecule = data[molecule_index:]
    before_molecule = data[:molecule_index-1]

    end_index = after_molecule.index(end)
    molecule_info = []
    molecule_info = after_molecule[:end_index]

    charge = molecule_info[0].split(" ")[0]
    multiplicity = (molecule_info[0].split(" ")[1]).split("\n")[0]
    molecule_geometry = molecule_info[1:]

    basis_keyword ='basis'
    matching = [s for s in data if basis_keyword in s]
    #print(matching)
    for i in range(len(matching)-1):
        if matching[i] != matching[i+1]:
            print("Error: basis used in the jobs are different!")
        else:
            print("Passed basis checks")
    basis = (matching[0].split("basis "))[1].split("\n")[0]
    print("basis is determined to be", basis)
    return basis, charge, multiplicity, molecule_geometry

def write_psi4(basis, charge, multiplicity, molecule_geometry):
    foutname = input ("The output filename is: ") + ".in"
    fout = open (foutname, "w")
    molecule_name = input("The molecule name that user defined is: ")
    fout.write("#! Test of SFX2C-1e on molecule " + molecule_name + " with basis " + basis)
    fout.write("\n\n\nmolecule " + molecule_name + " {" + "\n")
    fout.write("  " + charge + " " + multiplicity + "\n")
    for item in molecule_geometry:
            fout.write("  %s" % item)
    fout.write("}\n")
    fout.write("\n" + "set {\n")
    fout.write("  basis " + basis +"\n")
    scf_type = input("The scf_type that user defined is: ") or "pk"
    if scf_type == "pk":
        print("The scf_type is default to pk!")
    fout.write("  scf_type " + scf_type + "\n" + "}\n\n")
    energy = input("The energy needs to be solved with: ") or "scf"
    fout.write("test_energy = energy('" + energy + "')\n")
    fout.write("set relativistic x2c\n")
    fout.write("test_rel = energy('" + energy + "') \n")
    if energy == "scf":
        print("The energy solver is default to scf!")
    fout.close()

def main():
    print("Start interpreting the Q-Chem input file...\n")
    basis, charge, multiplicity, molecule_geometry = interprete_qchem()
    print("Successfully gathered info needed for Psi4 input file...\n")
    write_psi4(basis, charge, multiplicity, molecule_geometry)

if __name__ == '__main__':
    main()
