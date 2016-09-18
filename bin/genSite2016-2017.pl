#!/usr/bin/env perl

use v5.020;
use strict;
use warnings;
use utf8;

binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";
binmode STDIN,  ":encoding(UTF-8)";

use Data::Printer;
use Excel::Writer::XLSX;
use File::Spec;
use FindBin;
use Getopt::Long;
use Spreadsheet::XLSX;
use Template;

use lib "$FindBin::Bin/../lib";

use DartSense::Match;
use DartSense::Player;

use experimental 'signatures';
no warnings "experimental::signatures";

my $options = { file => '', };
GetOptions( "file=s" => \$options->{file}, );

die unless ( $options->{file} );

my $file  = File::Spec->rel2abs( $options->{file} );
my $excel = Spreadsheet::XLSX->new($file);

my $playerslookup = {};
my @matches;
my @players;

my $lastdate;
foreach my $sheet ( @{ $excel->{Worksheet} } ) {
    my $date  = $sheet->{Name};
    my $i     = 0;
    my %names = map { $_->{Val} => $i++ } @{ $sheet->{Cells}->[0] };
    foreach my $row ( 1 .. $sheet->{MaxRow} ) {
        my $matchdata = {
            date     => $date,
            baan     => $sheet->{Cells}->[$row]->[ $names{Baan} ]->{Val},
            ronde    => $sheet->{Cells}->[$row]->[ $names{Ronde} ]->{Val},
            speler1  => $sheet->{Cells}->[$row]->[ $names{Speler1} ]->{Val},
            speler2  => $sheet->{Cells}->[$row]->[ $names{Speler2} ]->{Val},
            legs1    => $sheet->{Cells}->[$row]->[ $names{Legs1} ]->{Val},
            legs2    => $sheet->{Cells}->[$row]->[ $names{Legs2} ]->{Val},
            lollies1 => $sheet->{Cells}->[$row]->[ $names{Lollies1} ]->{Val}
                // 0,
            lollies2 => $sheet->{Cells}->[$row]->[ $names{Lollies2} ]->{Val}
                // 0,
            max1 => $sheet->{Cells}->[$row]->[ $names{Max1} ]->{Val} || 0,
            max2 => $sheet->{Cells}->[$row]->[ $names{Max2} ]->{Val} || 0,
            finishes1 => [
                split ',',
                $sheet->{Cells}->[$row]->[ $names{Finishes1} ]->{Val} // ''
            ],
            finishes2 => [
                split ',',
                $sheet->{Cells}->[$row]->[ $names{Finishes2} ]->{Val} // ''
            ],
        };

        $matchdata->{player1} = getPlayer( $matchdata->{speler1} );
        $matchdata->{player2} = getPlayer( $matchdata->{speler2} );

        push @matches, $matchdata;
        $lastdate = $date;
    }
}

# p @matches;

foreach my $matchdata (@matches) {
    parsePlayer( 1, $matchdata );
    parsePlayer( 2, $matchdata );
}

my @players_stand = sort { $a->{matchcount} <=> $b->{matchcount} } @players;
@players_stand = sort { $b->{score} <=> $a->{score} } @players_stand;

my @players_180
    = sort { $b->{max} <=> $a->{max} } grep { $_->{max} } @players;
my @players_finishes = sort { $b->{finishes}->[0] <=> $a->{finishes}->[0] }
    grep { @{ $_->{finishes} } } @players;

unlink("/tmp/standen_$lastdate.xlsx");
my $workbook = Excel::Writer::XLSX->new("/tmp/standen_$lastdate.xlsx");

{
    my $worksheet_stand = $workbook->add_worksheet('stand');
    $worksheet_stand->write_row( 0, 0,
        [ 'Stand', 'Naam', 'Punten', 'Wedstrijden', 'Gemiddeld', ] );
    my $i = 1;
    foreach my $player (@players_stand) {
        $worksheet_stand->write( $i, 0, $i );
        $worksheet_stand->write( $i, 1, $player->{name} );
        $worksheet_stand->write( $i, 2, $player->{score} );
        $worksheet_stand->write( $i, 3, $player->{matchcount} );
        $worksheet_stand->write( $i, 4,
            sprintf( "%0.2f", $player->{score} / $player->{matchcount} ) );
        $i++;
    }
}

{
    my $worksheet_180 = $workbook->add_worksheet('180');
    $worksheet_180->write_row( 0, 0, [ '', 'Naam', 'x 180', ] );
    my $i = 1;
    foreach my $player (@players_180) {
        $worksheet_180->write( $i, 0, $i );
        $worksheet_180->write( $i, 1, $player->{name} );
        $worksheet_180->write( $i, 2, $player->{max} );
        $i++;
    }
}
{
    my $worksheet_finish = $workbook->add_worksheet('finish');
    $worksheet_finish->write_row( 0, 0, [ '', 'Naam', 'Finishes 100+', ] );
    my $i = 1;
    foreach my $player (@players_finishes) {
        $worksheet_finish->write( $i, 0, $i );
        $worksheet_finish->write( $i, 1, $player->{name} );
        $worksheet_finish->write( $i, 2,
            join( ', ', @{ $player->{finishes} } ) );
        $i++;
    }
}
{
    my @players_lollies = sort { $b->{lollies} <=> $a->{lollies} }
        grep { $_->{lollies} } @players;
    my $worksheet_lolly = $workbook->add_worksheet('lolly');
    $worksheet_lolly->write_row( 0, 0, [ '', 'Naam', "Lolly's", ] );
    my $i = 1;
    foreach my $player (@players_lollies) {
        $worksheet_lolly->write( $i, 0, $i );
        $worksheet_lolly->write( $i, 1, $player->{name} );
        $worksheet_lolly->write( $i, 2, $player->{lollies} );
        $i++;
    }
}

$workbook->close();

exit;

sub getPlayer {
    my $name   = shift;
    my $player = $playerslookup->{$name};
    if ( !$player ) {
        $player = DartSense::Player->new( { name => $name } );
        $playerslookup->{$name} = $player;
        push @players, $player;
    }

    return $player;
}

sub parsePlayer {
    my $nr        = shift;
    my $matchdata = shift;

    my $own = $nr;
    my $other = abs( 1 - $nr ) || 2;

    my $player = $matchdata->{"player$own"};
    $player->{matchcount}++;

    if ( $matchdata->{"legs$own"} == 2 && $matchdata->{"legs$other"} == 0 ) {
        $player->{score} += 5;
    }
    elsif ( $matchdata->{"legs$own"} == 2 && $matchdata->{"legs$other"} == 1 )
    {
        $player->{score} += 3;
    }
    elsif ( $matchdata->{"legs$own"} == 1 && $matchdata->{"legs$other"} == 2 )
    {
        $player->{score} += 1;
    }

    if ( my $max = $matchdata->{"max$own"} ) {
        $player->{max} += $max;

        #elke 180 is extra punt
        $player->{score} += $max;
    }

    if ( my $lollies = $matchdata->{"lollies$own"} ) {
        $player->{lollies} += $lollies;
    }

    for my $finish ( @{ $matchdata->{"finishes$own"} } ) {
        push @{ $player->{finishes} }, $finish;

        if ( $finish >= 100 && $finish <= 110 ) {
            $player->{score} += 1;
        }
        elsif ( $finish >= 111 && $finish <= 120 ) {
            $player->{score} += 2;
        }
        elsif ( $finish >= 121 && $finish <= 130 ) {
            $player->{score} += 3;
        }
        elsif ( $finish >= 131 && $finish <= 140 ) {
            $player->{score} += 4;
        }
        elsif ( $finish >= 141 && $finish <= 150 ) {
            $player->{score} += 5;
        }
        elsif ( $finish >= 151 && $finish <= 158 ) {
            $player->{score} += 6;
        }
        elsif ( $finish >= 160 && $finish <= 167 ) {
            $player->{score} += 7;
        }
        elsif ( $finish == 170 ) {
            $player->{score} += 10;
        }
    }
}

