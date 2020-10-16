# TuringPi K3S Cluster Setup HybriotOS
[![Actions Status](https://github.com/cSDes1gn/blade-k3s/workflows/yaml-lint/badge.svg)](https://github.com/cSDes1gn/blade-k3s/actions) [![Actions Status](https://github.com/cSDes1gn/blade-k3s/workflows/shellcheck/badge.svg)](https://github.com/cSDes1gn/blade-k3s/actions)

![img](docs/img/tp.jpeg) ![img](docs/img/logo_tr.png)![img](docs/img/k3s.png) 

Modified: 2020-10

## Navigation
1. [Automating Cluster Setup](#Automated-F)
2. [Setup](#Setup)
3. [Quick Start](#Quickstart)
4. [Node Management](#node-management)


## Automating Cluster Setup

Downloading dependancies, flashing compute modules, setting up custom node configs are all tedious and time consuming processes. This repository leverages automation for faster and more consistent setup results for turingpi 

## Quickstart
Clone and run `make` following the prompts for hardware interactions:
```bash
git clone --recurse-submodules https://github.com/cSDes1gn/blade-k3s
make
```

This will create a `build` directory containing the latest HypriotOS image. To remove the build directory and perform other cleanup:
```bash
make clean
```

## Setup
1. Set the first jumper closest to the micro-usb slave programmer port so that it is on the pin with the small triangle indicator. This sets the pinstate to eMMC flash mode. 
2. Connect micro-usb to computer
3. Insert eMMC compute module into the master SO-DIMM slot
4. Power TuringPi using 12V VDC in or mini-ITX power cable
