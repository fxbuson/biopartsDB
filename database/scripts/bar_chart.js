var chart_values = [];
var part_names = [];

for (dict of tabledata) {
    if (dict[chart_variable].includes("~")){
        chart_values.push(parseFloat(dict[chart_variable].split("~")[1]));
    }
    else{
        chart_values.push(parseFloat(dict[chart_variable]));
    }
    part_names.push(dict["Code"]);
}

unsorted = part_names.map(function(d, i) {
    return {
      label: d,
      data: chart_values[i] || 0
    };
});
  
sorted = unsorted.sort(function(a, b) {
    return b.data<a.data;
});
  
sorted_names = [];
sorted_values = [];
sorted.forEach(function(d){
    sorted_names.push(d.label);
    sorted_values.push(d.data);
});

var ctx = document.getElementById('bar_chart');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: sorted_names,
        datasets: [{
            label: chart_variable,
            data: sorted_values
        }]
    },
    options:{
        plugins:{
            legend:{
                display: false
            }
        },
        scales: {
            x: {
                grid:{
                    display: false
                }
            },
            y: {
                title:{
                    display: true,
                    text: y_title
                }
            }
        }
    }
});