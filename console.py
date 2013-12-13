#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import cmd
import readline
import sys
from src.console_controller import ConsoleController

def try_catch(command, args):
    try:
        if args is not None:
            return command(args) 
        else:
            return command()
    except:
        e = sys.exc_info()[0]
        print("Sorry, that command raised an exception. Here's what I know:\n")
        print(e)


class GagCmd(cmd.Cmd):

## Setup, loading and saving sessions, exit, etc.

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "GAG> "
        readline.set_history_length(1000)
        try:
            readline.read_history_file('.gaghistory')
        except IOError:
            sys.stderr.write("No .gaghistory file available...")
        self.controller = ConsoleController() 

    def precmd(self, line):
        readline.write_history_file('.gaghistory')
        return cmd.Cmd.precmd(self, line)

    def postcmd(self, stop, line):
        if hasattr(self, 'output') and self.output:
            print self.output
            self.output = None
        return stop

    def parseline(self, line):
        if '|' in line:
            commands = ['']
            quotes = ''
            for c in line:
                if c == '|' and quotes == '':
                    commands[-1] = commands[-1].strip()
                    commands.append('')
                else:
                    if quotes == '' and (c == "'" or c == '"'):
                        quotes = c
                    elif quotes == c:
                        quotes = ''
                    commands[-1] += c
            commands[-1] = commands[-1].strip()
            if len(commands) > 1:
                return 'pipe', commands, line
        return cmd.Cmd.parseline(self, line)

    def do_pipe(self, args):
        buf = None
        for arg in args:
            if buf:
                self.controller.input = buf
            else:
                self.controller.input = ''
            self.output = ''
            self.onecmd(arg)
            if hasattr(self, 'output') and self.output:
                buf = self.output

    def help_barfsession(self):
        print("Usage: barfsession <directory>\n")
        print("Writes gff, fasta and trinotate files to the specified directory.\n")

    def do_barfsession(self, line):
        try_catch(self.controller.barf_session, line)

    def help_loadsession(self):
        print("Usage: loadsession <directory>\n")
        print("Reads in a gff, fasta and trinotate file from the specified directory.\n")

    def do_loadsession(self, line):
        try_catch(self.controller.load_session, line)

    def help_exit(self):
        print("Exit this console.\n")

    def do_exit(self, line):
        return True

    def do_ls(self, line):
        self.output = self.controller.ls(line)

    def do_cat(self, line):
        self.output = self.controller.cat(line)

    def do_grep(self, line):
        self.output = self.controller.grep(line)

    def do_sed(self, line):
        self.output = self.controller.sed(line)

## Assorted utilities

    def help_addseq(self):
        print("Usage: addseq <seqid>\n")

    def do_addseq(self, line):
        try_catch(self.controller.add_seq, line)

    def help_addtemplatefile(self):
        print("Usage: addtemplatefile <path/to/file>\n")

    def do_addtemplatefile(self, line):
        try_catch(self.controller.add_template_file, line)

    def help_status(self):
        print("Usage: status\n")
        print("Gives a brief summary of what's in memory\n")

    def do_status(self, line):
        print(try_catch(self.controller.status, None))


## Reading in files

    def help_readfasta(self):
        print("Usage: readfasta <file_name>\n")
        print("Read the fasta file. Any unsaved changes")
        print("to the currently loaded fasta will be lost.\n")

    def do_readfasta(self, line):
        try_catch(self.controller.read_fasta, line)

    def help_readgff(self):
        print("Usage: readgff <file_name>\n")
        print("Read the gff file. Any unsaved changes")
        print("to the currently loaded gff will be lost.\n")

    def do_readgff(self, line):
        try_catch(self.controller.read_gff, line)

    def help_readtrinotate(self):
        print("Usage: readtrinotate <file_name>\n")
        print("Read annotations from a trinotate file.\n")

    def do_readtrinotate(self, line):
        try_catch(self.controller.read_trinotate, line)


## Manipulate genome

    def help_applybed(self):
        print("Usage: applybed <file_name>\n")
        print("Applies a bed file to the data. This will")
        print("trim out any sequences that aren't in the")
        print("ranges of the bed file and automagically")
        print("update the GFF file accordingly.\n")

    def do_applybed(self, line):
        try_catch(self.controller.apply_bed, line)

    def help_subsetfasta(self):
        print("Usage: subsetfasta\n")
        print("(You must first use 'addseq' to create a list of sequence ids to keep)\n")

    def do_subsetfasta(self, line):
        try_catch(self.controller.subset_fasta, None)

    def help_subsetgff(self):
        print("Usage: subsetgff\n")
        print("(You must first use 'addseq' to create a list of sequence ids to keep)\n")

    def do_subsetgff(self, line):
        try_catch(self.controller.subset_gff, None)

    def help_ducttapeseqframes(self):
        print("Usage: ducttapeseqframes <mrna_id> [another_gene_id] [etc.]\n")
        print("Checks the translation of the coding sequence of each supplied mrna against the expected protein sequence from Trinotate.\n")
        print("If it doesn't match, performs a six-frame translation and chooses the correct frame. Adjusts the gff accordingly.\n")

    def do_ducttapeseqframes(self, line):
        try_catch(self.controller.duct_tape_seq_frames, line)


## Output info to console

    def help_barfgenegff(self):
        print("Usage: barfgenegff <gene_id>\n")
        print("Prints gff entry for corresponding gene to console.\n")

    def do_barfgenegff(self, line):
        self.output = try_catch(self.controller.barf_gff, line)

    def help_barfseq(self):
        print("Usage: barfseq <seq_id> <start_index> <end_index>\n")
        print("Prints (sub)sequence to console.\n")

    def do_barfseq(self, line):
        self.output = try_catch(self.controller.barf_seq, line)

    def help_barfgenetbl(self):
        print("TODO")   # TODO

    def do_barfgenetbl(self, line):
        self.output = try_catch(self.controller.barf_gene_tbl, line)


## Output info to file

    def help_writetbl(self):
        print("Usage: writetbl <file_name>\n")
        print("Write a sweet feature table to the specified file.\n")

    def do_writetbl(self, line):
        try_catch(self.controller.write_tbl, line)

    def help_writefasta(self):
        print("Usage: writefasta <file_name>\n")
        print("Writes current fasta to specified file. If you've applied a bed or used 'subsetfasta', the modified version is written.\n")

    def do_writefasta(self, line):
        try_catch(self.controller.write_fasta, line)


## tbl2asn integration

    def help_preptbl2asn(self):
        print("Usage: preptbl2asn <path>\n")
        print("Creates a new folder, links current fasta and template file, writes current genes to .tbl file.\n")

    def do_preptbl2asn(self, line):
        try_catch(self.controller.prep_tbl2asn, line)

    def help_settbl2asnexecutable(self):
        print("Usage: settbl2asnexecutable <path/to/tbl2asn>\n")

    def do_settbl2asnexecutable(self, line):
        try_catch(self.controller.set_tbl2asn_executable, line)

    def help_runtbl2asn(self):
        print("Usage: runtbl2asn <path>\n")
        print("Runs tbl2asn executable in the folder provided. Folder must contain files with extensions .fsa, .sbt and .tbl, and tbl2asn executable must be set.\n")
        print("(See preptbl2asn, settbl2asnexecutable)\n")

    def do_runtbl2asn(self, line):
        try_catch(self.controller.run_tbl2asn, line)



########################################################################

if __name__ == '__main__':
    GagCmd().cmdloop("Welcome to the GAG console!")