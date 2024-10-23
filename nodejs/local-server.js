const net = require('net');
const fs = require('fs');

const socketPath = '/tmp/vsock_test.sock';

// Ensure the socket file doesn't exist
if (fs.existsSync(socketPath)) {
    fs.unlinkSync(socketPath);
}

const server = net.createServer((client) => {
    client.on('data', (data) => {
        console.log('Received signature: ', data.toString());
    });
});

server.listen(socketPath, () => {
    console.log(`Listening on ${socketPath}`);
});