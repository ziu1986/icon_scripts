#! /bin/bash
iconsrcdir=${1}
rsync -uavz $iconsrcdir/run . --exclude='*in' --exclude='.*'
rsync -uavz $iconsrcdir/externals . --exclude='.git' \
  --exclude='*.f90' --exclude='*.F90' --exclude='*.c' --exclude='*.h' \
  --exclude='*.Po' --exclude='tests' --exclude='rrtmgp*.nc' --exclude='*.mod' \
  --exclude='*.o'
rsync -uavz $iconsrcdir/make_runscripts .
ln -sf $iconsrcdir/data
ln -sf $iconsrcdir/vertical_coord_tables
