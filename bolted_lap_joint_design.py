import math

# Available parameters
bolt_diameters = [10, 12, 16, 20, 24]  # in mm
bolt_grades = [3.6, 4.6, 4.8, 5.6, 5.8]
plate_grades = {
    "E250": 250,
    "E275": 275,
    "E300": 300,
    "E350": 350,
    "E410": 410
}

def get_bolt_strength(grade):
    fu = 100 * grade
    fy = (grade - int(grade)) * fu
    return fu, fy

def shear_capacity(fy, d):
    Ab = (math.pi / 4) * d**2
    Vb = 0.6 * fy * Ab / 1000  # kN
    return Vb

def bearing_capacity(fu, t, d):
    Vdpb = 2.5 * d * t * fu / 1000  # kN
    return Vdpb

def design_lap_joint(P, t1, t2, width):
    best_design = None
    for d in bolt_diameters:
        for gb in bolt_grades:
            for gp, fy_plate in plate_grades.items():
                fu_bolt, fy_bolt = get_bolt_strength(gb)
                Vb = shear_capacity(fy_bolt, d)
                N_bolts = math.ceil(P / (0.75 * Vb))
                if N_bolts < 3:
                    N_bolts = 3
                pitch = 2.5 * d
                gauge = 2.5 * d
                end_dist = 1.7 * d
                edge_dist = 1.5 * d
                length = pitch * (N_bolts - 1) + 2 * end_dist
                Vdpb = bearing_capacity(fu_bolt, t1 + t2, d)
                connection_strength = min(Vb, Vdpb) * N_bolts
                utilization_ratio = P / connection_strength

                if utilization_ratio <= 1:
                    design = {
                        "Bolt Diameter (mm)": d,
                        "Bolt Grade": gb,
                        "Plate Grade": gp,
                        "Number of Bolts": N_bolts,
                        "Pitch (mm)": pitch,
                        "Gauge (mm)": gauge,
                        "End Distance (mm)": round(end_dist),
                        "Edge Distance (mm)": round(edge_dist),
                        "Hole Diameter (mm)": d + 2,
                        "Connection Strength (kN)": round(connection_strength, 2),
                        "Utilization Ratio": round(utilization_ratio, 3),
                        "Length of Connection (mm)": round(length)
                    }

                    if best_design is None or design["Utilization Ratio"] > best_design["Utilization Ratio"]:
                        best_design = design

    return best_design

# Example input
P = float(input("Enter tensile force (kN): "))
t1 = float(input("Enter plate 1 thickness (mm): "))
t2 = float(input("Enter plate 2 thickness (mm): "))
width = float(input("Enter plate width (mm): "))

result = design_lap_joint(P, t1, t2, width)
print("\n--- Bolted Lap Joint Design Result ---")
for k, v in result.items():
    print(f"{k}: {v}")
