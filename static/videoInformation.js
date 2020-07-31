

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

function getData(videoName) {
    const request = new Request(`/search?filename=${videoName}`);

    fetch(request)
        .then(res => res.json())
        .then(function(data) {
            console.log(data)
            var tableDiv = document.querySelector('table')
// createTabe(tableDiv)

            var video = document.querySelector('video')
            var videoName = video.getAttribute("name")
            console.log(videoName)
            generateTableContent(tableDiv, "File name   ", data.filename)
            generateTableContent(tableDiv, "Capture date    ",  data.capture_date)
            generateTableContent(tableDiv, "Algorithm   ", data.processing[0].algorithm)
            generateTableContent(tableDiv, "Number of items ", data.processing[0].detections[0].car.count)
        });
}

getData();

// var jsonData
// let Promise = new Promise(axios.get('../scripts/data.json'))
// Promise.then((data) => jsonData = data)
// Promise.catch((error) => alert(error))









