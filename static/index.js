var chartBaseURL;

document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.getElementsByClassName('video-name');
    const chart = document.getElementById('chart');
    chartBaseURL = chart.src;
    chart.src = chartBaseURL + `&filter={"filename":%20"${buttons[0].innerHTML}"}`
    addClickListener(buttons);
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
            const chart = document.getElementById('chart');
            chart.src = chartBaseURL + `&filter={"filename":%20"${videoFilename}"}`
        });
    }
}