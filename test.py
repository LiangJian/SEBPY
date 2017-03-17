###################################
#  simple SEB to my understanding
#          3/18/2016    lj
#       Modified 5/20/2016
###################################

###################################
import XMBF_class as Xc
import XMBF_function as Xf
###################################

Xc.SebParams()
Xf.info("hello world!", Xc.SebParams.Verbose)

# FIX IT! ADD FUNCTIONS TO READ INPUT FILE LATER!
# Xf.info(sys.argv[0])

Xc.XmbfParams(761, 128, 1, 1, 'proton-wp.txt')
Xc.XmbfIo.read_data_file()
Xc.XmbfIo.write_data_file()

'''
First trial
One way is that each fit uses 4 points.
Another way is to set the end point always be N_t/2 or Fit_range_end.
I'm not sure which one is good so I offer a argument here.
'''

t_1_s1 = 0
t_2_s1 = 0
print(t_1_s1)
print(t_2_s1)

for i in range(int(Xc.XmbfParams.N_t/2), Xc.SebParams.Init_test_range, -1):
    if Xc.SebParams.trial_1_method == 1:
        Xc.XmbfParams.set_t1t2(i-Xc.SebParams.Init_test_range, i)
    else:
        if Xc.SebParams.trial_1_method == 2:
            Xc.XmbfParams.set_t1t2(i-1, Xc.XmbfParams.N_t/2)
        else:
            print("method wrong")

    Xc.XmbfParams.set_e_a(0.2, 500000)
    Xc.HandleInput.init('input_attempt_1.xml')
    Xc.HandleInput.refresh()
    Xc.XmbfFitting.do_fit()
    if Xc.XmbfFitting.If_fail:
        break
    t_1_s1 = Xc.XmbfParams.t1
    t_2_s1 = Xc.XmbfParams.t2
    Xf.info('Now the fit range is %02d' % Xc.XmbfParams.t1 + " ~ %02d:" % Xc.XmbfParams.t2, Xc.SebParams.Verbose)
    Xc.XmbfFitting.print()

Xf.info("============================================")
Xf.info('The result fit range of stage one is %02d' % t_1_s1 + " ~ %02d" % t_2_s1, True)
Xf.info("============================================")


'''
Second trial
'''
for i in range(int(t_1_s1), 0, -1):
    Xc.XmbfParams.set_t1t2(i, Xc.XmbfParams.N_t/2)
    Xc.XmbfParams.set_e_a(0.2, 500000, 0)
    Xc.XmbfParams.set_e_a(0.2, 1, 1)
    Xc.HandleInput.init('input_attempt_2.xml')
    Xc.HandleInput.refresh()
    Xc.XmbfFitting.do_fit()
    if Xc.XmbfFitting.If_fail:
        break
    t_1_s2 = Xc.XmbfParams.t1
    t_2_s2 = Xc.XmbfParams.t2
    Xf.info('Now the fit range is %02d' % Xc.XmbfParams.t1 + " ~ %02d:" % Xc.XmbfParams.t2, Xc.SebParams.Verbose)
    Xc.XmbfFitting.print()
