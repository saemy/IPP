#! /usr/bin/env python

# This script is used to convert chain files into "chain tables".
# Every row in the chain table will contain an ungapped alignment block between the ref and the qry species.
# The columns will refer to chromosome, start and end coordinates of each alignment block in the ref and the qry species.

def main():
    # import packages and parse arguments
    import os, sys
    if len(sys.argv) != 3:
        print('Usage: python chainToTbl.py chain-file outfile')
        sys.exit(1)
    _, chain, outfile = sys.argv
    
    # read chain file
    with open (chain, 'r') as f:
        lines = f.readlines()

    # write coordinates of alignment blocks from chain file to outfile
    with open(outfile, 'w') as f:
        for line in lines:
            if (line.startswith('#')) or (line == '\n'):
                continue
            if line.startswith('chain'):
                line = line.strip().split()
                chrom_ref, chrom_qry, strand_qry = [line[i] for i in (2,7,9)]
                start_ref, end_ref, chrom_size_qry, start_qry, end_qry = [int(line[i]) for i in (5,6,8,10,11)]
                x_ref, x_qry = 0, 0
            else:
                line = [int(x) for x in line.strip().split()] # [block_width, gap_after_block_ref, gap_after_block_qry]
                aln_block = [chrom_ref, start_ref + x_ref, start_ref + x_ref + line[0], chrom_qry,  start_qry + x_qry, start_qry + x_qry + line[0]]
                # the chain file stores coordinates on the reverse strand from the right end, i.e. chrom_size - x.
                if strand_qry == '-':
                    start_qry_i, end_qry_i = aln_block[4:]
                    aln_block[4:] = chrom_size_qry - start_qry_i, chrom_size_qry - end_qry_i
                f.write('\t'.join(map(str, aln_block)) + '\n')
                if len(line) == 3:
                    x_ref += sum(line[:2]) # add block width plus gap size to current position
                    x_qry += sum([line[0],line[2]])

    # sort outfile
    os.system('sort -k1,1 -k2,2n %s > %s.tmp; mv %s.tmp %s' %((outfile,)*4))

if __name__ == '__main__':
    main()
