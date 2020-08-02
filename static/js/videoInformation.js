
// function createTabe(table){
//     let tHead = table.createTHead();
//     let row = table.insertRow();

//     let th = document.createElement("tr");
//     let td = document.createElement('tr');
//     td.textContent = "test"
//     let text = document.createTextNode("test");
//     th.appendChild(text)
//     th.appendChild(td)
//     row.appendChild(th)
//     var video = document.querySelector('video')
//     var videoName = video.getAttribute("name")
// }


function generateTableContent(table, rowName, data){
    let row = table.insertRow();

    let cell = row.insertCell();

    let text = document.createTextNode(rowName);
    let text2 = document.createTextNode(data);

    cell.appendChild(text)
    cell.appendChild(text2)

}

function getData() {
    const request = new Request(`/search?filename=trim`);

    fetch(request)
        .then(res => res.json())
        .then(function(data) {
            console.log(data)
            var tableDiv = document.querySelector('table')
            // createTabe(tableDiv)        
            generateTableContent(tableDiv, "File name   ", data.filename)
            generateTableContent(tableDiv, "Capture date    ",  data.capture_date)
            generateTableContent(tableDiv, "Algorithm   ", data.processing[0].algorithm)
            console.log(data.processing)
            let carCounter =0;
            let personCounter =0;
            data.processing.forEach(element => {
                element.detections.forEach(items =>{
                    if(items.objects.car != null){
                        carCounter += items.objects.car.count
                    }

                    if(items.objects.person != null){
                        personCounter += items.objects.person.count
                    }
                    
                    
                })
            });
            generateTableContent(tableDiv, "Number of cars  ", carCounter)
            generateTableContent(tableDiv, "Number of persons   ", personCounter)
            
        })
        .catch(error => console.error(error));
}



var currentVideo = document.querySelector('#currentVideo');
console.log(currentVideo.getAttribute(name))

getData();

// var jsonData
// let Promise = new Promise(axios.get('../scripts/data.json'))
// Promise.then((data) => jsonData = data)
// Promise.catch((error) => alert(error))









