var x_values = [];
var y_values = [];
var part_names = [];

for (dict of tabledata) {
    part_names.push(dict["Code"]);

    if (dict["High"].includes("~")){
        y_values.push(parseFloat(dict["High"].split("~")[1]));
    }
    else{
        y_values.push(parseFloat(dict["High"]));
    }
    if (dict["Low"].includes("~")){
        x_values.push(parseFloat(dict["Low"].split("~")[1]));
    }
    else{
        x_values.push(parseFloat(dict["Low"]));
    }
}

var chart_values = [];

for (idx = 0; idx<x_values.length; idx++) {
    chart_values.push({x:x_values[idx], y:y_values[idx]})
}

var ctx = document.getElementById('scatter_chart');
var myChart = new Chart(ctx, {
    type: 'scatter',
    data: {
        datasets: [{
            label: 'Legend',
            labels: part_names,
            data: chart_values
        }]
    },
    options:{
        plugins:{
            tooltip: {
               callbacks: {
                    label: function(ctx) {
                        let label = ctx.dataset.labels[ctx.dataIndex];
                        label += " (" + ctx.parsed.x + ", " + ctx.parsed.y + ")";
                        return label;
                    }
               }
            },
            legend:{
                display: false
            }
        },
        scales: {
            x: {
                title:{
                    display: true,
                    text: 'Low'
                }
            },
            y: {
                title:{
                    display: true,
                    text: 'High'
                }
            }
        }
    }
});