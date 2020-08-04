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
            currentVideo.src = videoFile

            // update chart
            createChart(videoFilename)
        });
    }
}

async function createChart(videoFile) {
    const ctx = document.getElementById('myChart').getContext('2d');
    const data = parseJson(videoFile);

    const algorithms = Object.keys(j);

    var frames = {};
    var seconds = {};
    var objects = {};

    algorithms.forEach(algorithm => {
        frames[algorithm] = [];
        seconds[algorithm] = [];
        objects[algorithm] = {};

        data[algorithm].forEach(item => {
            frames[algorithm].push(item['frame']);
            seconds[algorithm].push(item['seconds']);
            const keys = Object.keys(item['objects'])
            keys.forEach(key => {
                objects[algorithm][key] = []
                objects[algorithm][key].push(item['objects'][key])
            });
        });
    });
    console.log(frames);
    console.log(seconds);
    console.log(objects);

    // const chart = new Chart(ctx, {
    //     // The type of chart we want to create
    //     type: 'line',
    //
    //     // The data for our dataset
    //
    //     data: {
    //         labels: data.seconds,
    //         datasets: [{
    //             label: 'Coches',
    //             backgroundColor: red,
    //             borderColor: red,
    //             fill: false,
    //             data: data.cars
    //
    //         }, {
    //             label: 'Personas',
    //             backgroundColor: blue,
    //             borderColor: blue,
    //             fill: false,
    //
    //             data: data.persons,
    //
    //         }]
    //     },
    //
    //     // Configuration options go here
    //     options: {
    //         // responsive: true,
    //         maintainAspectRatio: true,
    //         title: {
    //             display: true,
    //             text: 'Conteo de detecciones'
    //         },
    //         hover: {
    //             mode: 'nearest',
    //             intersect: true
    //         },
    //         scales: {
    //             xAxes: [{
    //                 display: true,
    //                 scaleLabel: {
    //                     display: true,
    //                     labelString: 'Segundos'
    //                 }
    //             }],
    //             yAxes: [{
    //                 display: true,
    //                 scaleLabel: {
    //                     display: true,
    //                     labelString: '# de detecciones'
    //                 }
    //             }],
    //             // xAxes: [{
    //             //     display:true
    //             // }]
    //
    //         }
    //     }
    // });
    // chart.update();
}

function getRandomColor() {
  const letters = '0123456789ABCDEF';
  let color = '#';
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

function parseJson(filename) {
    let j = {}

    const request = new Request(`/search?filename=${filename}`);
 
    fetch(request)
        .then(res =>  res.json())
        .then(function(data) {
            data.processing.forEach(processing => {
                j[processing['algorithm']] = []
                processing.detections.forEach(item =>{
                    const keys = Object.keys(item.objects);
                    const k = {'frame': item['frame'], 'seconds': item['seconds'], 'objects': {}};
                    keys.forEach(key => {
                        k['objects'][key] = item['objects'][key]['count'];
                    });
                    j[processing.algorithm].push(k)
                });
            });
        });
    return new Promise((resolve, reject) => {
        resolve(j);
    })
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
