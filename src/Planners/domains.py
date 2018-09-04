'''
Created on Sep 2, 2018

@author: Shane
'''
import pyhop
state1 = pyhop.State('state1')
state1.at = {'robot':'dock', 'birthCertificate':'Office 1'}
state1.holding = None
state1.signed = []
state1.shredded = []

prob1 = [('goAndGet', 'birthCertificate'),
         ('takeAndSign', 'birthCertificate', 'Office 2'),
         ('deliver', 'birthCertificate', 'Office 1')]
