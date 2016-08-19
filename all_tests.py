#!/usr/bin/env python

# import all the lovely files
import unittest

from test.cds_tests import suite as cds_tests
from test.exon_tests import suite as exon_tests
from test.fasta_reader_tests import suite as fasta_reader_tests
from test.filter_manager_tests import suite as filter_manager_tests
from test.filters_tests import suite as filters_tests
from test.gene_part_tests import suite as gene_part_tests
from test.gene_tests import suite as gene_tests
from test.gff_reader_tests import suite as gff_reader_tests
from test.seq_helper_tests import suite as seq_helper_tests
from test.sequence_tests import suite as sequence_tests
from test.stats_manager_tests import suite as stats_manager_tests
from test.translator_tests import suite as translator_tests
from test.xrna_tests import suite as xrna_tests

# collect suites in a TestSuite object
suite = unittest.TestSuite()
suite.addTest(fasta_reader_tests())
suite.addTest(gene_part_tests())
suite.addTest(xrna_tests())
suite.addTest(gene_tests())
suite.addTest(translator_tests())
suite.addTest(gff_reader_tests())
suite.addTest(sequence_tests())
suite.addTest(filter_manager_tests())
suite.addTest(filters_tests())
suite.addTest(stats_manager_tests())
suite.addTest(seq_helper_tests())
suite.addTest(cds_tests())
suite.addTest(exon_tests())

# run suite
unittest.TextTestRunner(verbosity=2).run(suite)
