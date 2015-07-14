#!/bin/bash
source ${HOME}/.bash_profile
python ${HOME}/python/scripts/poly-rti.py -r KOD -c D -b 9 --days=10 --minskip=59.5 2>&1 1> ${HOME}/tmp/kod.d.log
python ${HOME}/python/scripts/poly-rti.py -r KOD -c C -b 3 -b 9 --days=10 --minskip=59.5 2>&1 1> ${HOME}/tmp/kod.c.log
python ${HOME}/python/scripts/poly-rti.py -r MCM -c A -b 9 --days=10 --minskip=59.5 2>&1 1> ${HOME}/tmp/mcm.a.log
python ${HOME}/python/scripts/poly-rti.py -r SPS -c A -b 9 --days=10 --minskip=59.5 2>&1 1> ${HOME}/tmp/sps.a.log
python ${HOME}/python/scripts/poly-rti.py -r ADE -c A -b 9 --days=10 --minskip=59.5 2>&1 1> ${HOME}/tmp/ade.a.log
python ${HOME}/python/scripts/poly-rti.py -r ADW -c A -b 9 --days=10 --minskip=59.5 2>&1 1> ${HOME}/tmp/adw.a.log
