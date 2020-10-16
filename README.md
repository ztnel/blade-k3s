# Automation for TuringPi K3S Blade Cluster using HybriotOS
[![Actions Status](https://github.com/cSDes1gn/blade-k3s/workflows/yaml-lint/badge.svg)](https://github.com/cSDes1gn/blade-k3s/actions) [![Actions Status](https://github.com/cSDes1gn/blade-k3s/workflows/shellcheck/badge.svg)](https://github.com/cSDes1gn/blade-k3s/actions)

![img](docs/img/tp.jpeg) ![img](docs/img/logo_tr.png)![img](docs/img/k3s.png) 

Modified: 2020-10

## Navigation
1. [Automating Cluster Setup](#automating-cluster-setup)
2. [TuringPi Setup](#turingpi-setup)
3. [Quickstart](#quickstart)
4. [License](#license)

## Automating Cluster Setup

Downloading dependancies, flashing compute modules, setting up custom node configs are all tedious and time consuming processes. This repository leverages automation for faster and more consistent setup results for turingpi 

## TuringPi Setup
1. Set the first jumper closest to the micro-usb slave programmer port so that it is on the pin with the small triangle indicator. This sets the pinstate to eMMC flash mode. 
2. Connect micro-usb to your local machine
3. Insert eMMC compute module into the master SO-DIMM slot
4. Power TuringPi using 12V VDC in or mini-ITX power cable

## Quickstart
Clone and run setup to generate build artefacts:
```bash
git clone --recurse-submodules https://github.com/cSDes1gn/blade-k3s
```
```bash
make setup
```
This will create a `build` directory build artefacts. To remove the build directory after flashing nodes and perform other cleanup:
```bash
make clean
```
Prepare TuringPi board for slave port flashing as per [instructions](#turingpi-setup) then run following the prompts:
```bash
make flash
```

## License
[GNU General Public License v3.0](#LICENSE)


