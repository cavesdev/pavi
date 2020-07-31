

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
    const request = new Request(`https://my-json-server.typicode.com/typicode/demo/posts`);

    fetch(request)
        .then(res => res.json())
        .then(function(data) {
            console.log(data)
            var tableDiv = document.querySelector('table')
// createTabe(tableDiv)

            var video = document.querySelector('video')
            var videoName = video.getAttribute("name")
            console.log(videoName)
            generateTableContent(tableDiv, "File name   ", data.id)
            generateTableContent(tableDiv, "Capture date    ",  data.title)
            generateTableContent(tableDiv, "Algorithm   ", data.id)
            generateTableContent(tableDiv, "Number of items ", data.title)
        });
}

getData();

// var jsonData
// let Promise = new Promise(axios.get('../scripts/data.json'))
// Promise.then((data) => jsonData = data)
// Promise.catch((error) => alert(error))









