import xml.etree.ElementTree as Et
import numpy as np
import XMBF_function as Xf
import subprocess


class SebParams:
    Fit_range_end = 36  # the end of fit range
    Init_test_range = 4  # the test range of first try
    Tolerance_type = 1  # 1->chi^2; 2->QValue
    Chi2_ratio_tolerance = 0.1  # \chi^2 ratio tolerance
    Chi2_abs_tolerance = 0.1  # \chi^2 absolute tolerance
    QValue_ratio_tolerance = 0.1  # QValue ratio tolerance
    QValue_abs_tolerance = 0.1  # QValue absolute tolerance
    N_term = 3  # mass terms included in the fitting
    Verbose = False
    If_init_param = 0

    @classmethod
    def __init__(cls, fit_range_end=36, init_test_range=4, tolerance_type=1, verbose=True):
        cls.Fit_range_end = fit_range_end
        cls.Init_test_range = init_test_range
        cls.Tolerance_type = tolerance_type
        cls.Verbose = verbose
        cls.If_init_param = True


class XmbfParams:
    N_conf = 1
    N_t = 1
    K = 1  # number of fit function
    V = 1  # dimension of data space
    M = int(N_t/2)  # number of data points
    N = N_conf
    X = np.arange(0, M)
    If_init_param = False
    Data_file_name = ""  # data file name
    twopf = np.ndarray(shape=(N_conf*N_t, 3))  # data
    Input_file_name = "input_template.xml"  # input template
    t1 = 0  # t small
    t2 = 0  # t large
    E = 0.0
    Ee = 0.0
    dE = np.zeros(10)  # never use dE[0]
    dEe = np.zeros(10)  # never use dEe[0]
    A = np.zeros(10)
    Ae = np.zeros(10)

    @classmethod
    def __init__(cls, n_conf, nt, k, v, file_name):
        cls.N_conf = n_conf
        cls.N = cls.N_conf
        cls.N_t = nt
        cls.K = k
        cls.V = v
        cls.M = int(cls.N_t/2)
        cls.X = np.arange(0, cls.M)
        cls.Data_file_name = file_name
        cls.If_init_param = True

    @classmethod
    def set_t1(cls, t11):
        cls.t1 = t11

    @classmethod
    def set_t2(cls, t22):
        cls.t2 = t22

    @classmethod
    def set_t1t2(cls, t11, t22):
        cls.set_t1(t11)
        cls.set_t2(t22)

    @classmethod
    def set_e_a(cls, ee, aa):
        cls.A[0] = aa
        cls.E = ee

    @classmethod
    def set_de_a(cls, dee, aa, index=1):
        if index == 0:
            Xf.info("wrong index!", True)
            return
        cls.A[index] = aa
        cls.dE[index] = dee


class XmbfIo (XmbfParams):

    @classmethod
    def read_data_file(cls):
        if not cls.If_init_param:
            print("class should be init first!")
            return
        print("check the data file")
        cls.twopf = np.loadtxt(cls.Data_file_name, float, '#', None, None, 0, None, False, 0)
        print(cls.twopf.size, cls.twopf.shape)
        if cls.twopf.shape[0] != cls.N_conf*cls.N_t:
            print("the data file is not consistent with N_conf and N_t")
            exit(-1)
        else:
            print("data file read.")

    @classmethod
    def write_data_file(cls):
        if not cls.If_init_param:
            print("class should be init first!")
            return
        try:
            f = open("for_xmbf_tmp", 'w')
            f.write(str(cls.K)+'\n')
            f.write(str(cls.V)+'\n')
            f.write(str(cls.M)+'\n')
            f.write(str(cls.N)+'\n')
            for i in range(0, cls.M):
                f.write(str(i+1)+'\t'+str(cls.X[i])+'\n')
            for i in range(0, cls.N):
                for j in range(0, cls.M):
                    f.write(str(i+1)+'\t'+str(j+1)+"\t%18.10f" % cls.twopf[i*cls.N_t+j][2]+'\n')
        except IOError as e:
            print(e)
            exit(-1)
        else:
            f.close()
        finally:
            print("write file done.")


class XmbfFitting (XmbfParams):
    result = b''
    If_fail = False
    X2 = 0.0
    Qv = 0.0

    @classmethod
    def do_fit(cls):
        cls.result = subprocess.check_output("./XMBF input.xml", shell=True, stderr=subprocess.STDOUT)
        cls.result = cls.result.split()
        if b'Warning:' in cls.result:
            cls.If_fail = True
        if b'WARNING:' in cls.result:
            cls.If_fail = True
        if b'chi^2/dof' in cls.result:
            cls.X2 = float(cls.result[cls.result.index(b'chi^2/dof')+2])
        else:
            cls.If_fail = True
        if b'Q(dof/2,chi^2/2)' in cls.result:
            cls.Qv = float(cls.result[cls.result.index(b'Q(dof/2,chi^2/2)')+2])
        else:
            cls.If_fail = True
        if b'A' in cls.result:
            cls.A[0] = float(cls.result[cls.result.index(b'A')+2])
            cls.Ae[0] = float(cls.result[cls.result.index(b'A')+3])
        else:
            cls.If_fail = True
        if b'E' in cls.result:
            cls.E = float(cls.result[cls.result.index(b'E')+2])
            cls.Ee = float(cls.result[cls.result.index(b'E')+3])
        else:
            cls.If_fail = True
        for i in range(1, 10):
            if b'A'+bytes(i) in cls.result:
                cls.A[i] = float(cls.result[cls.result.index(b'A')+2])
                cls.Ae[i] = float(cls.result[cls.result.index(b'A')+3])
            if b'E'+bytes(i) in cls.result:
                cls.dE[i] = float(cls.result[cls.result.index(b'E')+2])
                cls.dEe[i] = float(cls.result[cls.result.index(b'E')+3])

    @classmethod
    def print(cls):
        if cls.If_fail:
            print("fitting failed")
        else:
            print('\033[0;31;m', end="")
            print('X2=%4.2f' % cls.X2, end=" \t")
            print('Qv=%4.2f' % cls.Qv, end=" \t")
            print('\033[0;32;m', end="")
            print('E1=%4.2e' % cls.E + '(%4.2e)' % cls.Ee, end="\t")
            print('A1=%4.2e' % cls.A[0] + '(%4.2e)' % cls.Ae[0], end="")
            print('\033[0m', end="")
            print()


class HandleInput (XmbfParams):
    tree = Et.ElementTree()
    root = tree.getroot()
    If_init_input = False

    @classmethod
    def init(cls, file_name):
        cls.Input_file_name = file_name
        cls.tree = Et.parse(cls.Input_file_name)
        cls.root = cls.tree.getroot()
        cls.If_init_input = True

    @classmethod
    def refresh(cls, name='input.xml'):
        cls.root[0][0][4][1][0].text = str(cls.t1)
        cls.root[0][0][4][1][1].text = str(cls.t2)
        cls.root[2][0][1].text = str(cls.E)
        cls.root[2][4][1].text = str(cls.A[0])
        cls.root[3][0][1].text = str(cls.N_t)
        cls.tree.write(name)

    @classmethod
    def walk_data(cls, root_node):
        children_node = root_node.getchildren()
        if len(children_node) == 0:
            return
        for child in children_node:
            cls.walk_data(child)
            keyword = str(child).split()
            print(keyword[1])
        return
