## Pull, build and run the enclave

Make sure [vsock-proxy](https://github.com/aws/aws-nitro-enclaves-cli/tree/main/vsock_proxy) is running on host machine - `./enclave-cli/build/vsock_proxy/aarch64-unknown-linux-musl/release/vsock-proxy 8000 api.binance.com 443`

```
nitro-cli terminate-enclave --all && docker pull lukerogerson1/enclave-py-binance-ssl-check:0.0.15 && nitro-cli build-enclave --docker-uri lukerogerson1/enclave-py-binance-ssl-check:0.0.15 --output-file binance_thing.eif &&  nitro-cli run-enclave --eif-path binance.eif --cpu-count 1 --memory 1500 --enclave-cid 26  --debug-mode
```
