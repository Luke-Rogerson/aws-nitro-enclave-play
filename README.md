# EC2 spin up commands

```
aws ec2 create-default-vpc
```

```
aws ec2 run-instances \
--image-id ami-0c85f77ef4c000593 \
--count 1 \
--instance-type m8g.large \
--key-name luke-nitro-deleteme \
--enclave-options 'Enabled=true' \
--tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=luke-nitro-deleteme-2}]' 
--block-device-mappings '[{"DeviceName":"/dev/xvda","Ebs":{"VolumeSize":50,"VolumeType":"gp3"}}]'
```

# Enclave creation commands

```bash
nitro-cli build-enclave --docker-uri lukerogerson1/enclave-py-server:0.0.3 --output-file vsock_sample_server.eif && 
nitro-cli run-enclave --eif-path vsock_sample_server.eif --cpu-count 1 --memory 512 
```

Optional: add `--debug-mode` to the `run-enclave` command to see the enclave logs.

This outputs something like:

```
{
  "EnclaveName": "vsock_sample_server",
  "EnclaveID": "i-0804c56943a5e079b-enc192b9de7158f7e2",
  "ProcessID": 25061,
  "EnclaveCID": 38,
  "NumberOfCPUs": 1,
  "CPUIDs": [
    1
  ],
  "MemoryMiB": 1024
}
```

Make a note of the `EnclaveCID` as this is the ID of the enclave that we will use to connect to the enclave.

Inside the `python/client` folder, use the `client.py` script to sign messages or verify signatures:

1. `python3 client.py client <EnclaveCID> 5005 --message "Hello world" --operation sign` (server listens on port 5005)
2. `python3 client.py client <EnclaveCID> 5005 --message "Hello world" --operation verify --signature <signature>`

# Benchmarks

## Local

#### Signing

`python3 client.py client 127.0.0.1 8001 --message 'Hello world' --operation sign`

CONNECTED LOCALLY
🕒 Connection time: 0.000268 seconds
🕒 Send message time: 0.000021 seconds
🕒 Receive response time: 0.005342 seconds
Response: 03ccf76a29908730e7ec38953a60a006c48e627743f5344a819d243a996505ec3f7729f839708ff78b5b7ccc69f171d6c33e97a0dcd2d890f1622041e59d1eb11b
🕒 Total process time: 0.005659 seconds

CONNECTED LOCALLY
🕒 Connection time: 0.000248 seconds
🕒 Send message time: 0.000016 seconds
🕒 Receive response time: 0.003700 seconds
Response: 03ccf76a29908730e7ec38953a60a006c48e627743f5344a819d243a996505ec3f7729f839708ff78b5b7ccc69f171d6c33e97a0dcd2d890f1622041e59d1eb11b
🕒 Total process time: 0.003988 seconds

CONNECTED LOCALLY
🕒 Connection time: 0.000306 seconds
🕒 Send message time: 0.000015 seconds
🕒 Receive response time: 0.003890 seconds
Response: 03ccf76a29908730e7ec38953a60a006c48e627743f5344a819d243a996505ec3f7729f839708ff78b5b7ccc69f171d6c33e97a0dcd2d890f1622041e59d1eb11b
🕒 Total process time: 0.004243 seconds

CONNECTED LOCALLY
🕒 Connection time: 0.000286 seconds
🕒 Send message time: 0.000016 seconds
🕒 Receive response time: 0.003723 seconds
Response: 03ccf76a29908730e7ec38953a60a006c48e627743f5344a819d243a996505ec3f7729f839708ff78b5b7ccc69f171d6c33e97a0dcd2d890f1622041e59d1eb11b
🕒 Total process time: 0.004054 seconds

CONNECTED LOCALLY
🕒 Connection time: 0.000303 seconds
🕒 Send message time: 0.000019 seconds
🕒 Receive response time: 0.003806 seconds
Response: 03ccf76a29908730e7ec38953a60a006c48e627743f5344a819d243a996505ec3f7729f839708ff78b5b7ccc69f171d6c33e97a0dcd2d890f1622041e59d1eb11b
🕒 Total process time: 0.004167 seconds


#### Verifying

`python3 client.py client 127.0.0.1 8001 --message "Hello world" --operation verify --signature 03ccf76a29908730e7ec38953a60a006c48e627743f5344a819d243a996505ec3f7729f839708ff78b5b7ccc69f171d6c33e97a0dcd2d890f1622041e59d1eb11b`

CONNECTED LOCALLY
🕒 Connection time: 0.000258 seconds
🕒 Send message time: 0.000017 seconds
🕒 Receive response time: 0.007261 seconds
Response: Signature valid: True
🕒 Total process time: 0.007571 seconds

CONNECTED LOCALLY
🕒 Connection time: 0.000354 seconds
🕒 Send message time: 0.000022 seconds
🕒 Receive response time: 0.007542 seconds
Response: Signature valid: True
🕒 Total process time: 0.007950 seconds

CONNECTED LOCALLY
🕒 Connection time: 0.000268 seconds
🕒 Send message time: 0.000016 seconds
🕒 Receive response time: 0.007146 seconds
Response: Signature valid: True
🕒 Total process time: 0.007459 seconds

CONNECTED LOCALLY
🕒 Connection time: 0.000313 seconds
🕒 Send message time: 0.000018 seconds
🕒 Receive response time: 0.007562 seconds
Response: Signature valid: True
🕒 Total process time: 0.007927 seconds

CONNECTED LOCALLY
🕒 Connection time: 0.000270 seconds
🕒 Send message time: 0.000015 seconds
🕒 Receive response time: 0.007259 seconds
Response: Signature valid: True
🕒 Total process time: 0.007573 seconds


## EC2

### Enclave

#### Signing

`python3 client.py client 35 5005 --message "Hello world" --operation sign`

🕒 Connection time: 0.002361 seconds
🕒 Send message time: 0.000045 seconds
🕒 Receive response time: 0.012443 seconds
Response: 03ccf76a29908730e7ec38953a60a006c48e627743f5344a819d243a996505ec3f7729f839708ff78b5b7ccc69f171d6c33e97a0dcd2d890f1622041e59d1eb11b
🕒 Total process time: 0.015110 seconds

🕒 Connection time: 0.012737 seconds
🕒 Send message time: 0.000012 seconds
🕒 Receive response time: 0.011869 seconds
Response: 03ccf76a29908730e7ec38953a60a006c48e627743f5344a819d243a996505ec3f7729f839708ff78b5b7ccc69f171d6c33e97a0dcd2d890f1622041e59d1eb11b
🕒 Total process time: 0.024684 seconds

🕒 Connection time: 0.016183 seconds
🕒 Send message time: 0.000011 seconds
🕒 Receive response time: 0.015836 seconds
Response: 03ccf76a29908730e7ec38953a60a006c48e627743f5344a819d243a996505ec3f7729f839708ff78b5b7ccc69f171d6c33e97a0dcd2d890f1622041e59d1eb11b
🕒 Total process time: 0.032099 seconds

🕒 Connection time: 0.012311 seconds
🕒 Send message time: 0.000011 seconds
🕒 Receive response time: 0.011834 seconds
Response: 03ccf76a29908730e7ec38953a60a006c48e627743f5344a819d243a996505ec3f7729f839708ff78b5b7ccc69f171d6c33e97a0dcd2d890f1622041e59d1eb11b
🕒 Total process time: 0.024227 seconds

🕒 Connection time: 0.012964 seconds
🕒 Send message time: 0.000010 seconds
🕒 Receive response time: 0.015873 seconds
Response: 03ccf76a29908730e7ec38953a60a006c48e627743f5344a819d243a996505ec3f7729f839708ff78b5b7ccc69f171d6c33e97a0dcd2d890f1622041e59d1eb11b
🕒 Total process time: 0.028910 seconds


#### Verifying

`python3 client.py client 35 5005 --message "Hello world" --operation verify --signature 03ccf76a29908730e7ec38953a60a006c48e627743f5344a819d243a996505ec3f7729f839708ff78b5b7ccc69f171d6c33e97a0dcd2d890f1622041e59d1eb11b`

🕒 Connection time: 0.013165 seconds
🕒 Send message time: 0.000013 seconds
🕒 Receive response time: 0.015872 seconds
Response: Signature valid: True
🕒 Total process time: 0.029119 seconds

🕒 Connection time: 0.015879 seconds
🕒 Send message time: 0.000011 seconds
🕒 Receive response time: 0.015875 seconds
Response: Signature valid: True
🕒 Total process time: 0.031829 seconds

🕒 Connection time: 0.012369 seconds
🕒 Send message time: 0.000011 seconds
🕒 Receive response time: 0.015839 seconds
Response: Signature valid: True
🕒 Total process time: 0.028289 seconds

🕒 Connection time: 0.014838 seconds
🕒 Send message time: 0.000012 seconds
🕒 Receive response time: 0.015786 seconds
Response: Signature valid: True
🕒 Total process time: 0.030703 seconds

🕒 Connection time: 0.012806 seconds
🕒 Send message time: 0.000012 seconds
🕒 Receive response time: 0.015892 seconds
Response: Signature valid: True
🕒 Total process time: 0.028779 seconds

### Non-enclave

#### Signing

`python3 client.py client 127.0.0.1 8001 --message 'Hello world' --operation sign`

CONNECTED LOCALLY
🕒 Connection time: 0.000306 seconds
🕒 Send message time: 0.004851 seconds
🕒 Receive response time: 0.000082 seconds
Response: 03ccf76a29908730e7ec38953a60a006c48e627743f5344a819d243a996505ec3f7729f839708ff78b5b7ccc69f171d6c33e97a0dcd2d890f1622041e59d1eb11b
🕒 Total process time: 0.005431 seconds

CONNECTED LOCALLY
🕒 Connection time: 0.000302 seconds
🕒 Send message time: 0.003263 seconds
🕒 Receive response time: 0.001753 seconds
Response: 03ccf76a29908730e7ec38953a60a006c48e627743f5344a819d243a996505ec3f7729f839708ff78b5b7ccc69f171d6c33e97a0dcd2d890f1622041e59d1eb11b
🕒 Total process time: 0.005499 seconds

CONNECTED LOCALLY
🕒 Connection time: 0.000262 seconds
🕒 Send message time: 0.004827 seconds
🕒 Receive response time: 0.000082 seconds
Response: 03ccf76a29908730e7ec38953a60a006c48e627743f5344a819d243a996505ec3f7729f839708ff78b5b7ccc69f171d6c33e97a0dcd2d890f1622041e59d1eb11b
🕒 Total process time: 0.005351 seconds

CONNECTED LOCALLY
🕒 Connection time: 0.000281 seconds
🕒 Send message time: 0.004884 seconds
🕒 Receive response time: 0.000080 seconds
Response: 03ccf76a29908730e7ec38953a60a006c48e627743f5344a819d243a996505ec3f7729f839708ff78b5b7ccc69f171d6c33e97a0dcd2d890f1622041e59d1eb11b
🕒 Total process time: 0.005435 seconds

CONNECTED LOCALLY
🕒 Connection time: 0.000281 seconds
🕒 Send message time: 0.004203 seconds
🕒 Receive response time: 0.000721 seconds
Response: 03ccf76a29908730e7ec38953a60a006c48e627743f5344a819d243a996505ec3f7729f839708ff78b5b7ccc69f171d6c33e97a0dcd2d890f1622041e59d1eb11b
🕒 Total process time: 0.005398 seconds


#### Verifying

`python3 client.py client 127.0.0.1 8001 --message "Hello world" --operation verify --signature 03ccf76a29908730e7ec38953a60a006c48e627743f5344a819d243a996505ec3f7729f839708ff78b5b7ccc69f171d6c33e97a0dcd2d890f1622041e59d1eb11b`

CONNECTED LOCALLY
🕒 Connection time: 0.000299 seconds
🕒 Send message time: 0.007054 seconds
🕒 Receive response time: 0.002537 seconds
Response: Signature valid: True
🕒 Total process time: 0.010084 seconds

CONNECTED LOCALLY
🕒 Connection time: 0.000315 seconds
🕒 Send message time: 0.004420 seconds
🕒 Receive response time: 0.005215 seconds
Response: Signature valid: True
🕒 Total process time: 0.010147 seconds

CONNECTED LOCALLY
🕒 Connection time: 0.000312 seconds
🕒 Send message time: 0.007151 seconds
🕒 Receive response time: 0.002508 seconds
Response: Signature valid: True
🕒 Total process time: 0.010173 seconds

CONNECTED LOCALLY
🕒 Connection time: 0.000385 seconds
🕒 Send message time: 0.007056 seconds
🕒 Receive response time: 0.002456 seconds
Response: Signature valid: True
🕒 Total process time: 0.010139 seconds

CONNECTED LOCALLY
🕒 Connection time: 0.000315 seconds
🕒 Send message time: 0.005162 seconds
🕒 Receive response time: 0.004473 seconds
Response: Signature valid: True
🕒 Total process time: 0.010165 seconds