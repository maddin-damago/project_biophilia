# ── Testdaten ────────────────────────────────────────────────
# schöner sommertag
temps = np.array([22, 23, 24, 23, 22])   # °C
humidity = np.array([40, 42, 45, 43, 41])   # %
uv = np.array([3, 4, 5, 4, 3])        # UV-Index
cloud = np.array([10, 15, 10, 20, 10])   # %
precip = np.array([0, 0, 0, 0, 0])        # % Regenwahrscheinlichkeit

ws = WeatherScore()

# ── Einzelne Scores ──────────────────────────────────────────
print("=== Schöner Sommertag ===")
print(f"Temperatur score:   {ws.temperature_score(temps):.1f}")
print(f"Luftfeuchtigkeits score:  {ws.humidity_score(humidity):.1f}")
print(f"UV score:           {ws.uv_score(uv):.1f}")
print(f"Bewölkungs score:    {ws.cloud_score(cloud):.1f}")
print(
    f"Niederschlagswahrscheinlichkeit : {ws.percipation_score(precip):.1f}")
# print(
# f">>> Gesamt:   {ws.combined_score(temps, humidity, uv, cloud):.1f}")
score, warnings = ws.combined_score(temps, humidity, uv, cloud)
print(f">>> Gesamt:   {score:.1f}")
for w in warnings:
    print(f"  ⚠ {w}")

# ── Regnerischer Tag ─────────────────────────────────────────
temps2 = np.array([22, 23, 21, 22, 23])  # °C
humidity2 = np.array([80, 85, 90, 88, 82])  # %
uv2 = np.array([1, 1, 2, 1, 1])       # UV-Index
cloud2 = np.array([90, 95, 100, 90, 95])  # %
precip2 = np.array([80, 90, 85, 70, 80])  # % Regenwahrscheinlichkeit

print("\n=== Regnerischer Tag ===")
print(f"Temperatur:   {ws.temperature_score(temps2):.1f}")
print(f"Luftfeuchte:  {ws.humidity_score(humidity2):.1f}")
print(f"UV:           {ws.uv_score(uv2):.1f}")
print(f"Bewölkung:    {ws.cloud_score(cloud2):.1f}")
print(f"Niederschlag: {ws.percipation_score(precip2):.1f}")

score2, warnings2 = ws.combined_score(temps2, humidity2, uv2, cloud2)


print(
    # f">>> Gesamt:   {ws.combined_score(temps2, humidity2, uv2, cloud2)[0]:.1f}")
    f">>> Gesamt: {score2:.1f}")
for w in warnings2:
    print(f"  ⚠ {w}")


# ── Extremer Hitzetag(schwül)────────────────────────────────────────
temps3 = np.array([38, 39, 40, 39, 38])  # °C
humidity3 = np.array([20, 18, 15, 18, 20])  # %
uv3 = np.array([10, 11, 11, 11, 10])  # UV-Index
cloud3 = np.array([0, 0, 5, 0, 0])       # %
precip3 = np.array([0, 0, 0, 0, 0])       # % Regenwahrscheinlichkeit


print("\n=== Extremer Hitzetag ===")
print(f"Temperatur:   {ws.temperature_score(temps3):.1f}")
print(f"Luftfeuchte:  {ws.humidity_score(humidity3):.1f}")
print(f"UV:           {ws.uv_score(uv3):.1f}")
print(f"Bewölkung:    {ws.cloud_score(cloud3):.1f}")
# print(f"Niederschlag: {ws.percipation_score(precip3):.1f}")

score3, warnings3 = ws.combined_score(temps3, humidity3, uv3, cloud3)

print(
    # f">>> Gesamt:   {ws.combined_score(temps3, humidity3, uv3, cloud3)[0]:.1f}")
    f">>> Gesamt: {score3:.1f}")
for w in warnings3:
    print(f"  ⚠ {w}")


# ── Trockener Grautag ────────────────────────────────────────
temps_grau4 = np.array([15, 16, 15, 14, 15])  # °C
humidity_grau4 = np.array([28, 30, 32, 29, 31])  # %
uv_grau4 = np.array([1, 1, 1, 1, 1])       # UV-Index
cloud_grau4 = np.array([90, 92, 95, 88, 91])  # %
precip_grau4 = np.array([5, 10, 5, 0, 5])       # % Regenwahrscheinlichkeit

print("\n=== Trockener Grautag ===")
print(f"Temperatur:   {ws.temperature_score(temps_grau4):.1f}")
print(f"Luftfeuchte:  {ws.humidity_score(humidity_grau4):.1f}")
print(f"UV:           {ws.uv_score(uv_grau4):.1f}")
print(f"Bewölkung:    {ws.cloud_score(cloud_grau4):.1f}")
print(f"Niederschlag: {ws.percipation_score(precip_grau4):.1f}")

score_grau, warnings_grau = ws.combined_score(
    temps_grau4, humidity_grau4, uv_grau4, cloud_grau4)

print(f">>> Gesamt: {score_grau:.1f}")
for w in warnings_grau:
    print(f"  ⚠ {w}")


# ── Thermoregulations-Stress ──────────────────────────────────
temps_stress5 = np.array([6, 12, 22, 18, 7])  # °C
humidity_stress5 = np.array([50, 45, 40, 45, 50])  # %
uv_stress5 = np.array([3, 4, 5, 3, 1])       # UV-Index
cloud_stress5 = np.array([10, 10, 15, 20, 10])  # %
precip_stress5 = np.array([0, 0, 0, 0, 0])       # % Regenwahrscheinlichkeit

print("\n=== Thermoregulations-Stress ===")
print(f"Temperatur:   {ws.temperature_score(temps_stress5):.1f}")
print(f"Luftfeuchte:  {ws.humidity_score(humidity_stress5):.1f}")
print(f"UV:           {ws.uv_score(uv_stress5):.1f}")
print(f"Bewölkung:    {ws.cloud_score(cloud_stress5):.1f}")
print(f"Niederschlag: {ws.percipation_score(precip_stress5):.1f}")

score_stress, warnings_stress = ws.combined_score(
    temps_stress5, humidity_stress5, uv_stress5, cloud_stress5)

print(f">>> Gesamt: {score_stress:.1f}")
for w in warnings_stress:
    print(f"  ⚠ {w}")


# ── Hitze ohne Lichtbonus ────────────────────────────────────
temps_licht6 = np.array([31, 32, 33, 32, 31])  # °C
humidity_licht6 = np.array([40, 42, 45, 43, 41])  # %
uv_licht6 = np.array([0.5, 0.8, 0.6, 0.4, 0.5])  # UV-Index
cloud_licht6 = np.array([50, 60, 55, 65, 50])  # %
precip_licht6 = np.array([10, 15, 10, 5, 10])     # % Regenwahrscheinlichkeit

print("\n=== Hitze ohne Lichtbonus ===")
print(f"Temperatur:   {ws.temperature_score(temps_licht6):.1f}")
print(f"Luftfeuchte:  {ws.humidity_score(humidity_licht6):.1f}")
print(f"UV:           {ws.uv_score(uv_licht6):.1f}")
print(f"Bewölkung:    {ws.cloud_score(cloud_licht6):.1f}")
print(f"Niederschlag: {ws.percipation_score(precip_licht6):.1f}")

score_licht, warnings_licht = ws.combined_score(
    temps_licht6, humidity_licht6, uv_licht6, cloud_licht6)

print(f">>> Gesamt: {score_licht:.1f}")
for w in warnings_licht:
    print(f"  ⚠ {w}")
