@echo off
plink.exe -ssh robot@192.168.0.1 -pw maker ^ "cd ~/reseni-01 && brickrun -r -- pybricks-micropython real.py"
