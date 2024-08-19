// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;
library Device{
    enum State { Active, Suspended, Deactivated}
    enum Category {Security, Entertainment, Health, Monitoring}
    enum Zone {Zone1, Zone2, Zone3}
}