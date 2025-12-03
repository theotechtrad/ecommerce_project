# shop/similarity_calc.pyx
# Cython optimized version (OPTIONAL - if build fails, app still works)

import numpy as np
cimport numpy as np
cimport cython

DTYPE = np.float64
ctypedef np.float64_t DTYPE_t

@cython.boundscheck(False)
@cython.wraparound(False)
def cosine_similarity_optimized(np.ndarray[DTYPE_t, ndim=2] X, np.ndarray[DTYPE_t, ndim=2] Y):
    """Optimized cosine similarity using Cython"""
    cdef int n_samples_X = X.shape[0]
    cdef int n_samples_Y = Y.shape[0]
    cdef int n_features = X.shape[1]
    
    cdef np.ndarray[DTYPE_t, ndim=2] similarities = np.zeros((n_samples_X, n_samples_Y), dtype=DTYPE)
    cdef np.ndarray[DTYPE_t, ndim=1] X_norms = np.zeros(n_samples_X, dtype=DTYPE)
    cdef np.ndarray[DTYPE_t, ndim=1] Y_norms = np.zeros(n_samples_Y, dtype=DTYPE)
    
    cdef int i, j, k
    cdef DTYPE_t dot_product, norm_product
    
    for i in range(n_samples_X):
        for k in range(n_features):
            X_norms[i] += X[i, k] * X[i, k]
        X_norms[i] = X_norms[i] ** 0.5
    
    for j in range(n_samples_Y):
        for k in range(n_features):
            Y_norms[j] += Y[j, k] * Y[j, k]
        Y_norms[j] = Y_norms[j] ** 0.5
    
    for i in range(n_samples_X):
        for j in range(n_samples_Y):
            dot_product = 0.0
            
            for k in range(n_features):
                dot_product += X[i, k] * Y[j, k]
            
            norm_product = X_norms[i] * Y_norms[j]
            
            if norm_product > 0:
                similarities[i, j] = dot_product / norm_product
            else:
                similarities[i, j] = 0.0
    
    return similarities