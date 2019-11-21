function Plot(opts)
{
    this.points = opts.points;
    this.line = opts.line;
    this.point = opts.point;
    this.chartTitle = opts.chartTitle;
    this.chartCanvas = document.querySelector("#chartCanvas");
}

Plot.prototype.init = function ()
{
    this.drawPlot();
    this.clickListner();
};

Plot.prototype.drawPlot = function ()
{
    var self = this;
    var ctx = document.getElementById("chartCanvas").getContext('2d');
    window.chart = new Chart(ctx, {
        type: 'bubble',
        data: {
            datasets: [{
                    data: self.points,
                    borderColor: "#59aee4",
                    backgroundColor: "white",
                    borderWidth: 2,

                    hoverRadius: 2,
                    hoverBorderWidth: 2,
                    //hoverBorderColor: "rgba(12, 2, 62, 1)",
                    hoverBackgroundColor: "#59aee4", //"rgba(12, 2, 62, 1)"
                },
                {
                    data: self.point,
                    borderColor: "#92b342",
                    backgroundColor: "#92b342",
                    hoverBackgroundColor: "#92b342",
                    hoverBorderWidth: 2,
                    borderWidth: 2,
                    hoverRadius: 2,


                },
                {
                    data: self.line,
                    radius: 0,
                    type: 'line',
                    fill: false,
                    borderColor: "#92b342",
                    borderWidth: 3,
                }
            ]
        },
        options: {
            title: {
                display: true,
                //text: self.chartTitle
            },
            responsive: true,
            animation: {
                duration: 0
            },
            tooltips: {
                mode: "nearest",
                position: "nearest",
                enabled: false,
                fillColor: "red",
                callbacks: {
                    beforeTitle: function (tooltipItem, data) {
                        return "Price: <b>" + numberWithCommas(tooltipItem[0].yLabel) + '</b> ($)';
                    },
                    title: function (tooltipItems, data) {
                        return "<b>" + data.datasets[tooltipItems[0].datasetIndex].data[tooltipItems[0].index].year + "</b>";
                    },
                    afterTitle: function (tooltipItem, data) {
                        return "Odometer[mi]: <b>" + numberWithCommas(tooltipItem[0].xLabel) + '</b>';
                    },

                    label: function (tooltipItems, data) {
                        return '<img width="220" src="' + data.datasets[tooltipItems.datasetIndex].data[tooltipItems.index].picture + '" />';
                    },
                    footer: function (tooltipItems, data) {
                        return tooltipItems;
                    },
                },
                custom: function (tooltipModel) {
                    if (tooltipModel.footer) {
                        if (tooltipModel.footer[0].datasetIndex > 1) {
                            return;
                        }
                    }

                    var tooltipEl = document.getElementById('chartjs-tooltip');
                    if (!tooltipEl) {
                        tooltipEl = document.createElement('div');
                        tooltipEl.id = 'chartjs-tooltip';
                        tooltipEl.innerHTML = "<table></table>";
                        document.body.appendChild(tooltipEl);
                    }

                    if (tooltipModel.opacity === 0) {
                        tooltipEl.style.opacity = 0;
                        return;
                    }

                    tooltipEl.classList.remove('above', 'below', 'no-transform');
                    if (tooltipModel.yAlign) {
                        tooltipEl.classList.add(tooltipModel.yAlign);
                    } else {
                        tooltipEl.classList.add('no-transform');
                    }

                    var img = tooltipModel.body[0].lines[0];
                    var price = tooltipModel.title[0];
                    var year = tooltipModel.title[1];
                    var mileage = tooltipModel.title[2];
                    var innerHtml = '<tr><td>' + price + '</td><td>' + year + ' y.</td></tr><tr><td>' + mileage + '</td><td></td></tr>' + '<tr><td colspan="2">' + img + '</td></tr>';

                    var tableRoot = tooltipEl.querySelector('table');
                    tableRoot.innerHTML = innerHtml;

                    tooltipEl.style.opacity = 1;
                    tooltipEl.style.left = tooltipModel.caretX + 20 + 'px';
                    tooltipEl.style.top = tooltipModel.caretY + 20 + 'px';
                    tooltipEl.style.fontFamily = "inherit";
                    tooltipEl.style.fontSize = tooltipModel.fontSize;
                    tooltipEl.style.fontStyle = tooltipModel._fontStyle;


                }

            },
            legend: {
                display: false,
                labels: {
                    display: false
                }
            },
            scales: {
                xAxes: [{
                    gridLines: {
                        color: "#E6E5EB"
                    },
                    position: 'bottom',
                    scaleLabel: {
                        display: true,
                        labelString: 'Odometer[mi]',
                        fontColor: "#59aee4",
                        fontSize: 16,
                        fontStyle: "semibold"
                    },
                    ticks: {
                        fontColor: "#075fbd",
                        fontSize: 16,
                        fontStyle: "semibold",
                        callback: function (value) {
                            return numberWithCommas(value);
                        },
                    },
                }],
                yAxes: [{
                    gridLines: {
                        color: "#E6E5EB"
                    },
                    position: 'left',
                    scaleLabel: {
                        display: true,
                        labelString: 'Price ($)',
                        fontColor: " #59aee4",
                        fontSize: 16,
                        fontStyle: "semibold"
                    },
                    ticks: {
                        fontColor: "#075fbd",
                        fontSize: 16,
                        fontStyle: "semibold",
                        callback: function (value) {
                            return numberWithCommas(value);
                        },
                    },

                }]
            }
        }
    });
};

Plot.prototype.clickListner = function () {
    var self = this;
    self.chartCanvas.addEventListener("click", function (e) {
        var points = chart.getElementAtEvent(e);
        if (points.length > 0) {
            var point = points[0];
            var url = chart.data.datasets[point._datasetIndex].data[point._index].url;
            window.open(url);
        }
    });
};

window.plot = Plot;
