#!/bin/bash
#SBATCH --job-name=heracles_ncu
#SBATCH --partition=gpuq_v100
#SBATCH --time=00:20:00
#SBATCH --exclusive
#SBATCH --output=heracles_ncu_%j.out
#SBATCH --error=heracles_ncu_%j.err

# Load necessary modules if needed (uncomment and edit if using modules)
# module load nvidia/nsight-compute

# Source environment
source /home/catA/rb263871/heraclescpp/remi/env-heracles.sh
module list

# Get the latest commit hash
COMMIT_HASH=$(git -C /home/catA/rb263871/heraclescpp log -1 --pretty=%s | tr ' ' '_' | tr -cd '[:alnum:]_-')

# Run Nsight Compute with specified options
ncu \
  --nvtx \
  --import-source yes \
  --target-processes all \
  --set full \
  --kernel-name-base demangled \
  -k regex:".*(idefix_for|LinearReconstruction)" \
  -f \
  -o ${COMMIT_HASH}-v100.ncu-rep \
  /home/catA/rb263871/heraclescpp/build-v100/src/nova++ /home/catA/rb263871/heraclescpp/inputs/rayleigh_taylor3d.ini
