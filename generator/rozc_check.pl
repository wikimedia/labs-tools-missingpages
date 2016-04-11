#!/usr/bin/perl

# This script is released under terms of GNU GPL license
# See file COPYING for more information

#Chybejici primarni clanky

my $missmode = 0;
open IN, "<cswiki-latest-all-titles-in-ns0";
my %all   = ();
my %zav   = ();
my %acc   = ();
my %ros   = ();
my %black = ();
while (<IN>) {
    s#[\r\n]+##;
    s#_# #g;
    s# +# #g;
    $all{$_} = 1;
    if (/^(.*)\(([^\(\)]+)\)$/) {
        my $c  = $1;
        my $ro = $2;
        next if ( $ro =~ /^(planetka)$/ );
        $c =~ s/\s+$//g;
        next if ( $c =~ /-$/ );
        next if ( $c =~ /^$/ );
        if ( !$missmode ) { $zav{$_} = $c }
        $acc{$c} = 1;
    }
}
close IN;

open BL, "<rozc-blacklist.txt";
while (<BL>) {
    s#[\r\n]+##;
    s# +# #g;
    $black{$_} = 1;
}
close BL;

open INM, "<MISSLINK.txt";
while (<INM>) {
    s#[\r\n]+##;
    s#.*\t##g;
    s# +# #g;
    if (/^(.*)\(([^\(\)]+)\)$/) {
        my $c  = $1;
        my $ro = $2;
        next if ( $ro =~ /^(planetka)$/ );
        $c =~ s/\s+$//g;
        next if ( $c =~ /-$/ );
        next if ( $c =~ /^$/ );
        if ($missmode) {
            next if ( $acc{$c} );
        }
        else {
            next if ( !$acc{$c} );
        }

        #  print if (!$zav{$_});
        $all{$_} = 1;
        $zav{$_} = $c;
    }
}
close INM;

my @ou2 = ();

foreach my $i ( keys %zav ) {
    my $k = $zav{$i};
    next if $all{$k};
    next if $black{$i};

    #$s="{{#ifexist:$k | | #K [[$i]] neexistuje [[$k]]\n}}";
    my $s = "{{\n/záznam|$k|$i}}";

    # $s="* [[$i]]\n";
    if ($missmode) { $s = "# $i [[Special:Whatlinkshere/$i|O]]\n"; }
    push @ou2, $s;
}
open OUT, ">rozc_check.txt";
if ($missmode) {
    print OUT <<EOF;
Seznam odkazů na neexistující články s rozlišovačem, ke kterým neexistuje odpovídající článek bez rozlišovače ani jiný článek se stejným základem, ale jiným rozlišovačem

Možné řešení položek:
# dopsat rozcestník
# opravit odkaz na variantu bez rozlišovače
# nechat být, pokud je závorka součástí názvu článku

Kliknutím na modré '''O''' se zobrazí stránky, kde je odkaz uveden

Data jsou z dumpu 1.12.2006

Narozdíl od jiných podobných seznamů po opravení položka nezmizí

EOF
}
foreach my $i ( sort @ou2 ) {
    print OUT $i;
}
close OUT;
