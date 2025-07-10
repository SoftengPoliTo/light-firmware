# Light

[![LICENSE][license badge]][license]

A light firmware written with the `Ascot` framework.

## Building

Run the command

```console
cargo build
```

## Running the server

The server runs on `localhost` and listens to port `3000`. To make it run:

```console
cargo run
```

## REST API examples

Through `curl` or a web browser, it is possible to call the APIs which perform
some actions on a device.

**Turn a light on**

```console
curl -X PUT 127.0.0.1:3000/light/on/4.0/true
```

```console
curl -X POST 127.0.0.1:3000/light/on/4.0/true
```

**Turn a light off**

```console
curl -X PUT 127.0.0.1:3000/light/off
```

**Toggle a light**

```console
curl -X PUT 127.0.0.1:3000/light/toggle
```

At server startup, an initial message signalling its effective execution
is printed.

```
Starting server...
```

## Continuous Integration

**Code Quality**

https://github.com/user-attachments/assets/b51e0b8b-f60f-4922-82d1-b609f46e0cee


**Manifest Producer**

https://github.com/user-attachments/assets/b9393bf7-d749-4ec0-923d-ee547f3572d4



<!-- Links -->
[license]: https://github.com/SoftengPoliTo/light-firmware/blob/master/LICENSE

<!-- Badges -->
[license badge]: https://img.shields.io/badge/license-MIT-blue.svg
