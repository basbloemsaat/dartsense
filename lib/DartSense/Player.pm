package DartSense::Player;

use v5.020;
use strict;
use warnings;
use utf8;

binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";
binmode STDIN,  ":encoding(UTF-8)";

use Data::Printer;

use parent ('Class::Accessor');

use experimental 'signatures';
no warnings "experimental::signatures";

__PACKAGE__->follow_best_practice;
__PACKAGE__->mk_accessors( 'name', 'rating', 'ratecount' );

sub new($class, $args) {
    my $self = $class->SUPER::new($args);

    $self->{matches}    = [];
    $self->{mutations}  = [];
    $self->{cumulative} = [];
    $self->{ratecount}  = 0;
    $self->{rating}     = 1000;
    return $self;

}

sub addMatch($self, $match) {
    push @{ $self->{matches} }, $match;
    return @{ $self->{matches} };
}

sub addMutation($self, $mutation) {
    push @{ $self->{mutations} }, $mutation;
    $self->{rating} += $mutation;
    push @{ $self->{cumulative} }, $self->{rating};
    return $self->{rating};
}

1;
