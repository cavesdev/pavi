document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.getElementsByClassName('video-name');

    addClickListener(buttons);

    // first chart displayed
    const firstVideoFilename = buttons[0].innerHTML
    createChart(firstVideoFilename);
});

function addClickListener(buttons) {
    for (let btn of buttons) {
        btn.addEventListener('click', event => {
            const videoFilename = event.target.innerHTML;
            const videoFile = `../static/videos/${videoFilename}.mp4`

            // load new video
            const currentVideo = document.querySelector('#currentVideo');
            console.log(currentVideo.src)
            currentVideo.src = videoFile
            console.log(currentVideo.src)

            // update chart
            createChart(videoFilename)
        });
    }
}

function createChart(videoFile) {
    const ctx = document.getElementById('myChart').getContext('2d');
    const data = parseJson(videoFile);

    const red = 'rgb(255, 51,34)'
    const blue = 'rgb(91,192,222)'

    const chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'line',

        // The data for our dataset
        data: {
            labels: data.seconds,
            datasets: [{
                label: 'Coches',
                backgroundColor: red,
                borderColor: red,
                fill: false,
                data: data.cars

            }, {
                label: 'Personas',
                backgroundColor: blue,
                borderColor: blue,
                fill: false,

                data: data.persons,
                
            }]
        },

        // Configuration options go here
        options: {
            // responsive: true,
            maintainAspectRatio: true,
            title: {
                display: true,
                text: 'Conteo de detecciones'
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Segundos'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: '# de detecciones'
                    }
                }],
                // xAxes: [{
                //     display:true
                // }]

            }
        }
    });
    chart.update();
}

function parseJson(filename) {
    let cars = [];
    let seconds = [];
    let persons = [];

    const request = new Request(`/search?filename=${filename}`);
 
    fetch(request)
        .then(res =>  res.json())
        .then(function(data) {
            data.processing.forEach(element => {
                element.detections.forEach(items =>{
                    if(items.objects.car != null){
                        cars.push(items.objects.car.count);
                        seconds.push(items.seconds);
                        console.log(items.seconds)
                    }

                    if(items.objects.person != null){
                        persons.push(items.objects.person.count)
                        // seconds.push(items.objects.person.seconds)

                    }
                    
                })
            });
            
        });

    return {
        cars: cars,
        seconds: seconds,
        persons: persons
    }
}





function postReq(data){
    const params = {
        headers:{
            "contente-type":"application/json; charset=UTF-8"
        },
        body:{
            id:1,
            title:"test"
        },

        method: "post"

    }
    let baseURL = 'localhost:5500/process'

    fetch("https://my-json-server.typicode.com/typicode/demo/posts", params)
    .then(res => {console.log(JSON.stringify(res))})
}
