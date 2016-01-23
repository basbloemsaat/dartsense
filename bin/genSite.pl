#!/usr/bin/env perl

use v5.020;
use strict;
use warnings;
use utf8;

binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";
binmode STDIN,  ":encoding(UTF-8)";

use Data::Printer;
use FindBin;
use Getopt::Long;
use Template;
use Text::CSV_XS 'csv';

use lib "$FindBin::Bin/../lib";

use DartSense::Match;
use DartSense::Player;

use experimental 'signatures';
no warnings "experimental::signatures";

my $players = {};
my @matches;
my @players;

my $options = { file => '', };

GetOptions( "file=s" => \$options->{file}, );

my $aoa     = csv( in => $options->{file} );
my $headers = shift @{$aoa};
my $passes  = 5;

for ( @{$aoa} ) {
    my %args;
    for ( my $i = 0; $i < @{$_}; $i++ ) {
        $args{ $headers->[$i] } = $_->[$i];
    }

    my $player1 = getPlayer( $args{speler1} );
    my $player2 = getPlayer( $args{speler2} );

    push @matches,
        DartSense::Match->new(
        { %args, player1 => $player1, player2 => $player2, } );

}

@matches = sort { $a->get_seq cmp $b->get_seq } @matches;

for ( 1 .. $passes ) {
    for my $player (@players) {
        $player->resetPass;
    }
    for my $match (@matches) {
        $match->calcratings;
    }
}

@players = sort { $b->{rating} <=> $a->{rating} } @players;

# p @players;

my $template
    = Template->new( { INCLUDE_PATH => "$FindBin::Bin/../var/templates" } );
$template->process(
    "ranking.tt",
    { players => \@players },
    "$FindBin::Bin/../var/www/index.html"
) || die $template->error();

for (@players) {
    $template->process(
        "player.tt",
        { player => $_ },
        "$FindBin::Bin/../var/www/player_" . $_->get_name . ".html"
    ) || die $template->error();
}

# p @matches;
# # p $aoa;

sub getPlayer {
    my $name   = shift;
    my $player = $players->{$name};
    if ( !$player ) {
        $player = DartSense::Player->new( { name => $name } );
        $players->{$name} = $player;
        push @players, $player;
    }

    return $player;
}

