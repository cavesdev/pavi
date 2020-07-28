import axios from 'axios';
const axios = require('axios');
const baseURl = "localhost:5000/";

var tabelDiv = document.getElementById('info-table');

var table = document.createElement('table');
table.setAttribute("class", "table");


tabelDiv.appendChild(table);
// tabelDiv.appendChild();

axios.get(baseURL)
.then(resp => {

    var tableBody  = document.createElement('tbody')

    var fileNameField = document.createElement('tr')
    
    var tableHeader = document.createElement('th');
    tableHeader.setAttribute("scope", "row")
    tableHeader.textContent = "File Name";

    var tableD = document.createElement('td');
    tableD.textContent = resp.filename;
    
    fileNameField.appendChild(tableHeader)
    tableBody.appendChild(fileNmaeField)

    tableHeader.appendChild(tableD);

    var captureDate = document.createElement('tr');
    var captureHeader = document.createElement('th');
    captureDate.setAttribute("scope", "row");
    captureDate.textContent = 

});