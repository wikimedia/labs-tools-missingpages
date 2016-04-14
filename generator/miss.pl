#!/usr/bin/perl

# This script is released under terms of GNU GPL license
# See file COPYING for more information

# Nejvice chybejici clanky s ignorovanim odkazu ze sablon

open X, "<date.txt";
$date = <X>;
close X;
$date =~ s/ /&nbsp;/g;
open O, ">missl";

%q = ();

open X, "<MISSLINK.txt";
while (<X>) {
    if (/^(\d+)\t(.*)/) {
        $n = $1;
        next if ( $n < 1 ); # vygeneruje, pokud je alespoň 1 výskyt. Pro alespoň dva výskyty použít $n < 2
        $no   = $n;
        $v    = $2;
        $nkey = 1100000 - $n;
        $k    = "$nkey/$v";

        $q{$k} = "$v\n"; #výstupem je pouze název stránky
    }    
}
close X;
$iii = 0;
@kk  = sort keys %q;
foreach my $i (@kk) {
    $iii++;
    print O $q{$i};
}
