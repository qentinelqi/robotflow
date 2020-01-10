# RobotFlow

Controlling Robot Framework RPA flow with flowcharts

## Overview

Robot Flow is a RPA tool for Robot Framework (RF). It uses flow charts to control task execution order. Robot Flow is based on concept by Mika Kaukoranta <mika.kaukoranta@gmail.com>

High level process can be  designed in flowchart editor while RPA task steps are finished in Robot Framework. That makes overall flow easy to understand even for non programmers while still retaining Robot Framework more programming language like syntax for low level task implementation.

## Required tools

* Robot Framework 3.2 alpha 1 or later (3.2.dev1)
* Graphml drawing tool like [yEd Graph Editor](https://www.yworks.com/products/yed)

## Installation

Download both files from from this repository listeners folder and place them in a suitable location. Usually recommended place is listeners folder next to tests folder.

## Usage

1. Create high a level RPA flow using flow chart editor.
1. Write RPA tasks with Robot Framework
1. Robot Framework task name must match ones in flow chart. Names are case sensitive
1. Place both files in same directory and check that their names are same but with different suffix
1. Run Robot Framework with RobotFlow listener `robot -L RobotFlow.py mytask.robot`

## Demo

### Introduction

This repository contains a demo application and RPA scripts that show how this can be used. Application is in demo folder.

Script reads customerid's from input.xml, checks their status from application and writes output to output.xml.

There are two robot files:

* checkcustomer.robot
  * This script uses RobotFlow to control process execution
* checkcustomer-rf.robot
  * This script is written in traditional Robot Framework style and does not use RobotFlow

### Usage instructions

To use demo application:

1. Install required libraries
1. Start demoserver: `python demoserver.py`
1. Server opens to localhost port 8080
1. Run RPA with this command: `robot --rpa --listener ../listeners/RobotFlow.py checkuser.robot`

## Tests

Tests are in test directory. You can run them using Robot Framework

``` bash
cd tests
robot --listener ../listeners/RobotFlow.py test1.robot
```

## License

RobotFlow is released under Apache license. See the bundled [LICENSE](LICENSE.txt) file for details.
