###################################
#  simple  SEB to my understanding
#          3/18/2016    lj
###################################

###################################
import numpy as np
import xml.etree.ElementTree as Et
# import os
import sys
import subprocess
###################################

###################################
# print info


def info(something="", verbose=True):
    assert isinstance(something, str)
    assert isinstance(verbose, bool)
    if verbose:
        print(something)
        print('\n')
###################################

print("hello world!")

# FIX IT, ADD FUNCTIONS TO READ INPUT FILE LATER!
print(sys.argv[0])
# part zero, parameters table
print("step", 1)

N_t = 128
N_conf = 761
fit_range_end = 36  # the end of fit range
init_test_range = 4

tolerance_type = 1  # 1->chi^2; 2->pValue
chi2_ratio_tolerance = 0.1  # \chi^2 ratio tolerance
chi2_abs_tolerance = 0.1  # \chi^2 absolute tolerance
pValue_ratio_tolerance = 0.1  # pValue ratio tolerance
pValue_abs_tolerance = 0.1  # pValue absolute tolerance

N_term = 3  # mass terms included in the fitting

# part one, read in two-point function
print("step", 2)
print("check the data file")
twopf = np.loadtxt('proton-wp.txt', float, '#', None, None, 0, None, False, 0)
print(twopf.size, twopf.shape)
if twopf.shape[0] != N_conf*N_t:
    print("the data file is not consistent with N_conf and N_t")
    exit(-1)
else:
    print("data file read")


# part two, first trial, fit one mass term only to
# get the 1st prior.
print("step", 3, "1st trial...")

# write down the temporary XMBF format data file
K = 1
V = 1
M = int(N_t/2)
N = N_conf
X = np.arange(0, M)

try:
    f = open("for_xmbf_tmp", 'w')
    f.write(str(K)+'\n')
    f.write(str(V)+'\n')
    f.write(str(M)+'\n')
    f.write(str(N)+'\n')
    for i in range(0, M):
        f.write(str(i+1)+'\t'+str(X[i])+'\n')
    for i in range(0, N):
        for j in range(0, M):
            f.write(str(i+1)+'\t'+str(j+1)+"\t%18.10f" % twopf[i*N_t+j][2]+'\n')
except IOError as e:
    print(e)
    exit(-1)
else:
    f.close()
finally:
    info("write file done.")


# do the fit once
t1 = 0
t2 = 0
info(str(t1))
info(str(t2))
result = ""
for i in range(int(N_t/2), 0, -1):
    # parse the 1st XML input file
    tree = Et.parse('input_template.xml')
    root = tree.getroot()
    root[2][0][1].text = str(0.2)
    root[2][4][1].text = str(50000)
    root[3][0][1].text = str(N_t)  # T
    root[0][0][4][1][1].text = str(i)
    root[0][0][4][1][0].text = str(i-init_test_range)
    t1 = i-init_test_range
    t2 = i
    tree.write('input.xml')
    print("the fit range is now: ", root[0][0][4][1][0].text, '~', root[0][0][4][1][1].text)
    # print("the fit model is now: ", root[0][0][5][0][1].text)
    # print("the initial value of mass is now: ", root[2][0][1].text)
    result = subprocess.check_output("./XMBF input.xml", shell=True, stderr=subprocess.STDOUT)
    result = result.split()
    # print(result)

    if b'Warning:' in result:
        continue
    if b'WARNING:' in result:
        continue
    if b'chi^2/dof' in result:
        x2 = float(result[result.index(b'chi^2/dof')+2])
    else:
        print("XMBF fit error")
        continue
    if (x2 < 1.2) & (x2 > 0.8):
        break

dE = 0
dA = 0
info(str(dE))
info(str(dA))
print("Here comes the ground state result!")

if b'A' in result:
    print("A = ", float(result[result.index(b'A')+2]), "+/-", float(result[result.index(b'A')+3]))
    A = float(result[result.index(b'A')+2])
    dA = float(result[result.index(b'A')+3])
else:
    print("XMBF fit error")
    exit(-1)
if b'E' in result:
    print("E = ", float(result[result.index(b'E')+2]), "+/-", float(result[result.index(b'E')+3]))
    E = float(result[result.index(b'E')+2])
    dE = float(result[result.index(b'E')+3])
else:
    print("XMBF fit error")
    exit(-1)
if b'chi^2/dof' in result:
    print("chi^2/dof = ", float(result[result.index(b'chi^2/dof')+2]))
else:
    print("XMBF fit error")
    exit(-1)
if b'Q(dof/2,chi^2/2)' in result:
    print("Q(dof/2,chi^2/2) = ", float(result[result.index(b'Q(dof/2,chi^2/2)')+2]))
else:
    print("XMBF fit error")
    exit(-1)


# part three, the second trial, fit two mass terms with the
# prior of the ground state being the above result.
print("step", 4)

x2 = 0

info(str(x2))

# Move on to see where the x2 is obviously getting bigger
for i in range(t1, 0, -1):
    # parse the 1st XML input file
    tree = Et.parse('input_template.xml')
    root = tree.getroot()
    root[2][0][1].text = str(0.2)
    root[2][4][1].text = str(50000)
    root[3][0][1].text = str(N_t)  # T
    root[0][0][4][1][1].text = str(t2)
    root[0][0][4][1][0].text = str(i)
    t1 = i
    tree.write('input.xml')
    print("the fit range is now: ", root[0][0][4][1][0].text, '~', root[0][0][4][1][1].text)
    # print("the fit model is now: ", root[0][0][5][0][1].text)
    # print("the initial value of mass is now: ", root[2][0][1].text)
    result = subprocess.check_output("./XMBF input.xml", shell=True, stderr=subprocess.STDOUT)
    result = result.split()
    # print(result)

    if b'Warning:' in result:
        continue
    if b'WARNING:' in result:
        continue
    if b'chi^2/dof' in result:
        x2 = float(result[result.index(b'chi^2/dof')+2])
    else:
        print("XMBF fit error")
        continue
    if x2 > 1.5:
        break

print("the x2 is now ", x2)


# Here we use the previous results as priors to do this fit


for i in range(t1, 0, -1):
    tree = Et.parse('input_template2.xml')
    root = tree.getroot()
    root[2][0][1].text = str(E)
    root[2][0][2].text = str(E)  # prior
    root[2][0][3].text = str(dE)
    root[2][2][1].text = str(A)
    root[2][2][2].text = str(A)
    root[2][2][3].text = str(dA)
    root[0][0][4][1][1].text = str(t2)
    root[0][0][4][1][0].text = str(i)
    tree.write('input.xml')
    print("the fit range is now: ", root[0][0][4][1][0].text, '~', root[0][0][4][1][1].text)
    # print("the fit model is now: ", root[0][0][5][0][1].text)
    # print("the initial value of mass is now: ", root[2][0][1].text)
    result = subprocess.check_output("./XMBF input.xml", shell=True, stderr=subprocess.STDOUT)
    result = result.split()
    # print(result)

    if b'Warning:' in result:
        continue
    if b'WARNING:' in result:
        continue
    if b'chi^2/dof' in result:
        x2 = float(result[result.index(b'chi^2/dof')+2])
        print(x2)
    else:
        print("XMBF fit error")
        continue
    # if (x2 < 1.0) & (x2 > 0.8):
        # break

# part four, the third trial. fit three mass terms.
print("step", 5)

# part five, the fourth trial. fit four mass terms. I think we need no more.
print("step", 6)

# part six, finalize.
print("step", 7)
