//Radial Chart Probability of Misuse
var options = {
    //Series drives the number rendered in the chart and the position of the radial line
    series: odScore,
    //Colors are lt, md, and dk-primary-mustard. Change the if statements to set the thresholds to render the colors
    colors: [
        function ({ value, seriesIndex, w }) {
            if (value <= 33) {
                return "#FFD073";
            } else if (value >= 66) {
                return "#CC8800";
            } else {
                return "#FFAA00";
            }
        }
    ],
    chart: {
        height: "100%",
        type: "radialBar",
        toolbar: {
            show: true
        }
    },
    //Tooltip renders when mouseover of the track in the chart. Changing the number referenced in series will update the number in the tooltip as well. There have been custom breaks put into the text just to make it easier to read
    tooltip: {
        enabled: true,
        custom: function ({ series, seriesIndex, dataPointIndex, w }) {
            return (
                '<div class="tooltip_box">' +
                "<span>" +
                "A probability of " +
                "<b>" +
                [series] +
                "%" +
                "</b>" +
                " means that <br> the individual has a " +
                "<b>" +
                [series] +
                "%" +
                "</b>" +
                " chance <br> of overdosing in the next year" +
                "</span>" +
                "</div>"
            );
        }
    },
    //Start and end angle inside radialBar and track determine the start/end of the chart
    plotOptions: {
        radialBar: {
            startAngle: -135,
            endAngle: 135,
            hollow: {
                margin: 0,
                size: "70%",
                background: "#fff",
                image: undefined,
                imageOffsetX: 0,
                imageOffsetY: 0,
                position: "front",
                dropShadow: {
                    enabled: true,
                    top: 3,
                    left: 0,
                    blur: 4,
                    opacity: 0.15
                }
            },
            track: {
                background: "#e8eef9",
                strokeWidth: "67%",
                startAngle: -135,
                endAngle: 135,
                margin: 0, // margin is in pixels
                dropShadow: {
                    enabled: true,
                    top: 3,
                    left: 0,
                    blur: 4,
                    opacity: 0.10
                }
            },
            dataLabels: {
                show: true,
                name: {
                    offsetY: -30,
                    show: true,
                    color: "#847e8a",
                    //Font size is responsive
                    fontSize: "calc(8px + .5vw)"
                },
                value: {
                    //Returns the number with % added to the end
                    formatter: function (val) {
                        return parseInt(val) + "%";
                    },
                    color: "#363a4a",
                    //Font size is responsive
                    fontSize: "calc(8px + 2.5vw)",
                    show: true
                }
            }
        }
    },
    //The section below determines responsive behavior similar to css media queries. To target a specific section all parent items must also be listed
    responsive: [
        //1200px
        {
            breakpoint: 1200,
            options: {
                plotOptions: {
                    radialBar: {
                        dataLabels: {
                            name: {
                                offsetY: -15,
                                fontSize: "calc(8px + .4vw)"
                            }
                        }
                    }
                }
            }
        },
        //760px
        {
            breakpoint: 760,
            options: {
                plotOptions: {
                    radialBar: {
                        dataLabels: {
                            name: {
                                offsetY: -10,
                                fontSize: "calc(8px + 1.2vw)"
                            },
                            value: {
                                fontSize: "calc(8px + 3.5vw)",
                            }
                        }
                    }
                }
            }
        },
        //480px
        {
            breakpoint: 480,
            options: {
                plotOptions: {
                    radialBar: {
                        dataLabels: {
                            name: {
                                show: false
                            },
                            value: {
                                fontSize: "calc(8px + 6vw)",
                            }
                        }
                    }
                }
            }
        }
    ],
    stroke: {
        lineCap: "round"
    },
    labels: ["Probability of Misuse"]
};

var chart = new ApexCharts(document.querySelector("#PMradialchart"), options);
chart.render();

//Radial Chart Risk Percentile
var options = {
    //Series drives the number rendered in the chart and the position of the radial line
    series: odPercent,
    //Colors are lt, md, and dk-primary-mustard. Change the if statements to set the thresholds to render the colors
    colors: [
        function ({ value, seriesIndex, w }) {
            if (value <= 33) {
                return "#FFD073";
            } else if (value >= 66) {
                return "#CC8800";
            } else {
                return "#FFAA00";
            }
        }
    ],
    chart: {
        height: "100%",
        type: "radialBar",
        toolbar: {
            show: true
        }
    },
    //Tooltip renders when mouse over of the track in the chart. Changing the number referenced in series will update the number in the tooltip as well. There have been custom breaks put into the text just to make it easier to read
    tooltip: {
        enabled: true,
        custom: function ({ series, seriesIndex, dataPointIndex, w }) {
            return (
                '<div class="tooltip_box">' +
                "<span>" +
                "A percentile of " +
                "<b>" +
                [series] +
                "%" +
                "</b>" +
                " means that <br> means that this individual is more <br> likely to overdose than " +
                "<b>" +
                [series] +
                "%" +
                "</b>" +
                "<br> of the population" +
                "</span>" +
                "</div>"
            );
        }
    },
    //Start and end angle inside radialBar and track determine the start/end of the chart
    plotOptions: {
        radialBar: {
            startAngle: -135,
            endAngle: 135,
            hollow: {
                margin: 0,
                size: "70%",
                background: "#fff",
                image: undefined,
                imageOffsetX: 0,
                imageOffsetY: 0,
                position: "front",
                dropShadow: {
                    enabled: true,
                    top: 3,
                    left: 0,
                    blur: 4,
                    opacity: 0.15
                }
            },
            track: {
                background: "#e8eef9",
                strokeWidth: "67%",
                startAngle: -135,
                endAngle: 135,
                margin: 0, // margin is in pixels
                dropShadow: {
                    enabled: true,
                    top: 3,
                    left: 0,
                    blur: 4,
                    opacity: 0.10
                }
            },

            dataLabels: {
                show: true,
                name: {
                    offsetY: -30,
                    show: true,
                    color: "#847e8a",
                    fontSize: "calc(8px + .5vw)"
                },
                value: {
                    formatter: function (val) {
                        return parseInt(val) + "%";
                    },
                    color: "#363a4a",
                    fontSize: "calc(8px + 2.5vw)",
                    show: true
                }
            }
        }
    },
    //The section below determines responsive behavior similar to css media queries. To target a specific section all parent items must also be listed
    responsive: [
        //1200px
        {
            breakpoint: 1200,
            options: {
                plotOptions: {
                    radialBar: {
                        dataLabels: {
                            name: {
                                offsetY: -15,
                                fontSize: "calc(8px + .4vw)"
                            }
                        }
                    }
                }
            }
        },
        //760px
        {
            breakpoint: 760,
            options: {
                plotOptions: {
                    radialBar: {
                        dataLabels: {
                            name: {
                                offsetY: -10,
                                fontSize: "calc(8px + 1.2vw)"
                            },
                            value: {
                                fontSize: "calc(8px + 3.5vw)",
                            }
                        }
                    }
                }
            }
        },
        //480px
        {
            breakpoint: 480,
            options: {
                plotOptions: {
                    radialBar: {
                        dataLabels: {
                            name: {
                                show: false
                            },
                            value: {
                                fontSize: "calc(8px + 6vw)",
                            }
                        }
                    }
                }
            }
        }
    ],
    stroke: {
        lineCap: "round"
    },
    labels: ["Risk Percentile"]
};

var chart = new ApexCharts(document.querySelector("#RPradialchart"), options);
chart.render();

//Bar Chart
var options = {
    //2 series allows for the legend + color to show up
    series: [{
            name: 'Increase in change of likelihood',
            data: graphValuesPos
        },
        {
            name: 'Decrease in change of likelihood',
            data: graphValuesNeg
        },

    ],

    //Chart styling settings
    legend: {
        show: true,
        inverseOrder: true
    },
    chart: {
        type: 'bar',
        height: "100%",
        stacked: true
    },
    colors: ['#0047B3', '#c8b4eb'],
    plotOptions: {
        bar: {
            horizontal: true,
            barHeight: '80%',
        },
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        width: 1,
        colors: ["#fff"]
    },

    grid: {
        xaxis: {
            lines: {
                show: false
            }
        }
    },
    yaxis: {
        min: -10,
        max: 10,
        title: {
        //label for y axis (remove note if needed) text: 'y axis label',
        },
    },
    tooltip: {
        shared: false,
        followCursor: true,
        x: {
            formatter: function (val) {
                return val
            }
        },
        y: {
            formatter: function (val) {
                return Math.abs(val) + "%"
            }
        }
    },
    title: {
        //chart title (remove note if needed) text: 'chart title'
    },
    xaxis: {
        categories: graphKeys,
        title: {
            //label for x axis (remove note if needed) text: 'x axis label'
        },
        labels: {
            formatter: function (val) {
                return Math.abs(Math.round(val)) + "%"
            }
        }
    },
    responsive: [
        //480px
        {
            breakpoint: 760,
            options: {
                yaxis: {
                    labels: {
                        show: false
                    },
                },
                chart: {
                    height: 500
                },
            },
        },
    ],
};

var chart = new ApexCharts(document.querySelector("#barchart"), options);
chart.render();

