
// generate table at the id in the table page. "tabledata" is set on the json files called earlier in the html code 

var table = new Tabulator("#parts-table", {
    data: tabledata,
    layout:"fitColumns",
    layoutColumnsOnNewData:true,
    autoColumns:true,
    placeholder:"Something went wrong",
});


// get the column names  
var column_names = Object.keys(tabledata[0])

// link columns formatting
table.updateColumnDefinition("Code", {formatter:'link', hozAlign:'center', 
                                    formatterParams:{url:function(code){var pref='../parts/'; var suff='.html'; return pref.concat(code.getValue(), suff)}}})
table.updateColumnDefinition("doi", {formatter:'link'})

// formatting for other possible columns. Strength, Copy Number and Efficiency are substitutes to "High", and are set on the python code based on the "Set" column
table.updateColumnDefinition("Set", {width:'10%', hozAlign:'center'})
table.updateColumnDefinition("DR", {width:'5%', hozAlign:'center'})
table.updateColumnDefinition("Strength", {width:'10%', hozAlign:'center'})
table.updateColumnDefinition("Copy Number", {width:'10%', hozAlign:'center'})
table.updateColumnDefinition("Unit", {width:'5%', hozAlign:'center'})
table.updateColumnDefinition("n", {width:'5%', hozAlign:'center'})
table.updateColumnDefinition("High", {width:'5%', hozAlign:'center'})
table.updateColumnDefinition("Low", {width:'5%', hozAlign:'center'})
table.updateColumnDefinition("Km", {width:'5%', hozAlign:'center'})
table.updateColumnDefinition("Km Unit", {width:'10%', hozAlign:'center'})
table.updateColumnDefinition("Device", {width:'10%', hozAlign:'center'})
table.updateColumnDefinition("Regulator", {width:'10%', hozAlign:'center'})
table.updateColumnDefinition("Lab", {width:'5%', hozAlign:'center'})
table.updateColumnDefinition("Reg Type", {width:'10%', hozAlign:'center'})


// Hide all columns
for (num in Array.from({length: column_names.length}, (x, i) => i)){
    table.hideColumn(column_names[num])
}

// Always show at least names and codes for each part
var constant_columns = ["Name", "Code"]

for (num in Array.from({length: constant_columns.length}, (x, i) => i)){
    table.showColumn(constant_columns[num])
}


// Show other columns. "specific_columns" should be set on the table page html code as a script tag in the header.
for (num in Array.from({length: specific_columns.length}, (x, i) => i)){
    table.showColumn(specific_columns[num])
}

// Update the table as the page loads (to check for inputs to show or hide some parameter data)
update_table()


// function to show or hide quantitative parameter data based on page inputs. Based on whether the checkbox tags for specific ids are ticked or not
function update_table(){
    var dr = document.getElementById('dr')
    if (dr.checked == true){
        table.showColumn(column_names[3])
        table.redraw()
    } else {
        table.hideColumn(column_names[3])
        table.redraw()
    }
    var hill = document.getElementById('hill')
    if (hill.checked == true){
        table.showColumn(column_names[4])
        table.redraw()
    } else {
        table.hideColumn(column_names[4])
        table.redraw()
    }
    var max_min = document.getElementById('max_min')
    if (max_min.checked == true){
        table.showColumn(column_names[5])
        table.showColumn(column_names[6])
        table.showColumn(column_names[7])        
        table.redraw()
    } else {
        table.hideColumn(column_names[5])
        table.hideColumn(column_names[6])
        table.hideColumn(column_names[7])      
        table.redraw()
    }
    var k = document.getElementById('k')
    if (k.checked == true){
        table.showColumn(column_names[8])
        table.showColumn(column_names[9])
        table.redraw()
    } else {
        table.hideColumn(column_names[8])
        table.hideColumn(column_names[9])
        table.redraw()
    }
}