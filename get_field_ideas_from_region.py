from __future__ import print_function  # get python 3 print function
import re
import numpy as pl

from pipeline.infrastructure import casatools

"""

find_fields(msfile=None, distance='0deg', phase_center=None, matchregex='')
"""


def find_fields(msfile=None, distance='0deg', phase_center=None, matchregex=''):

    # Created STM 2016-May-16 use center direction measure
    # Returns list of fields from msfile within a rectangular box of size distance

    # Version STM 2016-Jun-07 add matchregex parameter for name
    # Version STM 2016-Jun-18 correct RA sep for cos(dec)
    # Version STM 2016-Jul-11 actually implement Jun 18 fix :(

    qa = casatools.quanta
    me = casatools.measures
    tb = casatools.table

    fieldlist = []

    phase_center = phase_center.split()
    center_dir = me.direction(phase_center[0], phase_center[1], phase_center[2])
    center_ra = center_dir['m0']['value']
    center_dec = center_dir['m1']['value']

    try:
        qdist = qa.toangle(distance)
        qrad = qa.convert(qdist, 'rad')
        maxrad = qrad['value']
    except:
        print('ERROR: cannot parse distance ', distance)
        return

    try:
        tb.open(msfile + '/FIELD')
    except:
        print('ERROR: could not open ' + msfile + '/FIELD')
        return
    field_dirs = tb.getcol('PHASE_DIR')
    field_names = tb.getcol('NAME')
    tb.close()

    (nd, ni, nf) = field_dirs.shape
    print('Found ' + str(nf) + ' fields')

    # compile field dictionaries
    ddirs = {}
    flookup = {}
    for i in range(nf):
        fra = field_dirs[0, 0, i]
        fdd = field_dirs[1, 0, i]
        rapos = qa.quantity(fra, 'rad')
        decpos = qa.quantity(fdd, 'rad')
        ral = qa.angle(rapos, form=["tim"], prec=9)
        decl = qa.angle(decpos, prec=10)
        fdir = me.direction('J2000', ral[0], decl[0])
        ddirs[i] = {}
        ddirs[i]['ra'] = fra
        ddirs[i]['dec'] = fdd
        ddirs[i]['dir'] = fdir
        fn = field_names[i]
        ddirs[i]['name'] = fn
        if fn in flookup:
            flookup[fn].append(i)
        else:
            flookup[fn] = [i]
    print('Cataloged ' + str(nf) + ' fields')

    # Construct offset separations in ra,dec
    print('Looking for fields with maximum separation ' + distance)
    nreject = 0
    skipmatch = matchregex == '' or matchregex == []
    for i in range(nf):
        dd = ddirs[i]['dir']
        dd_ra = dd['m0']['value']
        dd_dec = dd['m1']['value']
        sep_ra = abs(dd_ra - center_ra)
        if sep_ra > pl.pi:
            sep_ra = 2.0 * pl.pi - sep_ra
        # change the following to use dd_dec 2017-02-06
        sep_ra_sky = sep_ra * pl.cos(dd_dec)

        sep_dec = abs(dd_dec - center_dec)

        ddirs[i]['offset_ra'] = sep_ra_sky
        ddirs[i]['offset_ra'] = sep_dec

        if sep_ra_sky <= maxrad:
            if sep_dec <= maxrad:
                if skipmatch:
                    fieldlist.append(i)
                else:
                    # test regex against name
                    foundmatch = False
                    fn = ddirs[i]['name']
                    for rx in matchregex:
                        mat = re.findall(rx, fn)
                        if len(mat) > 0:
                            foundmatch = True
                    if foundmatch:
                        fieldlist.append(i)
                    else:
                        nreject += 1

    print('Found ' + str(len(fieldlist)) + ' fields within ' + distance)
    if not skipmatch:
        print('Rejected ' + str(nreject) + ' distance matches for regex')

    return fieldlist
