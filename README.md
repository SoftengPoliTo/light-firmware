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

**Description**:

The video demonstrates the automated integration of the `rust-code-analysis` tool into the Continuous Integration pipeline. The analysis begins with the installation of the tool from the official repository, followed by the preparation of output artifacts and the start of source code analysis, whose metadata is saved in JSON format (within the first 3 seconds).

A Python script then processes this data, analysing each function based on quality indicators such as:
* **Lines of Code (LOC)**
* **Cyclomatic Complexity**
* **Maintainability Index**
* **Halstead Effort**

The results are then summarised using a visual traffic light system: 🟢 good, 🟡 caution, 🔴 critical. 
This analysis allows for precisely identifying potentially problematic code segments in terms of complexity and maintainability, thus enabling timely corrective action during the continuous integration phase.


**Manifest Producer**

https://github.com/user-attachments/assets/b9393bf7-d749-4ec0-923d-ee547f3572d4

**Description**:

The video documents the use of `manifest-producer` as an integral part of the Continuous Integration pipeline, focusing on the security and structural analysis of the ELF binary file generated during project compilation. This is followed by an automated analysis of the binary's behaviour using reverse engineering techniques to disassemble the functions and reconstruct the main function's call graph.

The process begins with the tool's download and setup (0–6 seconds), and then continues with the analysis. During this phase, several automatic checks are performed: verification of the integrity of the ELF file, structural checks (class, endianness, headers), presence of active security protections (NX, RELRO, PIE, canary, etc.), detection of debug symbols or suspicious sections, through specific checks that return ✅ on success and ❌ on failure. At the end, a detailed report is produced in JSON format.

The central analysis phase follows (from the second 9), in which the tool reads and interprets the firmware, extracting key metadata, such as the programming language used, the linking at compile time, and its size. Based on this information, the tool identifies functions and, if necessary, demangles symbols in languages ​​that use obfuscated names. This allows the symbols to be correctly associated with readable function names. Then the tool moves on to function analysis, disassembling the machine code, identifying call instructions (to reconstruct the flow between functions), and identifying syscall instructions (to trace direct interactions with the operating system). The final phase (14-16 seconds) involves tracing the main function from the binary's entry point, thus generating a visual representation of the results via static HTML pages. Among these, one of the most relevant is the main function's call tree, which allows for in-depth inspection of the firmware's behaviour.


<!-- Links -->
[license]: https://github.com/SoftengPoliTo/light-firmware/blob/master/LICENSE

<!-- Badges -->
[license badge]: https://img.shields.io/badge/license-MIT-blue.svg
