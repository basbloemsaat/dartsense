var dartsapp = {};
(function() {
    this.data = [];
    this.data_indexes = {
        "bydate": {},
        "byplayer": {},
    };
    this.seasons = {};
    this.all_player_seasons = [];


    this.lastdate = new Date('2001-01-01')

    this.players_name_lookup = {
        "Andor": "Andor",
        "Anil": "Anil",
        "Bas": "Bas",
        "Bert": "Bert",
        "Brandon": "Brandon",
        "Christa": "Christa",
        "Colin": "Colin",
        "Ed": "Ed",
        "Elbert": "Elbert",
        "Erik H": "Erik H",
        "Erik": "Erik H",
        "Ernie": "Ernie",
        "Frank": "Frank",
        "Frans": "Frans",
        "Gert J": "Gert J",
        "Gert": "Gert J",
        "Gijs": "Gijs",
        "Gilbert": "Gilbert",
        "Hans": "Hans",
        "Harry": "Harry",
        "Henri": "Henri",
        "Jari": "Jari",
        "Johan": "Johan",
        "John": "John",
        "Joost": "Joost",
        "Joris": "Joris",
        "JR": "JR",
        "Kim": "Kim",
        "Maik": "Maik",
        "Marianne": "Marianne",
        "Martin": "Martin",
        "Menno": "Menno",
        "Otto": "Otto",
        "Paplip": "Paplip",
        "Pietra": "Pietra",
        "Reyn": "Reyn",
        "Youri": "Youri"
    }

    this.add_item_to_index = function(index, key, item) {
        if (!this.data_indexes[index][key]) {
            this.data_indexes[index][key] = [];
        }
        this.data_indexes[index][key].push(item);
    }

    this.add_data = function(filename, data) {
        this.data = this.data.concat(data);

        let competitie_naam = filename.replace(/\.json$/, '').replace(/_/g, ' ');

        // meer manieren om naar de data te kijken: indexen maken.
        for (let i = 0; i < data.length; i++) {
            let item = data[i];

            // this.lastdate = Math.max(this.lastdate, item['Date'])
            let itemdate = new Date(item['Date']);
            item['Date'] = itemdate;
            if(itemdate.getTime() > dartsapp.lastdate.getTime()) {
                dartsapp.lastdate = itemdate;
            }

            item['Year'] = item['Date'].getYear();
            item['Seizoen'] = competitie_naam;

            //d3.nest werkt hier ook, maar niet bij spelers en ik loop er toch al door
            this.add_item_to_index('bydate', item['Date'], item);

            if (item['Speler']) {
                this.add_item_to_index('byplayer', this.players_name_lookup[item['Speler']], item);
            } else {
                this.add_item_to_index('byplayer', this.players_name_lookup[item['Speler1']], item);
                this.add_item_to_index('byplayer', this.players_name_lookup[item['Speler2']], item);
            }
        }
    }

    this.calc_seasons = function() {
        let seasons = {};
        
        let speler_ref = function(seizoen, speler_naam) {
            if (!seizoen['byplayer'][speler_naam]) {
                seizoen['byplayer'][speler_naam] = {
                    "id": speler_naam,
                    '180s': [],
                    'Finishes': [],
                    'Gemiddelde': 0,
                    'GemiddeldePerDate': {},
                    'Lollies': [],
                    'Naam': speler_naam,
                    'Punten': 0,
                    'PuntenPerDate': {},
                    'Wedstrijden': 0,
                    'WedstrijdenPerDate': {},
                };
                seizoen['results'].push(seizoen['byplayer'][speler_naam]);
                dartsapp.all_player_seasons.push(seizoen['byplayer'][speler_naam])
            }

            return seizoen['byplayer'][speler_naam];
        }

        let speler_add_180 = function(speler, date, max) {
            if (max) {
                speler['180s'].push([date, max]);
                speler_add_points(speler, date, max);
            }
        }
        let speler_add_lollies = function(speler, date, lollies) {
            if (lollies) {
                speler['Lollies'].push([date, lollies]);
            }
        }
        let speler_add_finishes = function(speler, date, finishes) {
            if (finishes) {
                let a = ('' + finishes).split(',');
                for (let ai = 0; ai < a.length; ai++) {
                    let finish = a[ai];
                    speler['Finishes'].push([date, finish]);
                    // voeg toe aan speler punten
                    if (finish == 170) {
                        speler_add_points(speler, date, 10);
                    } else if (finish == 167) {
                        speler_add_points(speler, date, 9);
                    } else if (finish == 164) {
                        speler_add_points(speler, date, 8);
                    } else if (finish == 161) {
                        speler_add_points(speler, date, 8);
                    } else if (finish == 160) {
                        speler_add_points(speler, date, 7);
                    } else if (finish > 150) {
                        speler_add_points(speler, date, 6);
                    } else if (finish > 140) {
                        speler_add_points(speler, date, 5);
                    } else if (finish > 130) {
                        speler_add_points(speler, date, 4);
                    } else if (finish > 120) {
                        speler_add_points(speler, date, 3);
                    } else if (finish > 110) {
                        speler_add_points(speler, date, 2);
                    } else {
                        speler_add_points(speler, date, 1);
                    }
                }
            }
        }
        let speler_add_points = function(speler, date, points) {
            if (points) {
                speler['Punten'] += points;
                if (!speler['PuntenPerDate'][date]) {
                    speler['PuntenPerDate'][date] = 0;
                }
                speler['PuntenPerDate'][date] += points;
            }
            speler_gemiddelde(speler, date);
        }

        let speler_add_wedstrijden = function(speler, date, aantal) {
            speler['Wedstrijden'] += aantal;
            if (!speler['WedstrijdenPerDate'][date]) {
                speler['WedstrijdenPerDate'][date] = 0;
            }
            speler['WedstrijdenPerDate'][date] += aantal;
            speler_gemiddelde(speler, date);
        }

        let speler_gemiddelde = function(speler, date) {
            if (speler['Wedstrijden'] > 0) {
                speler['Gemiddelde'] = speler['Punten'] / speler['Wedstrijden'];
            }
            if (speler['WedstrijdenPerDate'][date] > 0 && speler['PuntenPerDate'][date] > 0) {
                speler['GemiddeldePerDate'][date] = speler['PuntenPerDate'][date] / speler['WedstrijdenPerDate'][date];
            }
        }

        for (let i = 0; i < this.data.length; i++) {
            let item = this.data[i];

            if (!item['Seizoen']) { continue; }
            let seizoen_naam = item['Seizoen'];
            // console.log(item);

            if (!seasons[seizoen_naam]) {
                seasons[seizoen_naam] = {
                    byplayer: {},
                    results: [],
                };
            }

            let seizoen = seasons[seizoen_naam];
            if (item['Type'] == 'regulier') {
                // gewone wedstrijd op competitieavond
                let speler1_data = speler_ref(seizoen, item['Speler1']);
                let speler2_data = speler_ref(seizoen, item['Speler2']);

                speler_add_wedstrijden(speler1_data, item['Date'], 1);
                speler_add_wedstrijden(speler2_data, item['Date'], 1);

                let points1 = 0;
                let points2 = 0;

                // punten wedstrijd
                if (item['Legs1'] == 0 && item['Legs2'] == 2) {
                    points2 += 5;
                } else if (item['Legs1'] == 1 && item['Legs2'] == 2) {
                    points1 += 1;
                    points2 += 3;
                } else if (item['Legs1'] == 2 && item['Legs2'] == 1) {
                    points1 += 3;
                    points2 += 1;
                } else if (item['Legs1'] == 2 && item['Legs2'] == 0) {
                    points1 += 5;
                }

                speler_add_points(speler1_data, item['Date'], points1);
                speler_add_points(speler2_data, item['Date'], points2);
                speler_add_180(speler1_data, item['Date'], item['Max1']);
                speler_add_180(speler2_data, item['Date'], item['Max2']);
                speler_add_lollies(speler1_data, item['Date'], item['Lollies1']);
                speler_add_lollies(speler2_data, item['Date'], item['Lollies2']);
                speler_add_finishes(speler1_data, item['Date'], item['Finishes1']);
                speler_add_finishes(speler2_data, item['Date'], item['Finishes2']);
            } else if (item['Type'] == 'koppel') {
                // de punten en andere dingen van een koppelavond
                let speler_data = speler_ref(seizoen, item['Speler']);
                speler_add_wedstrijden(speler_data, item['Date'], item['Matches']);
                speler_add_points(speler_data, item['Date'], item['Points']);
                speler_add_180(speler_data, item['Date'], item['Max']);
                speler_add_lollies(speler_data, item['Date'], item['Lollies']);
                speler_add_finishes(speler_data, item['Date'], item['Finishes']);
            }
        }

        for (let season_name in seasons) {
            let season = seasons[season_name];
            season['results'].sort(function(a, b) {
                let res = b.Punten - a.Punten
                if (res == 0) {
                    res = a.Wedstrijden - b.Wedstrijden;
                }
                return res;
            })
        }



        let all = dartsapp.all_player_seasons;
        for (let i=0;i<all.length;i++) {
            let ps = all[i];

            console.log(ps);
            // let keys = 
            for (let entry of Object.entries(ps['PuntenPerDate'])) {
                console.log(entry)
            }
            // ps['PuntenPerDate'] = ps['PuntenPerDate'].sort(function(a,b) {
            //     return a.Date.getTime() - b.Date.getTime();
            // })


        }

        dartsapp.seasons = seasons;
        return seasons;
    }
}).apply(dartsapp);