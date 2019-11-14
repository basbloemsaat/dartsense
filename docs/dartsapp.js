var dartsapp = {};
(function() {
    this.data = [];
    this.data_indexes = {
        "bydate": {},
        "byplayer": {},
    };

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

        let competitie_naam = filename.replace(/\.json$/,'').replace(/_/g,' ');
        console.log(competitie_naam)


        // meer manieren om naar de data te kijken: indexen maken.
        for (let i = 0; i < data.length; i++) {
            let item = data[i];

            item['Year'] = item['Date'].substr(0, 4);
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

}).apply(dartsapp);