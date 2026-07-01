import numpy as np

from dataclasses import dataclass


@dataclass
class WeatherScore:

    def temperature_score(self, temps: np.ndarray) -> float:
        avg = float(np.mean(temps))
        score = float(np.interp(
            avg,
            [-1, 0, 10, 20, 25, 35, 36],
            [0, 10, 40, 80, 100, 40, 0]
        ))
        return score

    def humidity_score(self, humidity: np.ndarray) -> float:
        avg = float(np.mean(humidity))
        score = float(np.interp(
            avg,
            [0, 20, 30, 60, 75, 85, 100],
            [40, 70, 100, 100, 60, 30, 0]
        ))
        return score

    def uv_score(self, uv: np.ndarray) -> float:
        avg = float(np.mean(uv))
        score = float(np.interp(
            avg,
            [1, 3, 5, 8, 10, 11],  # uv-indizes
            [100, 80, 80, 50, 20, 0]
        ))
        return score

    def cloud_score(self, cloud_cover: np.ndarray) -> float:
        avg = float(np.mean(cloud_cover))
        score = float(np.interp(
            avg,
            [0, 20, 50, 80, 100],  # bewölkung in %
            [80, 100, 60, 20, 0]
        ))
        return score

    def percipation_score(self, precip: np.ndarray) -> float:
        avg = float(np.mean(precip))
        score = float(np.interp(
            avg,
            [0, 20, 50, 80, 100],  # in %
            [100, 80, 40, 10, 0]
        ))
        return score

    def interaction_penalty(
        self,
        temps: np.ndarray,
        humidity: np.ndarray,
        cloud_cover: np.ndarray,
        uv: np.ndarray,
    ) -> tuple[float, list[str]]:
        """
        strafpunkte für paradoxe wetterkonstellationen.
        gibt (penalty: float, warnungen: list[str]) zurück.
        """
        avg_temp = float(np.mean(temps))
        avg_humid = float(np.mean(humidity))
        avg_cloud = float(np.mean(cloud_cover))
        avg_uv = float(np.mean(uv))
        temp_diff = float(np.max(temps) - np.min(temps))

        penalty = 0.0
        warnings = []

        # 1. hitzestress: heiß + wolkenlos
        if avg_temp > 35 and avg_cloud < 20:
            penalty += 20
            warnings.append(
                f"Hitzestress-Falle: {avg_temp:.1f}°C Temperatur + {avg_cloud:.0f}% Bewölkung "
                f"(-20 Pkt). Direkte Sonne verstärkt Hitzestress stark."
            )

        # 2. schwül: angenehme temperatur + sehr hohe luftfeuchtigkeit oder hohe temperatur + hohe luftfeuchtigkeit
        if 20 <= avg_temp <= 26 and avg_humid > 80:
            penalty += 15
            warnings.append(
                f"Schwüle-Falle: {avg_temp:.1f}°C Temperatur + {avg_humid:.0f}% Luftfeuchtigkeit "
                f"(-15 Pkt). Schwitzen wird erschwert, Erschöpfung steigt."
            )
        elif 27 < avg_temp and avg_humid >= 52:
            penalty += 15
            warnings.append(
                f"Schwüle-Falle: {avg_temp:.1f}°C Temperatur + {avg_humid:.0f}% Luftfeuchtigkeit "
                f"(-15 Pkt). Schwitzen wird erschwert, Erschöpfung steigt."
            )

        # 3. trockener grautag: bewölkt + trocken
        if avg_cloud > 85 and avg_humid < 35:
            penalty += 10
            warnings.append(
                f"Trockener Grautag: {avg_cloud:.0f}% Bewölkung + {avg_humid:.0f}% Luftfeuchtigkeit "
                f"(-10 Pkt). Lichtmangel und trockene Luft kombinieren sich negativ."
            )

        # 4. thermoregulations-stress: große temperaturschwankung im tag
        if temp_diff > 12:
            penalty += 10
            warnings.append(
                f"Thermoregulations-Stress: Temperaturdifferenz {temp_diff:.1f}°C "
                f"(-10 Pkt). Körper muss ständig zwischen Kälte und Hitze umschalten."
            )

        # 5. hitze ohne lichtbonus: heiß aber kein UV
        if avg_temp > 30 and avg_uv < 1:
            penalty += 5
            warnings.append(
                f"Hitze ohne Lichtbonus: {avg_temp:.1f}°C + UV {avg_uv:.1f} "
                f"(-10 Pkt). Hitzebelastung ohne positiven Serotonin-Effekt."
            )

        return penalty, warnings

    def combined_score(
        self,
        temps: np.ndarray,
        humidity: np.ndarray,
        uv: np.ndarray,
        cloud: np.ndarray,
        # precip: np.ndarray,
    ) -> tuple[float, list[str]]:

        weights = {
            # "precipitation": 0.35,
            "temperature": 0.40,
            "cloud": 0.35,
            "humidity": 0.15,
            "uv": 0.10
        }

        scores = {
            # "precipitation": self.percipation_score(precip),
            "temperature": self.temperature_score(temps),
            "cloud": self.cloud_score(cloud),
            "humidity": self.humidity_score(humidity),
            "uv": self.uv_score(uv),
        }

        base_score = float(sum(scores[key] * weights[key]
                               for key in weights))

        penalty, warnings = self.interaction_penalty(
            temps, humidity, cloud, uv)

        final_score = float(np.clip(base_score - penalty, 0, 100))
        return final_score, warnings
