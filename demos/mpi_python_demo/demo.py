from mpi4py import MPI
comm=MPI.COMM_WORLD
prank = comm.Get_rank()
p = comm.Get_size()

if prank!=0:
  message = "Hello from %s", str(prank)
  comm.send(message, dest=0)

else:
  for pid in range(1, p):
    message = comm.recv(source=pid)
    print("PID 0 received Hello from", pid)   

if MPI.Is_initialized():
   #MPI.COMM_WORLD.Barrier()
   MPI.Finalize()
 
