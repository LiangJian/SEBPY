###################################
#  simple  SEB to my understanding
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
Here each fit uses 4 points, I'm not sure whether this is a
good choice or not.
An optional way is to set the end point always be N_t/2 or Fit_range_end
'''
for i in range(int(Xc.XmbfParams.N_t/2), Xc.SebParams.Init_test_range, -1):
    Xc.XmbfParams.set_t1t2(i-Xc.SebParams.Init_test_range, i)
    Xc.XmbfParams.set_e_a(0.2, 50000)
    Xc.HandleInput.init('input_template.xml')
    Xc.HandleInput.refresh()
    Xc.XmbfFitting.do_fit()
    if Xc.XmbfFitting.If_fail:
        continue
    Xf.info('Now the fit range is %02d' % Xc.XmbfParams.t1 + " ~ %02d:" % Xc.XmbfParams.t2, Xc.SebParams.Verbose)
    Xc.XmbfFitting.print()
