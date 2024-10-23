const net = require('net');
const { ethers } = require('ethers');

const privateKey = "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
const wallet = new ethers.Wallet(privateKey);
const message = "Message to be signed";

// const SOCKET_ADDRESS = '/tmp/vsock_test.sock'; // local
const SOCKET_ADDRESS = '/var/run/nitro_enclaves/vsocks/8001.sock'

console.time('---- TOTAL PROCESS TIME ----');

async function signAndSendMessage() {
    // Generate the signature
    console.time('---- SIGNATURE GENERATION TIME ----');
    const signature = await wallet.signMessage(message);
    console.log('signature :', signature);
    console.timeEnd('---- SIGNATURE GENERATION TIME ----');

    // Send the signature over vsock
    console.time('---- VSOCKET COMMUNICATION TIME ----');
    const client = net.createConnection(SOCKET_ADDRESS, () => {
        client.write(signature, () => {
            client.end();
            console.timeEnd('---- VSOCKET COMMUNICATION TIME ----');
            console.timeEnd('---- TOTAL PROCESS TIME ----');  // End total timer
        });
    });
}

signAndSendMessage();

setTimeout(() => {
    console.log("Exiting...");
}, 60000);