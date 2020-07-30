
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
var videoData;
function getData(videoName) {
    const request = new Request(`localhost:5500/search?filename=trim`);

    fetch(request)
        .then(res => res.json())
        .then(function(data) {
            videoData = JSON.stringify(data);
            console.log(data);
            
        });
}

// var jsonData
// let Promise = new Promise(axios.get('../scripts/data.json'))
// Promise.then((data) => jsonData = data)
// Promise.catch((error) => alert(error))

var tableDiv = document.querySelector('table')
// createTabe(tableDiv)

var video = document.querySelector('video')
var videoName = video.getAttribute("name")
console.log(videoName)
generateTableContent(tableDiv, "File name   ", videoData.filename)
generateTableContent(tableDiv, "Capture date    ",  videoData.capture_date)
generateTableContent(tableDiv, "Algorithm   ", videoData.processing[0].algorithm)
generateTableContent(tableDiv, "Number of items ", videoData.processing[0].detections[0].objects.car.count)

getData(videoName);
console.log("I was able to get here")








