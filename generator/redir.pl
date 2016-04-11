#!/usr/bin/perl

# This script is released under terms of GNU GPL license
# See file COPYING for more information

# Nejvice odkazovane redirecty

open X, "<date.txt";
$date = <X>;
close X;
$date =~ s/ /&nbsp;/g;
open O, ">redirl";
print O <<EOF;
<!--
 Tento seznam je generován skriptem a čas od času je automaticky přepsán.
 Needitujte ho, vaše změny budou přepsány
 Editovat lze podstránky /h (hlavička) a /p (patička)
 Tyto jsou do stránky vkládány a jejich obsah není skriptem nijak měněn.
 -->
{{/h|$date}}
EOF

%q = ();

my $sum = 0;
open X, "<REDIRLIST.txt";
while (<X>) {
    if (/^(\d+)\t(.*)\t(.*)/) {
        $n  = $1;
        $no = $n;
        $sum += $no;
        $v   = $2;
        $tgt = $3;

        #next if (($v=~/^\d+\.\s*(prosince|listopadu|dubna|března|července|srpna|května|října|ledna|června|února)/));
        $nkey = 1000000 - $n;
        $k    = "$nkey/$v";
        $q{$k} = "# [[$v]] ([[Special:Whatlinkshere/$v|$no odkazů]]), odkazuje na [[$tgt]]\n";
    }
}
close X;
print O
"\nV celé české wikipedii je celkem $sum odkazů na některé z přesměrování\n\n";

$iii = 0;
@kk  = sort keys %q;
foreach my $i (@kk) {
    $iii++;
    print O $q{$i};
    last if ( $iii == 500 );
}

print O <<EOF;
{{/p}}
EOF
