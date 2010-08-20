#!/usr/bin/env perl

use lib 'lib';
use SVG::Convert;

my $converter = SVG::Convert->new();

print $converter->convert(
    format   => 'raphael',
    src_file => '/tmp/tmp.svg',
    output   => 'string',
    convert_opts => {
        id => 'raphael_canvas',
    },
);
