import xml.etree.ElementTree as Et
import numpy as np


class XmbfParams:
    N_conf = 1
    N_t = 1
    K = 1
    V = 1
    M = int(N_t/2)
    N = N_conf
    X = np.arange(0, M)
    If_init_param = 0
    File_name = ""  # data file name
    twopf = np.loadtxt("")  # data
    Input_file_name = "input_template.xml"  # input template
    t1 = 0  # t small
    t2 = 0  # t large
    E = 0
    A = 0
    dE = np.zeros(10)
    dA = np.zeros(10)

    @classmethod
    def _init_(cls, n_conf, nt, k, v, file_name):
        cls.N_conf = n_conf
        cls.N_t = nt
        cls.K = k
        cls.V = v
        cls.M = int(cls.N_t/2)
        cls.X = np.arange(0, cls.M)
        cls.File_name = file_name
        cls.If_init_param = 1


class XmbfIo(XmbfParams):

    @classmethod
    def read_data_file(cls):
        if cls.If_init_param == 0:
            print("class should be init first!")
            return
        print("check the data file")
        twopf = np.loadtxt(cls.File_name, float, '#', None, None, 0, None, False, 0)
        print(twopf.size, twopf.shape)
        if twopf.shape[0] != cls.N_conf*cls.N_t:
            print("the data file is not consistent with N_conf and N_t")
            exit(-1)
        else:
            print("data file read")

    @classmethod
    def write_data_file(cls):
        if cls.If_init_param == 0:
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
    If_init = 0

    @classmethod
    def do_fit(cls):
        print("fit")


class HandleInput(XmbfParams):
    root = Et.parse("").getroot()
    If_init_input = 0

    @classmethod
    def init(cls, file_name):
        cls.File_name = file_name
        tree = Et.parse(cls.Input_file_name)
        cls.root = tree.getroot()
        cls.If_init_input = 1

    @classmethod
    def set_t1(cls, t11):
        cls.t1 = t11
        cls.root[0][0][4][1][0].text = str(cls.t1)

    @classmethod
    def set_t2(cls, t22):
        cls.t2 = t22
        cls.root[0][0][4][1][1].text = str(cls.t2)

    @classmethod
    def set_t1(cls, t11):
        cls.t1 = t11
        cls.root[0][0][4][1][0].text = str(cls.t1)

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
