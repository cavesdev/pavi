

// import axios from 'axios';
// const axios = require('axios');
// const baseURl = "localhost:5000/";




var data = {

  FPS: 30,
  capture_date: 1,
  duration: 7,
  filename: "trim",
  format: ".mp4",
  processing :  [
      {
          algorithm: "YOLOv3",
          detections: [
              {
                  objects:{
                      car:{
                          count: 11
                      }
                  }
              }
          ]
      }
  ]

}

function createTabe(table){
    let tHead = table.createTHead();
    let row = table.insertRow();

    let th = document.createElement("th");
    let text = document.createTextNode("test");
    th.appendChild(text)
    row.appendChild(th)
}

function generateTableContent(table, rowName, data){
    let row = table.insertRow();

    let cell = row.insertCell();

    let text = document.createTextNode(rowName);
    let text2 = document.createTextNode(data);

    cell.appendChild(text)
    cell.appendChild(text2)

}

(function getData() {
    let dataPromise = new Promise(() => {
        let req = new XMLHttpRequest();

        req.open('get', 'localhost:5000/search')
        req.send();
        req.onload = function() {
            console.log(req.response);
        };
    })
})();

// var jsonData
let Promise = new Promise(axios.get('../scripts/data.json'))
// Promise.then((data) => jsonData = data)
// Promise.catch((error) => alert(error))

var tableDiv = document.querySelector('table')
// createTabe(tableDiv)
generateTableContent(tableDiv, "File name   ", data.filename)
generateTableContent(tableDiv, "Capture date    ",  data.capture_date)
generateTableContent(tableDiv, "Algorithm   ", data.processing[0].algorithm)
generateTableContent(tableDiv, "Number of items ", data.processing[0].detections[0].objects.car.count)


console.log("I was able to get here")








