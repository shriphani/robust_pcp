#!/usr/bin/env python 
#-*- coding: utf-8 -*- 
# Copyright 2013 Subhodeep Moitra, all rights reserved 
# subhodeep.moitra@gmail.com, spalakod@cs.cmu.edu

import sys, os
import argparse

import numpy as np
from pypropack import svdp;
from scipy.io import loadmat

MAX_ITERS = 1000
TOL = 1.0e-7

def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input-file',
        dest = 'npy_file',
        help = 'Location to .npy file'
    )
    parser.add_argument(
        '--prefix',
        dest = 'prefix',
        help = 'prefix for output',
        default = ''
    )
    parser.add_argument(
        '--test',
        dest = 'test',
        action = 'store_true',
        default = False
    )

    return parser.parse_args()

def converged(Z, d_norm):
    err = np.linalg.norm(Z, 'fro') / d_norm
    print 'ERR', err
    return err < TOL

def pcp(X):
    m, n = X.shape
    # Set params 
    lamda = 1./ np.sqrt(m);
    # Initialize
    Y = X;
    u, s, v = svdp(Y, k=1, which='L');
    norm_two = s[0]
    norm_inf = np.linalg.norm( Y[:], np.inf) / lamda
    dual_norm = max(norm_two, norm_inf)
    Y = Y / dual_norm

    A_hat = np.zeros((m, n))
    E_hat = np.zeros((m, n))
    mu = 1.25/norm_two 
    mu_bar = mu * 1e7
    rho = 1.5
    d_norm = np.linalg.norm(X, 'fro')

    num_iters = 0
    total_svd = 0
    stopCriterion = 1
    sv = 1

    while True:
        num_iters += 1

        temp_T = X - A_hat + (1/mu)*Y
        E_hat = np.maximum(temp_T - lamda/mu, 0)
        E_hat = E_hat + np.minimum(temp_T + lamda/mu, 0)

        u, s, v = svdp(X - E_hat + (1/mu)*Y, sv, which = 'L')

        diagS = np.diag(s);
        svp = len(np.where(s > 1/mu))
        
        if svp < sv:
            sv = min(svp + 1, n)
        
        else:
            sv = min(svp + round(0.05*n), n)
    
        A_hat = np.dot(
            np.dot(
                u[:,0:svp],
                np.diag(s[0:svp] - 1/mu)
            ), 
            v[0:svp,:]
        )

        total_svd = total_svd + 1
    
        Z = X - A_hat - E_hat;
    
        Y = Y + mu*Z;
        mu = min(mu*rho, mu_bar)

        if converged(Z, d_norm) or num_iters >= MAX_ITERS:
            return A_hat, E_hat

if __name__ == '__main__': 
    args = process_args()
    # Load Data
    if not args.test:
        data = np.load(args.npy_file)
        A_hat, E_hat = pcp(data)
        np.save(args.prefix + 'low_rank', A_hat)
        np.save(args.prefix + 'sparse', E_hat)
    else:
        data = (10*np.ones((10, 10))) + (-5 * np.eye(10))
        A_hat, E_hat = pcp(data)
        print A_hat, E_hat