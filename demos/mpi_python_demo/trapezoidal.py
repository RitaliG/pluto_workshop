import numpy as np
from mpi4py import MPI
from mpi4py.MPI import ANY_SOURCE
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

a = 0.
b = 1.
n = 10000 

def f(x):
        return x*x

#parallelization occurs by dividing the range among processes
def integrateRange(a, b, n):
        integral = (f(a) + f(b))/2.0
        # n+1 endpoints, but n trapazoids
        for x in np.linspace(a,b,n+1):
            integral = integral + f(x)
        integral = integral* (b-a)/n
        return integral


h = (b-a)/n
#local_n is the number of trapezoids each process will calculate
#note that size must divide n
local_n = int(n/size)

local_a = a + rank*local_n*h
local_b = local_a + local_n*h

#initializing variables. mpi4py requires that we pass numpy objects.
integral = np.zeros(1)
recv_buffer = np.zeros(1)

# perform local computation. Each process integrates its own interval
integral[0] = integrateRange(local_a, local_b, local_n)

# communication
# root node receives results from all processes and sums them
if rank == 0:
        total = integral[0]
        for i in range(1, size):
                comm.Recv(recv_buffer, ANY_SOURCE)
                total += recv_buffer[0]
else:
        # all other process send their result 
        comm.Send(integral, dest=0)

# root process prints results
if comm.rank == 0:
        print("With n =", n, "trapezoids, our estimate of the integral from"\
        , a, "to", b, "is", total)
