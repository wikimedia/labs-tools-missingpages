#!/usr/bin/perl

# This script is released under terms of GNU GPL license
# See file COPYING for more information

# Nejvice chybejici clanky s ignorovanim odkazu ze sablon

open X, "<date.txt";
$date = <X>;
close X;
$date =~ s/ /&nbsp;/g;
open O, ">missl";
print O <<EOF;
<!--
 Tento seznam je generován skriptem a čas od času je automaticky přepsán.
 Needitujte ho, vaše změny budou přepsány
 Editovat lze podstránky /head (hlavička) a /tail (patička)
 Tyto jsou do stránky vkládány a jejich obsah není skriptem nijak měněn.
 -->
{{/head|$date}}
<ol>
EOF

%q = ();

open X, "<MISSLINK.txt";
while (<X>) {
    if (/^(\d+)\t(.*)/) {
        $n = $1;
        next if ( $n < 6 );
        $no   = $n;
        $v    = $2;
        $nkey = 1000000 - $n;
        $k    = "$nkey/$v";

        #$q{$k} = "# [[$v]] ($no)\n";
        #$q{$k} = "{{subst:Stránka|$v|<li>| ($no)</li>}}";
        $q{$k} = "{{#ifexist:$v | |<li>[[$v]] ([[Special:Whatlinkshere/$v|$no odkazů]])</li>\n}}";
    }
}
close X;
$iii = 0;
@kk  = sort keys %q;
foreach my $i (@kk) {
    $iii++;
    print O $q{$i};
    last if ( $iii == 1000 );
}

print O <<EOF;
</ol>
{{/tail}}
EOF

