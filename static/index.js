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
    // const data = parseJson(videoFile);

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
            responsive: true,
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
                }]
            }
        }
    });
    chart.update();
}

function parseJson(filename) {
    let cars = [];
    let seconds = [];
    let persons = [];
    let i = 0;

    const request = new Request(`/search?filename=${filename}`);

    fetch(request)
        .then(res => res.json())
        .then(function(data) {
            data.processing.forEach(function(processingObjects) {
                processingObjects.detections.forEach(function(detectionsObjects) {

                    // TODO: need better method of getting this json data.
                    cars.push(detectionsObjects.objects.car)
                    seconds.push(detectionsObjects.seconds)
                    persons.push(detectionsObjects.objects.person)
                    i++
                })
            });
        });

    return {
        cars: cars,
        seconds: seconds,
        persons: persons
    }
}