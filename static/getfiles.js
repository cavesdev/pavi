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


var form = document.querySelector('form')
var file = document.querySelector('[type=file]').files
var formData = new FormData();

formData.append("File", file[0]);
console.log(formData)
form.addEventListener('submit', (e) => {

        e.preventDefault();
})

postReq(formData);