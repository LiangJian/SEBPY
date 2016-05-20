###################################
# print info


def info(something="", verbose=True):
    assert isinstance(something, str)
    assert isinstance(verbose, bool)
    if verbose:
        print(something)
        print('\n')
###################################
