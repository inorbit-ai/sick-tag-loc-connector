#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

# Computes the translational transform between SICK Tag-LOC and InOrbit

# An ordered set of ground truth points in the InOrbit coordinate system
inorbit = [
    {"x": -10.276103973388672, "y": -4.393621826171875, "theta": -0.3944724500179291},
    {"x": -9.889497756958008, "y": -4.960001373291016, "theta": -0.1534339040517807},
    {"x": -9.820926666259766, "y": -5.260604286193848, "theta": 2.4598984718322754},
    {"x": -11.860822677612305, "y": -2.4610618591308597, "theta": 2.341604471206665},
]

# An order set of points in the SICK coordinate system that correspond to the above list
rtls = [
    {"x": 12.79, "y": -1.86},
    {"x": 13.29, "y": -1.13},
    {"x": 13.28, "y": -0.6},
    {"x": 11.77, "y": -3.41},
]

# Calculate average translations
translation_x = sum((b["x"] - a["x"]) for a, b in zip(inorbit, rtls)) / len(inorbit)
# The coordinate system for "Y" in SICK is reversed so negate everything
translation_y = -sum((b["y"] + a["y"]) for a, b in zip(inorbit, rtls)) / len(inorbit)

# Calculate average rotation - Since no theta in the SICK system, assume rotation based
# on coordinate changes might need to align system InOrbit's theta with the coordinate
# changes only. If thetas from the SICK system were known, they would be subtracted from
# each corresponding InOrbit theta.
theta_inorbit = [p["theta"] for p in inorbit]
# This is not directly useful without SICK system thetas
average_theta_inorbit = sum(theta_inorbit) / len(theta_inorbit)

print(f"translation_x: {translation_x}")
print(f"translation_y: {translation_y}")
print("-------------------------------")
print(f"average_theta_inorbit: {average_theta_inorbit}")
