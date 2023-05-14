const axios = require('axios');
// const axios_binary = require('axios-binary');
// axios_binary(axios);

const url = 'http://127.0.0.1:5000/data';

const sendRequest = async () => {
    const response = await axios.post(url, {
        command: 'cube'
    }, {
        responseType: 'arraybuffer',
    });

    // Ensure we're dealing with an ArrayBuffer
    let buf = response.data;
    if (buf instanceof Buffer) {
        buf = Uint8Array.from(buf).buffer;
    }

    const data = new DataView(buf);
    const vertices = [];
    const faces = [];

    // Read the number of vertices and faces from the first two integers
    const vertexCount = data.getInt32(0, true);
    const faceCount = data.getInt32(4, true);
    

    const vertSize = 3 * 4;
    const metadataOffset = 8; 
    // Assume each vertex consists of three float32 numbers
    for (let i = 0; i < vertexCount; i++) {
        const x = data.getFloat32(metadataOffset + i * vertSize, true);
        const y = data.getFloat32(metadataOffset + i * vertSize + 4, true);
        const z = data.getFloat32(metadataOffset + i * vertSize + 8, true);
        vertices.push([x, y, z]);
    }

    const faceSize = 4 * 4;
    const vertexOffset = vertexCount * 12;
    // Assume each face consists of three int32 numbers
    for (let i = 0; i < faceCount; i++) {
        const a = data.getInt32(metadataOffset + vertexOffset + i * faceSize, true);
        const b = data.getInt32(metadataOffset + vertexOffset + i * faceSize + 4, true);
        const c = data.getInt32(metadataOffset + vertexOffset + i * faceSize + 8, true);
        const d = data.getInt32(metadataOffset + vertexOffset + i * faceSize + 12, true);
        faces.push([a, b, c, d]);
    }
    console.log(vertices, faces);
};

sendRequest().catch(console.error);
