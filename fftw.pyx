# cython: language_level=3

cdef extern from "fftw3.h":
    int read3images (char *fname, int * nx, int * ny, double **arr, double **barr, double **carr, int transp)
