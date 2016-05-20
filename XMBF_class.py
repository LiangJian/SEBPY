import xml.etree.ElementTree as Et
import numpy as np
import XMBF_function as Xf


class SebParams:
    Fit_range_end = 36  # the end of fit range
    Init_test_range = 4  # the test range of first try
    Tolerance_type = 1  # 1->chi^2; 2->pValue
    Chi2_ratio_tolerance = 0.1  # \chi^2 ratio tolerance
    Chi2_abs_tolerance = 0.1  # \chi^2 absolute tolerance
    PValue_ratio_tolerance = 0.1  # pValue ratio tolerance
    PValue_abs_tolerance = 0.1  # pValue absolute tolerance
    N_term = 3  # mass terms included in the fitting
    Verbose = False
    If_init_param = 0

    @classmethod
    def __init__(cls, fit_range_end=36, init_test_range=4, tolerance_type=1, verbose=1):
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
    twopf = np.loadtxt("")  # data
    Input_file_name = "input_template.xml"  # input template
    t1 = 0  # t small
    t2 = 0  # t large
    E = 0
    A = 0
    dE = np.zeros(10)
    AA = np.zeros(10)

    @classmethod
    def __init__(cls, n_conf, nt, k, v, file_name):
        cls.N_conf = n_conf
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
        cls.A = aa
        cls.E = ee

    @classmethod
    def set_de_aa(cls, dee, aa, index=1):
        if index == 0:
            Xf.info("wrong index!", True)
            return
        cls.AA[index] = aa
        cls.dE[index] = dee


class XmbfIo(XmbfParams):

    @classmethod
    def read_data_file(cls):
        if not cls.If_init_param:
            print("class should be init first!")
            return
        print("check the data file")
        twopf = np.loadtxt(cls.Data_file_name, float, '#', None, None, 0, None, False, 0)
        print(twopf.size, twopf.shape)
        if twopf.shape[0] != cls.N_conf*cls.N_t:
            print("the data file is not consistent with N_conf and N_t")
            exit(-1)
        else:
            print("data file read")

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


class XmbfFitting:
    If_init = False

    @classmethod
    def do_fit(cls):
        print("fit")


class HandleInput(XmbfParams):
    tree = Et.parse("")
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
        cls.root[2][4][1].text = str(cls.A)
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
