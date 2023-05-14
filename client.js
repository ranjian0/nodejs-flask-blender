const axios = require('axios');
const url = 'http://127.0.0.1:5000/data';

const sendRequest = async () => {
    const response = await axios.post(url, {
        command: 'cube'
    }, {
        responseType: 'json',
    });

    if (response.data.error) {
        console.log(`Error: ${response.data.error}`);
        return;
    }

    const vertices = response.data.vertices;
    const faces = response.data.faces;
    console.log(vertices, faces)
};

sendRequest().catch(console.error);
