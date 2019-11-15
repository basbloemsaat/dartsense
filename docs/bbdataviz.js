// requires d3

var bbdataviz = {};
(function() {

    this.parameters = {
        row_height: 20,
        row_offset: 25,
        column_spacer: 25,
    }

    // svg table to assist in visualizing and making interactive
    // columns = [
    //   {
    //     "id": "columnid",
    //     "pos": "position", // left mid or right, default left
    //     "width": "width", // unit, fit or max (1 per table), default fit
    //     "content": "field name", // if string: the name of a field in the data, otherwise a function
    //     "newfunction": function(cell) {}, // function to fill new cell, other than text;
    //     "header": { 
    //         "text": "text", //string or function
    //         "rotate": 45, //optional, default no rotate
    //     },
    //   },
    // ]
    this.Table = function(svg, columns) {
        this.svg = svg;
        this.columns = columns;
        this.g = svg.append('g').attr('class', 'root');
        this.headers = this.g.append('g')
            .attr('class', 'headers')
            .attr("transform", "translate(0,12)");
        this.rows = this.g.append('g')
            .attr('class', 'rows')
            .attr("transform", "translate(0,12)");

        this.resize();
        this.render_cols();
    }

    this.Table.prototype.resize = function() {
        let width = Math.round(0 + this.g.node().getBBox().width);
        let height = Math.round(0 + this.g.node().getBBox().height + 10);

        this.svg.attr('viewBox', '0 0 ' + width + ' ' + height);
        // this.svg.attr('preserveAspectRatio', 'xMidYMid meet');

    }

    this.Table.prototype.render_cols = function() {
        if (this.columns.length == 0) { return };

        this.column_lookup = this.columns.reduce(function(lookup, column) {
            if (column['id']) {
                lookup[column.id] = column;
            }
            return lookup;
        }, {})

        let left = 0;
        let right = this.width;

        let cols_left = this.cols_left = [];
        let col_mid = this.col_mid = [];
        let cols_right = this.cols_right = [];

        // prep columns for display
        for (let i = 0; i < this.columns.length; i++) {
            let col = this.columns[i];
            switch (col['position']) {
                case 'fill':
                    col_mid[0] = col;
                    break;
                case 'right':
                    cols_right.unshift(col);
                    break;
                default:
                    col['position'] = 'left';
                    cols_left.push(col);
            }
        }

        let cols = this.headers.selectAll('text.header').data(cols_left.concat(col_mid).concat(cols_right), function(d) { return d.id });
        cols.exit().remove();
        cols.enter().append('text')
            .classed('header', true)
            .attr('data-columnid', function(d) { return d.id })
            .attr('text-anchor', function(d) {
                if (d['header'] && d['header']['rotate']) {
                    return 'end';
                }
                return 'start';
            })
            .text(function(d) {
                if (d['header'] && d['header']['text']) {
                    return d['header']['text'];
                }
            })

        this.reposition_columns();
    }

    this.Table.prototype.reposition_columns = function() {
        if (this.columns.length == 0) { return };

        this.g.select('g.headers').selectAll('text.header').text(function(d) {
            if (d['header'] && d['header']['text']) {
                return d['header']['text'];
            } else {
                return '';
            }
        });

        let column_lookup = this.column_lookup;

        // get cell widths
        this.g.selectAll('text.header').each(function(d) {
            let col = column_lookup[d3.select(this).attr('data-columnid')];
            let mw = this.getBBox().width;

            if (col['header'] && col['header']['rotate']) {
                mw = bbdataviz.parameters.row_height;
            }
            if (!mw) {
                mw = 0;
            }
            col.measured_width = Math.max(col.measured_width || 0, mw)
        })

        this.g.selectAll('g.cell').each(function(d) {
            if (column_lookup[d3.select(this).attr('data-columnid')]) {

                column_lookup[d3.select(this).attr('data-columnid')].measured_width = Math.max(column_lookup[d3.select(this).attr('data-columnid')].measured_width || 0, Math.ceil(this.getBBox().width) || 0)
            }
        })


        // position columns
        let left = 0;
        let right = this.width;
        for (let i = 0; i < this.cols_left.length; i++) {
            let col = this.cols_left[i];
            col.pos = left;
            left = left + col.measured_width + bbdataviz.parameters.column_spacer;
        }
        for (let i = 0; i < this.cols_right.length; i++) {
            let col = this.cols_right[i];
            right = right - col.measured_width;
            col.pos = right;
            right = right - bbdataviz.parameters.column_spacer;
        }
        if (this.col_mid && this.col_mid[0]) {
            this.col_mid[0].pos = left;
            this.col_mid[0].width = right - left;
        }

        // reposition column cells and headers
        this.g.selectAll('text.header').attr('transform', function(d) {
            let colid = d3.select(this).attr('data-columnid');
            let col = column_lookup[colid];
            let retval = 'translate(' + col.pos + ',0)';
            if (col['header'] && col['header']['rotate']) {
                retval += ' rotate(' + col['header']['rotate'] + ')'
            }
            return retval
        });
        this.g.selectAll('g.cell').attr('transform', function(d) {
            let colid = d3.select(this).attr('data-columnid');
            return 'translate(' + (column_lookup[colid] ? column_lookup[colid].pos : 0) + ',0)';
        });

        // Check the header height and reposition the header and rows g accordingly.
        let h = this;
        this.g.select('g.headers').each(function(d) { h.headerheight = Math.ceil(this.getBBox().height) });
        this.g.select('g.headers').attr('transform', function(d) {
            return 'translate(0,' + h.headerheight + ')';
        })

        this.g.select('g.rows').attr('transform', 'translate(0,' + (h.headerheight + bbdataviz.parameters.row_offset) + ')');

    }

    // set the data and (re)render the table
    this.Table.prototype.data = function(data) {
        let s = this.g.select('g.rows').selectAll('g.row')
            .data(data, function(d) {
                return d.id;
            });

        s.exit().remove();
        let newrows = s.enter()
            .append('g')
            .attr('class', 'row')
            .attr('row_id', function(d) {
                return 'row_' + d.id
            })

        if (newrows.size()) {
            for (let i = 0; i < this.columns.length; i++) {
                let col = this.columns[i];
                var cell = newrows.append('g')
                    .classed('cell', true)
                    .classed('cell_' + col.id, true)
                    .attr('data-columnid', col.id);

                // per col juiste element invoegen.
                if (!col['newfunction']) {
                    cell.append('text');
                }
            }
        }
        let table = this;

        // refresh alle cellcontents
        this.svg.selectAll('g.cell').each(function(d) {
            let sel = d3.select(this);
            let coldef = table.column_lookup[sel.attr('data-columnid')];
            // console.log(coldef, d);
            if (!coldef['newfunction']) {
                let content
                if (typeof coldef['content'] == 'function') {
                    content = coldef['content'](d);
                } else {
                    content = d[coldef['content']];
                }
                sel.selectAll('text').text(content);
            }
            sel
        });

        s.merge(newrows).attr('transform', function(d, i) {
            return 'translate(0,' + (i * bbdataviz.parameters.row_height) + ')';
        })

        this.reposition_columns();
        this.resize();
    }


    this.LineChart = function(svg, xscale, yscale) {
        this.parameters = {
            chart_width: 800,
            chart_height: 600,
            chart_margin: 30,
        };
        this.svg = svg;
        this.g = svg.append('g').attr('class', 'root');
        // this.g.attr('width', this.parameters.width);
        // this.g.attr('height', this.parameters.height);


        this.xscale = xscale;
        xscale.range([0, this.parameters.chart_width]);
        this.x =
            this.g.append('g')
            .attr('class', 'xaxis')
            .attr('transform', 'translate(' + this.parameters.chart_margin + ',' + (this.parameters.chart_height + this.parameters.chart_margin) + ')')
            .call(d3.axisBottom(xscale));;

        this.yscale = yscale;
        yscale.range([this.parameters.chart_height, 0]);
        this.y = this.g.append('g').attr('class', 'yaxis')
            .attr('transform', 'translate(' + this.parameters.chart_margin + ',' + this.parameters.chart_margin + ')')
            .call(d3.axisLeft(yscale));;

        this.canvas = this.g.append('g').attr('class', 'canvas');

        this.resize();
    }

    this.LineChart.prototype.resize = function() {
        let width = Math.round(0 + this.g.node().getBBox().width) + (this.parameters.chart_margin);
        let height = Math.round(0 + this.g.node().getBBox().height) + this.parameters.chart_margin;

        this.svg.attr('viewBox', '0 0 ' + width + ' ' + height);
    }

    // set the data and (re)render the chart
    this.LineChart.prototype.data = function(data) {
        console.log(data);
    }

}).apply(bbdataviz);