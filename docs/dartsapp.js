var dartsapp = {};
(function() {

    this.data = {
        'index': {
            'spelers': [],
            'competitions': [],
        },
        'games': [],
        'spelers': {},
    };

    this.loaded = {
        'index': false,
    }

    this.available_data = {
        'index': {}
    }

    this.load_data = function(callback, to_load = {}) {

        // function die checkt of alles geladen is. Als alles is geladen wordt
        // de callback aangeroepen, anders return zonder actie
        let collector = function() {
            // todo: check of alles geladen is
            callback();
        }

        for (let i in to_load) {
            if (i == 'index') {
                d3.json('./data/index.json')
                    .then(
                        function(data) {
                            dartsapp.data['index'] = data;
                            dartsapp.loaded['index'] = true;
                            collector();
                        }
                    )
            } else if (i == 'spelers') {
                for (let s in to_load[i]) {
                    d3.json('./data/perspeler/' + to_load[i][s] + '.json')
                        .then(
                            function(data) {
                                let seasons = {};
                                dartsapp.data['spelers'][to_load[i][s]] = data;
                                let games = data.games;
                                games.sort(function(a, b) {
                                    return a.game_order - b.game_order
                                })
                                for(let g in games) {
                                    let game = games[g];
                                    let c = game['comp']
                                    if(!Object.keys(seasons).includes(c)) {
                                        seasons[c] = 0
                                    } 

                                    seasons[c] += game.speler_punten;
                                    game['comp_punten'] = seasons[c];

                                    game['date'] = new Date(game['datum'] + ' 12:00');
                                    game['timestamp'] = Date.parse(game['datum'] + ' 12:00');
                                }

                                collector();
                            }
                        )
                }
            } else {
                console.log(i)
            }
        }
    }
}).apply(dartsapp);