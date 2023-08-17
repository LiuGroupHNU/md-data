#!/bin/bash
gmx_mpi grompp -f md.mdp -c lig_solv.gro -p topol.top -o md.tpr -maxwarn 3
export GMX_MDPU_INPUT_JSON=input.json
gmx_mpi mdrun -deffnm md
