from mpi4py import MPI

comm = MPI.COMM_WORLD
prank = comm.Get_rank()

if prank == 0:
    data = {'nums' : [7, 2.72, 2+3j],
            'alph' : ( 'abc', 'xyz')}
else:
    data = None

print("Before BCast: Proc %d:\t"%(prank), data, flush=True)
if prank==0: dummy=input()
comm.Barrier()

data = comm.bcast(data, root=0)
print("After BCast: Proc %d:\t" %(prank), data, flush=True)
