#!/usr/bin/perl

# This script is released under terms of GNU GPL license
# See file COPYING for more information

# Nejvice odkazovane rozcestniky

open X, "<date.txt";
$date = <X>;
close X;
$date =~ s/ /&nbsp;/g;
open O, ">rozcl";
print O <<EOF;
<!--
 Tento seznam je generován skriptem a čas od času je automaticky přepsán.
 Needitujte ho, vaše změny budou přepsány
 Editovat lze podstránky /hlava (hlavička) a /pata (patička)
 Tyto jsou do stránky vkládány a jejich obsah není skriptem nijak měněn.
 -->
{{/hlava|$date}}
EOF

%q = ();

my $sum = 0;
open X, "<ROZCLIST.txt";
while (<X>) {
    if (/^(\d+)\t(.*)/) {
        $n  = $1;
        $no = $n;
        $sum += $no;
        next if ( $n < 2 );
        $v     = $2;
        $nkey  = 1000000 - $n;
        $k     = "$nkey/$v";
        $q{$k} = "# [[$v]] ([[Special:Whatlinkshere/$v|$no odkazů]])\n";
    }
}
close X;

print O
"\nV celé české wikipedii je celkem $sum odkazů na některý z rozcestníků\n\n";

$iii = 0;
@kk  = sort keys %q;
foreach my $i (@kk) {
    $iii++;
    print O $q{$i};
    last if ( $iii == 500 );
}

print O <<EOF;
{{/pata}}
EOF

