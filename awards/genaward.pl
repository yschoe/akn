#!/usr/bin/perl

while (<STDIN>) {
 chop;
 $line =$_;
 $line =~ s/uni/University/g;
 $line =~ s/JHU/Johns Hopkins University/g;
 $line =~ s/SNU/Seoul National University/g;
 ($name,$affil) = split(/:/,$line);
 print '<p class="aw_name">'.$name.'</p>'."\n";
 print '<p class="aw_aff">'.$affil.'</p>'."\n\n";
}
