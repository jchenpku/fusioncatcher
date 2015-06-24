#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
It takes as input a PSL formated file generated which has been converted from
SAM file (that is some-bowtie2-or-bwa--local-alignment.sam by sam2psl.py) generated by
BOWTIE2/BWA aligners. Here the assumption is that the PSL is sorted by columns 10, 14,
12, and 13.



Author: Daniel Nicorici, Daniel.Nicorici@gmail.com

Copyright (c) 2009-2015 Daniel Nicorici

This file is part of FusionCatcher.

FusionCatcher is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

FusionCatcher is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with FusionCatcher (see file 'COPYING.txt').  If not, see
<http://www.gnu.org/licenses/>.

By default, FusionCatcher is running BLAT aligner
<http://users.soe.ucsc.edu/~kent/src/> but it offers also the option to disable
all its scripts which make use of BLAT aligner if you choose explicitly to do so.
BLAT's license does not allow to be used for commercial activities. If BLAT
license does not allow to be used in your case then you may still use
FusionCatcher by forcing not use the BLAT aligner by specifying the option
'--skip-blat'. Fore more information regarding BLAT please see its license.

Please, note that FusionCatcher does not require BLAT in order to find
candidate fusion genes!

This file is not running/executing/using BLAT.

"""


# info PSL
"""
========================================================
More about PSL format is here: http://genome.ucsc.edu/FAQ/FAQformat#format2


PSL format

PSL lines represent alignments, and are typically taken from files generated
by BLAT or psLayout. See the BLAT documentation for more details. All of the
following fields are required on each data line within a PSL file:

   1. matches - Number of bases that match that aren't repeats
   2. misMatches - Number of bases that don't match
   3. repMatches - Number of bases that match but are part of repeats
   4. nCount - Number of 'N' bases
   5. qNumInsert - Number of inserts in query
   6. qBaseInsert - Number of bases inserted in query
   7. tNumInsert - Number of inserts in target
   8. tBaseInsert - Number of bases inserted in target
   9. strand - '+' or '-' for query strand. For translated alignments, second '+'or '-' is for genomic strand
  10. qName - Query sequence name
  11. qSize - Query sequence size
  12. qStart - Alignment start position in query
  13. qEnd - Alignment end position in query
  14. tName - Target sequence name
  15. tSize - Target sequence size
  16. tStart - Alignment start position in target
  17. tEnd - Alignment end position in target
  18. blockCount - Number of blocks in the alignment (a block contains no gaps)
  19. blockSizes - Comma-separated list of sizes of each block
  20. qStarts - Comma-separated list of starting positions of each block in query
  21. tStarts - Comma-separated list of starting positions of each block in target

Example:
Here is an example of an annotation track in PSL format. Note that line breaks
have been inserted into the PSL lines in this example for documentation display
purposes. Click here for a copy of this example that can be pasted into the
browser without editing.

track name=fishBlats description="Fish BLAT" useScore=1
59 9 0 0 1 823 1 96 +- FS_CONTIG_48080_1 1955 171 1062 chr22
    47748585 13073589 13073753 2 48,20,  171,1042,  34674832,34674976,
59 7 0 0 1 55 1 55 +- FS_CONTIG_26780_1 2825 2456 2577 chr22
    47748585 13073626 13073747 2 21,45,  2456,2532,  34674838,34674914,
59 7 0 0 1 55 1 55 -+ FS_CONTIG_26780_1 2825 2455 2676 chr22
    47748585 13073727 13073848 2 45,21,  249,349,  13073727,13073827,

Be aware that the coordinates for a negative strand in a PSL line are handled
in a special way. In the qStart and qEnd fields, the coordinates indicate the
position where the query matches from the point of view of the forward strand,
even when the match is on the reverse strand. However, in the qStarts list, the
coordinates are reversed.

Example:
Here is a 30-mer containing 2 blocks that align on the minus strand and 2 blocks
that align on the plus strand (this sometimes can happen in response to assembly
errors):

0         1         2         3 tens position in query
0123456789012345678901234567890 ones position in query
            ++++          +++++ plus strand alignment on query
    --------    ----------      minus strand alignment on query

Plus strand:
     qStart=12
     qEnd=31
     blockSizes=4,5
     qStarts=12,26

Minus strand:
     qStart=4
     qEnd=26
     blockSizes=10,8
     qStarts=5,19

Essentially, the minus strand blockSizes and qStarts are what you would get if you reverse-complemented the query. However, the qStart and qEnd are not reversed. To convert one to the other:

     qStart = qSize - revQEnd
     qEnd = qSize - revQStart
"""


"""
Example of "bowtie2-or-bwa.sam"


2L1/1	16	ENSG00000143924|ENSG00000171094|163199	131998	0	46M34S	*	0	0	AATAATTCTGTGGGATCATGATCTGAATCCTGAAAGAGAAATAGAGTTTAGTGCTTCAAGGGCCAGGCTGCCAGGCCATG	D@FEECEHA=;D>FD<CHCAC@GGHIIHIGGCHCHEIHGEGHGEBC3@FD;9<GGEGIIIIIGIIGGDDFB<EDBB;@?@	AS:i:92	XS:i:92	XN:i:0	XM:i:0	XO:i:0	XG:i:0	NM:i:0	MD:Z:46	YT:Z:UU
2L1/1	272	ENSG00000171094|ENSG00000143924|728793	860791	0	46M34S	*	0	0	AATAATTCTGTGGGATCATGATCTGAATCCTGAAAGAGAAATAGAGTTTAGTGCTTCAAGGGCCAGGCTGCCAGGCCATG	D@FEECEHA=;D>FD<CHCAC@GGHIIHIGGCHCHEIHGEGHGEBC3@FD;9<GGEGIIIIIGIIGGDDFB<EDBB;@?@	AS:i:92	XS:i:92	XN:i:0	XM:i:0	XO:i:0	XG:i:0	NM:i:0	MD:Z:46	YT:Z:UU
2L1/1	272	ENSG00000143924|ENSG00000171094|163199	861182	0	48S32M	*	0	0	AATAATTCTGTGGGATCATGATCTGAATCCTGAAAGAGAAATAGAGTTTAGTGCTTCAAGGGCCAGGCTGCCAGGCCATG	D@FEECEHA=;D>FD<CHCAC@GGHIIHIGGCHCHEIHGEGHGEBC3@FD;9<GGEGIIIIIGIIGGDDFB<EDBB;@?@	AS:i:64	XS:i:92	XN:i:0	XM:i:0	XO:i:0	XG:i:0	NM:i:0	MD:Z:32	YT:Z:UU
2L1/1	272	ENSG00000171094|ENSG00000143924|728793	697983	0	48S32M	*	0	0	AATAATTCTGTGGGATCATGATCTGAATCCTGAAAGAGAAATAGAGTTTAGTGCTTCAAGGGCCAGGCTGCCAGGCCATG	D@FEECEHA=;D>FD<CHCAC@GGHIIHIGGCHCHEIHGEGHGEBC3@FD;9<GGEGIIIIIGIIGGDDFB<EDBB;@?@	AS:i:64	XS:i:92	XN:i:0	XM:i:0	XO:i:0	XG:i:0	NM:i:0	MD:Z:32	YT:Z:UU



The same converted to PSL (by sam2psl.py and sorted):

46	34	0	0	0	0	0	0	-	2L1/1	80	0	46	ENSG00000143924|ENSG00000171094|163199	891992	131997	132043	1	46,	0,	131997,
32	48	0	0	0	0	0	0	-	2L1/1	80	48	80	ENSG00000143924|ENSG00000171094|163199	891992	861181	861213	1	32,	48,	861181,
46	34	0	0	0	0	0	0	-	2L1/1	80	0	46	ENSG00000171094|ENSG00000143924|728793	891992	860790	860836	1	46,	0,	860790,
32	48	0	0	0	0	0	0	-	2L1/1	80	48	80	ENSG00000171094|ENSG00000143924|728793	891992	697982	698014	1	32,	48,	697982,




The expected output of this program would be this PSL file for the above example:

46	34	0	0	0	0	0	0	-	2L1/1	80	0	46	ENSG00000143924|ENSG00000171094|163199	891992	131997	132043	1	46,	0,	131997,
32	48	0	0	0	0	0	0	-	2L1/1	80	48	80	ENSG00000143924|ENSG00000171094|163199	891992	861181	861213	1	32,	48,	861181,
becomes
46+32	63-55	0	0	0	0	0	0	+	000B1-2	90	0	90	ENSG00000143924|ENSG00000171094|163199	105086	22877	22912	2	35,55,	0,35,	22877,21915,


46	34	0	0	0	0	0	0	-	2L1/1	80	0	46	ENSG00000171094|ENSG00000143924|728793	891992	860790	860836	1	46,	0,	860790,
32	48	0	0	0	0	0	0	-	2L1/1	80	48	80	ENSG00000171094|ENSG00000143924|728793	891992	697982	698014	1	32,	48,	697982,
becomes
46+32	43-31	0	0	0	0	0	0	-	00IUU-2	90	3	84	ENSG00000171094|ENSG00000143924|728793	179087	176519	176568	2	49,32	3,52	176519,176253,



"""

import os
import sys
import optparse
import gc
import itertools


# PSL columns
psl_matches = 0
psl_misMatches = 1
psl_repMatches = 2
psl_nCount = 3
psl_qNumInsert = 4
psl_qBaseInsert = 5
psl_tNumInsert = 6
psl_tBaseInsert = 7
psl_strand = 8
psl_qName = 9
psl_qSize = 10
psl_qStart = 11
psl_qEnd = 12
psl_tName = 13
psl_tSize = 14
psl_tStart = 15
psl_tEnd = 16
psl_blockCount = 17
psl_blockSizes = 18
psl_qStarts = 19
psl_tStarts = 20


#########################
def lines(filename):
    # it gives chunks
    fin = None
    if filename == '-':
        fin = sys.stdin
    else:
        fin = open(filename,'r')
    while True:
        lines = fin.readlines(10**8)
        if not lines:
            break
        gc.disable()
        lines = [line.rstrip('\r\n').split('\t') for line in lines if line.rstrip('\r\n')]
        gc.enable()
        for line in lines:
            yield line
    fin.close()

#########################
def index_max(values):
    return max(xrange(len(values)),key=values.__getitem__)

#########################
def chunks(psl_file, min_count = 2, ids_out = None, ref_out = None, clip_size = 10):
    # gives in a chunk the PSL files which have the same read is a QNAME
    last_qname = None
    last_tname = None
    last_strand = None
    chunk = []
    if ids_out:
        ft = open(ids_out,'w')
        fr = None
        if ref_out:
            fr = open(ref_out,'w')
        buff = []
        ref = []
        for line in lines(psl_file):
            if not chunk:
                last_qname = line[psl_qName]
                last_tname = line[psl_tName]
            if last_qname != line[psl_qName] or last_tname != line[psl_tName] or last_strand != line[psl_strand]:
                # the bin is full and now analyze it
                if len(chunk) > min_count - 1:
                    yield chunk
                elif len(chunk) == 1: #and int(chunk[0][psl_qSize]) + int(chunk[0][psl_qStart]) - int(chunk[0][psl_qEnd]) > clip_size - 1:
                    #z = "%s\t%s\t%s\t%s\t%s\n" % (chunk[0][psl_qName],chunk[0][psl_qSize],chunk[0][psl_strand],chunk[0][psl_qStart],chunk[0][psl_qEnd])
                    nn = int(chunk[0][psl_qSize])
                    pqs = int(chunk[0][psl_qStart])
                    pqe = int(chunk[0][psl_qEnd])
                    if nn + pqs - pqe > clip_size - 1:
                        if chunk[0][psl_blockCount] == '1':
                            p2 = pqs
                            p3 = pqe
                        else:
                            # here are more blocks
                            # find the largest block
                            blen = map(int,chunk[0][psl_blockSizes][:-1].split(','))
                            qstart = map(int,chunk[0][psl_qStarts][:-1].split(','))
                            bidx = index_max(blen)
                            p2 = qstart[bidx]
                            p3 = p2 + blen[bidx]
                        if chunk[0][psl_strand] == "-":
                            (p2,p3) = (nn - p3,nn - p2)
                        cut = -1
                        if p2 >= clip_size:
                            cut = p2 - 1
                        elif nn - p3 >= clip_size:
                            cut = p3
                        if cut != -1:
                            z = "%s\t%d\n" % (chunk[0][psl_qName],cut)
                            if not(buff and buff[-1] == z):
                                buff.append(z)
                                if len(buff) > 100000:
                                    ft.writelines(buff)
                                    buff = []
                                if fr:
                                    ref.append(chunk[0][psl_tName]+'\n')
                                    if len(ref) > 100000:
                                        fr.writelines(ref)
                                        ref = []
                last_qname = line[psl_qName]
                last_tname = line[psl_tName]
                last_strand = line[psl_strand]
                chunk = []
            chunk.append(line)
        if buff:
            ft.writelines(buff)
            buff = []
        ft.close()
        if fr:
            if ref:
                fr.writelines(ref)
                ref = []
            fr.close()
    else:
        for line in lines(psl_file):
            if not chunk:
                last_qname = line[psl_qName]
                last_tname = line[psl_tName]
            if last_qname != line[psl_qName] or last_tname != line[psl_tName] or last_strand != line[psl_strand]:
                # the bin is full and now analyze it
                if len(chunk) > min_count - 1:
                    yield chunk
                last_qname = line[psl_qName]
                last_tname = line[psl_tName]
                last_strand = line[psl_strand]
                chunk = []
            chunk.append(line)
    if chunk:
        yield chunk

#########################
def merge_local_alignment_sam(psl_in, psl_ou, ids_ou = None, ref_ou = None, min_clip = 10, remove_extra = False):
    #
    psl = []
    fou = None
    if psl_ou == '-':
        fou = sys.stdout
    else:
        fou = open(psl_ou,'w')

    limit_psl = 10**5

    for bucket in chunks(psl_in, min_count = 2, ids_out = ids_ou, ref_out = ref_ou, clip_size = min_clip):

        for box in itertools.combinations(bucket,2):

            if box[0][psl_strand] == box[1][psl_strand]:

                merged = None

                temp = box[0][:]

                r1_start = int(box[0][psl_qStart])
                r2_start = int(box[1][psl_qStart])
                if r1_start > r2_start:
                    box = (box[1],box[0])

                r1_start = int(box[0][psl_qStart])
                r1_end = int(box[0][psl_qEnd])
                r2_start = int(box[1][psl_qStart])
                r2_end = int(box[1][psl_qEnd])

                t1_start = int(box[0][psl_tStart])
                t1_end = int(box[0][psl_tEnd])
                t2_start = int(box[1][psl_tStart])
                t2_end = int(box[1][psl_tEnd])

                if t1_start > t2_start:
                    continue

                wiggle_gap = 9
                wiggle_overlap = 17
                if r1_end + wiggle_gap > r2_start and r1_end < r2_start:
                    dif = r2_start - r1_end

                    # extend the first
                    #box[0][psl_matches] = str(int(box[0][psl_matches]))
                    #box[0][psl_misMatches] = str(int(box[0][psl_misMatches]) + dif)

                    box[0][psl_qEnd] = str(int(box[0][psl_qEnd]) + dif)
                    box[0][psl_tEnd] = str(int(box[0][psl_tEnd]) + dif)

                    t = box[0][psl_blockSizes].split(',')
                    t[-2] = str(int(t[-2]) + dif)
                    box[0][psl_blockSizes] = ','.join(t)

                    # recompute 1
                    r1_start = int(box[0][psl_qStart])
                    r1_end = int(box[0][psl_qEnd])

                    t1_start = int(box[0][psl_tStart])
                    t1_end = int(box[0][psl_tEnd])

                elif r1_end > r2_start and r1_end < r2_start + wiggle_overlap:
                    dif = r1_end - r2_start

                    if r2_end - r2_start - dif > min_clip:
                        # cut the second
                        box[1][psl_matches] = str(int(box[1][psl_matches]) - dif)
                        box[1][psl_misMatches] = str(int(box[1][psl_misMatches]) + dif)

                        box[1][psl_qStart] = str(int(box[1][psl_qStart]) + dif)
                        box[1][psl_tStart] = str(int(box[1][psl_tStart]) + dif)

                        t = box[1][psl_blockSizes].split(',')
                        t[0] = str(int(t[0]) - dif)
                        box[1][psl_blockSizes] = ','.join(t)

                        t = box[1][psl_qStarts].split(',')
                        t[0] = str(int(t[0]) + dif)
                        box[1][psl_qStarts] = ','.join(t)

                        t = box[1][psl_tStarts].split(',')
                        t[0] = str(int(t[0]) + dif)
                        box[1][psl_tStarts] = ','.join(t)

                        # recompute 2
                        r2_start = int(box[1][psl_qStart])
                        r2_end = int(box[1][psl_qEnd])

                        t2_start = int(box[1][psl_tStart])
                        t2_end = int(box[1][psl_tEnd])
                    else:
                        box[0][psl_matches] = str(int(box[0][psl_matches]) - dif)
                        box[0][psl_misMatches] = str(int(box[0][psl_misMatches]) + dif)

                        box[0][psl_qEnd] = str(int(box[0][psl_qEnd]) - dif)
                        box[0][psl_tEnd] = str(int(box[0][psl_tEnd]) - dif)

                        t = box[0][psl_blockSizes].split(',')
                        t[-2] = str(int(t[-2]) - dif)
                        box[0][psl_blockSizes] = ','.join(t)

                        # recompute 1
                        r1_start = int(box[0][psl_qStart])
                        r1_end = int(box[0][psl_qEnd])

                        t1_start = int(box[0][psl_tStart])
                        t1_end = int(box[0][psl_tEnd])

                if r1_end <= r2_start and t1_end <= t2_start: #and box[0][psl_strand] == "+" :

                    temp[psl_matches] = int(box[0][psl_matches]) + int(box[1][psl_matches])
                    temp[psl_misMatches] = int(box[0][psl_misMatches]) - int(box[1][psl_matches])

                    temp[psl_qNumInsert] = int(box[0][psl_qNumInsert]) + int(box[1][psl_qNumInsert])
                    temp[psl_qBaseInsert] = int(box[0][psl_qBaseInsert]) + int(box[1][psl_qBaseInsert])
                    temp[psl_tNumInsert] = int(box[0][psl_tNumInsert]) + int(box[1][psl_tNumInsert])
                    temp[psl_tBaseInsert] = int(box[0][psl_tBaseInsert]) + int(box[1][psl_tBaseInsert])

                    temp[psl_qStart] = r1_start
                    temp[psl_qEnd] = r2_end

                    temp[psl_tStart] = t1_start
                    temp[psl_tEnd] = t2_end

                    temp[psl_blockCount] = int(box[0][psl_blockCount]) + int(box[1][psl_blockCount])
                    temp[psl_blockSizes] = box[0][psl_blockSizes] + box[1][psl_blockSizes]

                    temp[psl_qStarts] = box[0][psl_qStarts] + box[1][psl_qStarts]

                    temp[psl_tStarts] = box[0][psl_tStarts] + box[1][psl_tStarts]
                    temp[psl_tNumInsert] = '1'

                    merged = temp

#                elif r1_end <= r2_start and box[0][psl_strand] == "-" and t2_end <= t1_start:
#
#                    temp[psl_matches] = int(box[0][psl_matches]) + int(box[1][psl_matches])
#                    temp[psl_misMatches] = int(box[0][psl_misMatches]) - int(box[1][psl_matches])
#
#                    temp[psl_qNumInsert] = int(box[0][psl_qNumInsert]) + int(box[1][psl_qNumInsert])
#                    temp[psl_qBaseInsert] = int(box[0][psl_qBaseInsert]) + int(box[1][psl_qBaseInsert])
#                    temp[psl_tNumInsert] = int(box[0][psl_tNumInsert]) + int(box[1][psl_tNumInsert])
#                    temp[psl_tBaseInsert] = int(box[0][psl_tBaseInsert]) + int(box[1][psl_tBaseInsert])
#
#                    temp[psl_qStart] = r1_start
#                    temp[psl_qEnd] = r2_end
#
#                    temp[psl_tStart] = t2_start
#                    temp[psl_tEnd] = t1_end
#
#                    temp[psl_blockCount] = int(box[0][psl_blockCount]) + int(box[1][psl_blockCount])
#                    temp[psl_blockSizes] = box[1][psl_blockSizes] + box[0][psl_blockSizes]
#
#                    temp[psl_qStarts] = box[0][psl_qStarts] + box[1][psl_qStarts]
#
#                    temp[psl_tStarts] = box[1][psl_tStarts] + box[0][psl_tStarts]
#                    temp[psl_tNumInsert] = '1'
#
#                    merged = temp

                if merged:
                    gc.disable()
                    psl.append(map(str,merged))
                    gc.enable()
                    if len(psl) >= limit_psl:
                        if remove_extra:
                            for line in psl:
                                line[9] = line[9].partition("__")[0]
                        fou.writelines(['\t'.join(line)+'\n' for line in psl])
                        psl = []
    # output PSL
    if psl:
        for line in psl:
            line[9] = line[9].partition("__")[0]
        fou.writelines(['\t'.join(line)+'\n' for line in psl])
    #



#########################
if __name__ == '__main__':

    #command line parsing

    usage = "%prog [options]"
    description = """It takes as input a PSL formated file generated which has been converted from
SAM file (that is sorted output of sam2psl.py) generated by BOWTIE2/BWA aligners.
Here the assumption is that the PSL is sorted by columns 10, 14, 12, and 13."""
    version = "%prog 0.11 beta"

    parser = optparse.OptionParser(
        usage = usage,
        description = description,
        version = version)

    parser.add_option("--input","-i",
                      action="store",
                      type="string",
                      dest="input_filename",
                      help="""The input file in PSL format.""")

    parser.add_option("--output","-o",
                      action="store",
                      type="string",
                      dest="output_filename",
                      help="""The output PSL file containing the contigs with the best alignment which must be unique.""")

    parser.add_option("--clipped-reads-ids","-r",
                      action="store",
                      type="string",
                      dest="output_ids_filename",
                      help="""The output text file containing ids of reads which have unmapped clippings.""")

    parser.add_option("--clipped-reads-refs","-s",
                      action="store",
                      type="string",
                      dest="output_ref_filename",
                      help="""The output text file containing reference ids on which the clipped reads are mapped.""")

    parser.add_option("--clip-min","-c",
                      action = "store",
                      type = "int",
                      dest = "min_clip",
                      default = 10,
                      help = """Minimum size of clipping which will be written in the output given by '--reads-ids'. Default is '%default'.""")

    parser.add_option("--remove-extra","-x",
                      action = "store_true",
                      dest = "remove_extra",
                      default = False,
                      help = """It removes from the string of reads ids everything what is after '__' and also '__'. Default is '%default'.""")



    (options,args) = parser.parse_args()

    # validate options
    if not (options.input_filename and
            options.output_filename
            ):
        parser.print_help()
        sys.exit(1)

    # running
    merge_local_alignment_sam(options.input_filename,
                              options.output_filename,
                              options.output_ids_filename,
                              options.output_ref_filename,
                              options.min_clip,
                              remove_extra = options.remove_extra)
#
