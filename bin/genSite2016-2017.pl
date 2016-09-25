#!/usr/bin/env perl

use v5.020;
use strict;
use warnings;
use utf8;

binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";
binmode STDIN,  ":encoding(UTF-8)";

use Data::Printer;
use DateTime;
use Excel::Writer::XLSX;
use File::Spec;
use FindBin;
use Getopt::Long;
use HTML::Table;
use Spreadsheet::XLSX;
use Template;
use WWW::Mechanize;
use YAML 'LoadFile';

use lib "$FindBin::Bin/../lib";

use DartSense::Match;
use DartSense::Player;

use experimental 'signatures';
no warnings "experimental::signatures";

my $options = { file => '', updatesite => 0 };
GetOptions(
    "file=s"     => \$options->{file},
    "updatesite" => \$options->{updatesite},
);

die unless ( $options->{file} );

my $now = DateTime->now(
    time_zone => DateTime::TimeZone->new( name => 'local' ) );
my $updatetime = $now->dmy . ' ' . $now->hms;

my $config = LoadFile('/home/bas/.darts.yaml');
my $file   = File::Spec->rel2abs( $options->{file} );
my $excel  = Spreadsheet::XLSX->new($file);

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

unlink("/tmp/standen_$lastdate.xlsx");
my $workbook = Excel::Writer::XLSX->new("/tmp/standen_$lastdate.xlsx");

my %tables;

my @players_stand
    = sort { $a->{matchcount} <=> $b->{matchcount} } @players;
@players_stand = sort { $b->{score} <=> $a->{score} } @players_stand;
{
    my @table
        = ( [ 'Stand', 'Naam', 'Punten', 'Wedstrijden', 'Gemiddeld', ] );
    my $i = 1;
    foreach my $player (@players_stand) {
        my @row = (
            $i, $player->{name}, $player->{score}, $player->{matchcount},
            sprintf( "%0.2f", $player->{score} / $player->{matchcount} ),
        );

        push @table, \@row;
        $i++;
    }

    my $worksheet = storeTable( 'stand', \@table );
}

my @players_180
    = sort { $b->{max} <=> $a->{max} } grep { $_->{max} } @players;
{
    my @table = ( [ 'Naam', 'x 180' ] );
    foreach my $player (@players_180) {
        my @row = ( $player->{name}, $player->{max}, );
        push @table, \@row;
    }

    my $worksheet = storeTable( '180', \@table );

}

my @players_finishes = sort { $b->{finishes}->[0] <=> $a->{finishes}->[0] }
    grep { @{ $_->{finishes} } } @players;
{
    my @table = ( [ 'Naam', 'Finishes 100+', ] );
    foreach my $player (@players_finishes) {
        my @row = ( $player->{name}, join( ', ', @{ $player->{finishes} } ) );
        push @table, \@row;
    }

    my $worksheet = storeTable( 'finishes', \@table );
}

my @players_lollies = sort { $b->{lollies} <=> $a->{lollies} }
    grep { $_->{lollies} } @players;
{
    my @table = ( [ 'Naam', 'Lollies', ] );
    foreach my $player (@players_lollies) {
        my @row = ( $player->{name}, $player->{lollies}, );
        push @table, \@row;
    }

    my $worksheet = storeTable( 'lollies', \@table );
}

{
    my @table = (
        [   'Stand',     'Naam', 'Punten',        'Wedstrijden',
            'Gemiddeld', '180',  '100+ finishes', 'lollies'
        ]
    );
    my $i = 1;
    foreach my $player (@players_stand) {
        my @row = (
            $i,
            $player->{name},
            $player->{score},
            $player->{matchcount},
            sprintf( "%0.2f", $player->{score} / $player->{matchcount} ),
            $player->{max},
            join( ', ', @{ $player->{finishes} } ),
            $player->{lollies},
        );
        push @table, \@row;
        $i++;
    }

    my $worksheet = storeTable( 'alles', \@table );

}

$workbook->close();

my $mech;
if ( $options->{updatesite} ) {
    $mech = WWW::Mechanize->new();
    $mech->get('https://svausterlitz.voetbalassist.nl/cms/index.aspx');
    my $res = $mech->submit_form(
        form_name => 'aspnetForm',
        fields    => {
            'ctl00$Content$gebruikersnaam' => $config->{website}->{username},
            'ctl00$Content$wachtwoord'     => $config->{website}->{password},
        },
        button => 'ctl00$Content$SubmitBtn'
    );

    if ( $res->is_success ) {

        # my $c = $res->decoded_content;
        # p $c;
        updatePage('stand');
        updatePage(180);
        updatePage('finishes');
        updatePage('lollies');
    }

}

exit;

sub updatePage {
    my $name = shift;

    my $aoa = $tables{$name};

    my $pages = {
        stand => {
            title => 'Competitiestand',
            uri =>
                'https://svausterlitz.voetbalassist.nl/cms/Index2.aspx?m=1&o=1&miid=412',
        },
        180 => {
            title => "Aantal 180's",
            uri =>
                'https://svausterlitz.voetbalassist.nl/cms/Index2.aspx?m=1&o=1&miid=413',
        },
        finishes => {
            title => 'Hoogste finishes',
            uri =>
                'https://svausterlitz.voetbalassist.nl/cms/Index2.aspx?m=1&o=1&miid=414',
        },
        lollies => {
            title => 'Aantal Lollies',
            uri =>
                'https://svausterlitz.voetbalassist.nl/cms/Index2.aspx?m=1&o=1&miid=493',
        },
    };

    my $table = HTML::Table->new($aoa);
    $table->setBorder(1);
    my $t = $table->getTable;

    my $content = "<h1>$pages->{$name}->{title}</h1>". $table . '<p><hr>' . 'updated ' . $updatetime;

    $mech->get( $pages->{$name}->{uri} );
    my $res = $mech->submit_form(
        form_name => 'aspnetForm',
        fields    => {
            'Mp$Content$ctl00$contentTextBox' => $content,
            'Mp$Content$ctl00$Opslaan'        => 'Opslaan',
        },
        button => 'Mp$Content$ctl00$Opslaan'
    );
}

sub storeTable {
    my $name  = shift;
    my $table = shift;

    $tables{$name} = $table;
    my $worksheet = $workbook->add_worksheet($name);
    $worksheet->write_col( 0, 0, $table );

    return $worksheet;
}

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

