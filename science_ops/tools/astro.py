from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Optional

import typer
from rich.console import Console

app = typer.Typer(help="Astronomy helpers: sidereal time and coordinate transforms.")
console = Console()


def _parse_datetime(dt_str: Optional[str]) -> datetime:
    """Parse an ISO8601 string; default to now (UTC)."""
    if dt_str is None:
        return datetime.now(timezone.utc)

    cleaned = dt_str.strip()
    if cleaned.endswith("Z"):
        cleaned = cleaned[:-1] + "+00:00"

    try:
        dt = datetime.fromisoformat(cleaned)
    except ValueError as exc:
        raise typer.BadParameter("Use ISO format like '2024-06-01T10:00:00Z'.") from exc

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _parse_ra(ra_str: str) -> float:
    """Parse right ascension string to degrees (default unit: hours)."""
    raw = ra_str.strip()
    negative = raw.startswith("-")
    text = raw.lower().replace(" ", "")

    # Allow RA provided directly in degrees if explicitly marked
    if "d" in text or "°" in text or "deg" in text:
        return _parse_dec(raw)

    if negative:
        text = text[1:]

    if all(marker not in text for marker in ["h", "m", "s", ":"]):
        try:
            numeric = float(text)
        except ValueError as exc:
            raise typer.BadParameter("Invalid RA format. Try '10h12m45s' or '10:12:45'.") from exc
        hours_value = numeric if numeric <= 24 else numeric / 15.0
        hours_value *= -1 if negative else 1
        return hours_value * 15.0

    cleaned = text.replace("h", " ").replace("m", " ").replace("s", " ").replace(":", " ")
    parts = [p for p in cleaned.split(" ") if p]
    try:
        hours = float(parts[0])
        minutes = float(parts[1]) if len(parts) > 1 else 0.0
        seconds = float(parts[2]) if len(parts) > 2 else 0.0
    except (IndexError, ValueError) as exc:
        raise typer.BadParameter("Invalid RA format. Try '10h12m45s' or '10:12:45'.") from exc

    total_hours = hours + minutes / 60.0 + seconds / 3600.0
    total_hours *= -1 if negative else 1
    return total_hours * 15.0


def _parse_dec(dec_str: str) -> float:
    """Parse declination to degrees."""
    raw = dec_str.strip()
    negative = raw.startswith("-")
    text = raw.lstrip("+-").strip().lower()
    text = text.replace("deg", "d").replace("°", "d")
    text = text.replace(" ", "")
    cleaned = text.replace("d", " ").replace("m", " ").replace("s", " ").replace(":", " ")
    parts = [p for p in cleaned.split(" ") if p]

    try:
        deg = float(parts[0])
        minutes = float(parts[1]) if len(parts) > 1 else 0.0
        seconds = float(parts[2]) if len(parts) > 2 else 0.0
    except (IndexError, ValueError) as exc:
        raise typer.BadParameter("Invalid Dec format. Try '-12d30m00s' or '-12:30:00'.") from exc

    total_deg = deg + minutes / 60.0 + seconds / 3600.0
    return -total_deg if negative else total_deg


def _julian_date(dt: datetime) -> float:
    """Compute Julian Date from a timezone-aware datetime."""
    year = dt.year
    month = dt.month
    day = dt.day + (dt.hour + dt.minute / 60 + dt.second / 3600 + dt.microsecond / 3.6e9) / 24

    if month <= 2:
        year -= 1
        month += 12

    a = math.floor(year / 100)
    b = 2 - a + math.floor(a / 4)
    jd = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + b - 1524.5
    return jd


def _gmst(dt: datetime) -> float:
    """Greenwich Mean Sidereal Time in degrees."""
    jd = _julian_date(dt)
    t = (jd - 2451545.0) / 36525.0
    gmst = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * t * t - (t * t * t) / 38710000.0
    return gmst % 360.0


def local_sidereal_time(dt: datetime, lon_deg: float) -> float:
    """Local sidereal time (degrees), longitude east-positive."""
    lst = _gmst(dt) + lon_deg
    return lst % 360.0


def ra_dec_to_altaz(ra_deg: float, dec_deg: float, lat_deg: float, lst_deg: float) -> tuple[float, float]:
    """Convert equatorial coords (deg) to altitude/azimuth (deg)."""
    ra_rad = math.radians(ra_deg)
    dec_rad = math.radians(dec_deg)
    lat_rad = math.radians(lat_deg)
    lst_rad = math.radians(lst_deg)
    ha = lst_rad - ra_rad

    sin_alt = math.sin(dec_rad) * math.sin(lat_rad) + math.cos(dec_rad) * math.cos(lat_rad) * math.cos(ha)
    alt = math.asin(sin_alt)

    cos_alt = math.cos(alt)
    if abs(cos_alt) < 1e-10:
        return math.degrees(alt), 0.0

    sin_az = -math.sin(ha) * math.cos(dec_rad) / cos_alt
    cos_az = (math.sin(dec_rad) - math.sin(alt) * math.sin(lat_rad)) / (cos_alt * math.cos(lat_rad))
    az = math.atan2(sin_az, cos_az)

    az_deg = (math.degrees(az) + 360.0) % 360.0
    return math.degrees(alt), az_deg


def _format_hours(deg_value: float) -> str:
    hours_total = (deg_value % 360.0) / 15.0
    h = int(hours_total)
    m = int((hours_total - h) * 60)
    s = (hours_total - h - m / 60.0) * 3600
    return f"{h:02d}h {m:02d}m {s:04.1f}s"


def _format_deg(deg_value: float) -> str:
    sign = "-" if deg_value < 0 else "+"
    value = abs(deg_value)
    d = int(value)
    m = int((value - d) * 60)
    s = (value - d - m / 60.0) * 3600
    return f"{sign}{d:02d}° {m:02d}' {s:04.1f}\""


@app.command("lst")
def lst_command(
    lon: float = typer.Option(..., help="Observer longitude in degrees (east positive)."),
    datetime_str: Optional[str] = typer.Option(None, "--datetime", "-d", help="ISO datetime, default: now (UTC)."),
) -> None:
    """Compute local sidereal time for a longitude."""
    dt = _parse_datetime(datetime_str)
    lst_deg = local_sidereal_time(dt, lon)
    console.print(f"LST @ {dt.isoformat()} for lon {lon:+.3f}°")
    console.print(f"Degrees: [bold]{lst_deg:.3f}°[/bold]")
    console.print(f"Hours  : [bold]{_format_hours(lst_deg)}[/bold]")


@app.command("altaz")
def altaz_command(
    ra: str = typer.Option(..., "--ra", help="Right ascension (e.g. '10h12m45s' or decimal hours)."),
    dec: str = typer.Option(..., "--dec", help="Declination (e.g. '-12d30m00s')."),
    lat: float = typer.Option(..., "--lat", help="Observer latitude in degrees."),
    lon: float = typer.Option(..., "--lon", help="Observer longitude in degrees (east positive)."),
    datetime_str: Optional[str] = typer.Option(None, "--datetime", "-d", help="ISO datetime, default: now (UTC)."),
) -> None:
    """Convert RA/Dec to altitude and azimuth for a given observer/time."""
    dt = _parse_datetime(datetime_str)
    ra_deg = _parse_ra(ra)
    dec_deg = _parse_dec(dec)
    lst_deg = local_sidereal_time(dt, lon)
    alt_deg, az_deg = ra_dec_to_altaz(ra_deg, dec_deg, lat, lst_deg)

    console.print(f"Observation time (UTC): {dt.isoformat()}")
    console.print(f"Local Sidereal Time   : {_format_hours(lst_deg)}")
    console.print(f"RA {ra} => {ra_deg:.3f}° | Dec {dec} => {dec_deg:.3f}°")
    console.print(f"Altitude: [bold]{alt_deg:.2f}°[/bold]")
    console.print(f"Azimuth : [bold]{az_deg:.2f}°[/bold] (0°=North, 90°=East)")
