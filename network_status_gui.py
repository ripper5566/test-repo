#!/usr/bin/env python3
"""Simple Tkinter GUI to display network security and connectivity information."""
from __future__ import annotations

import json
import os
import socket
import subprocess
import threading
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Optional, Tuple

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError as exc:  # pragma: no cover - Tkinter missing
    raise SystemExit("Tkinter is required to run this application") from exc


@dataclass
class ProxyInfo:
    http: Optional[str]
    https: Optional[str]
    no_proxy: Optional[str]


@dataclass
class ConnectivityStatus:
    is_connected: bool
    latency_ms: Optional[float]
    error: Optional[str] = None


@dataclass
class PublicIPInfo:
    ip: Optional[str]
    isp: Optional[str]
    country_name: Optional[str]
    country_code: Optional[str]
    raw_json: Optional[str]
    error: Optional[str] = None


def check_connectivity(host: str = "1.1.1.1", port: int = 53, timeout: float = 3.0) -> ConnectivityStatus:
    """Try to open a socket connection to determine internet connectivity."""
    start = time.perf_counter()
    sock: Optional[socket.socket] = None
    try:
        sock = socket.create_connection((host, port), timeout=timeout)
        latency = (time.perf_counter() - start) * 1000.0
        return ConnectivityStatus(True, latency_ms=latency)
    except OSError as exc:
        return ConnectivityStatus(False, latency_ms=None, error=str(exc))
    finally:
        if sock:
            sock.close()


def get_proxy_info() -> ProxyInfo:
    """Fetch proxy settings from environment variables."""
    return ProxyInfo(
        http=os.environ.get("http_proxy") or os.environ.get("HTTP_PROXY"),
        https=os.environ.get("https_proxy") or os.environ.get("HTTPS_PROXY"),
        no_proxy=os.environ.get("no_proxy") or os.environ.get("NO_PROXY"),
    )


def _run_command(command: list[str]) -> Tuple[int, str, str]:
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )
        return completed.returncode, completed.stdout.strip(), completed.stderr.strip()
    except FileNotFoundError:
        return 127, "", "command not found"


def get_wifi_ssid() -> Optional[str]:
    """Attempt to detect the active Wi-Fi SSID using platform specific tools."""
    # Try Linux tools first
    returncode, stdout, _ = _run_command(["nmcli", "-t", "-f", "ACTIVE,SSID", "dev", "wifi"])
    if returncode == 0 and stdout:
        for line in stdout.splitlines():
            if line.startswith("yes:"):
                return line.split(":", 1)[1] or None
    returncode, stdout, _ = _run_command(["iwgetid", "-r"])
    if returncode == 0 and stdout:
        return stdout.strip()

    # Windows
    returncode, stdout, _ = _run_command(["netsh", "wlan", "show", "interfaces"])
    if returncode == 0 and stdout:
        for line in stdout.splitlines():
            if "SSID" in line and "BSSID" not in line:
                _, ssid = line.split(":", 1)
                return ssid.strip() or None

    return None


def fetch_public_ip_info(timeout: float = 5.0) -> PublicIPInfo:
    url = "https://ipapi.co/json/"
    request = urllib.request.Request(url, headers={"User-Agent": "NetworkStatusGUI/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        return PublicIPInfo(None, None, None, None, None, error=str(exc))

    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        return PublicIPInfo(None, None, None, None, payload, error=str(exc))

    return PublicIPInfo(
        ip=data.get("ip"),
        isp=data.get("org"),
        country_name=data.get("country_name"),
        country_code=data.get("country"),
        raw_json=json.dumps(data, indent=2),
    )


def fetch_flag_image(country_code: str, timeout: float = 5.0) -> Optional[tk.PhotoImage]:
    """Download the PNG flag for the given ISO country code."""
    if not country_code:
        return None
    url = f"https://flagcdn.com/w80/{country_code.lower()}.png"
    request = urllib.request.Request(url, headers={"User-Agent": "NetworkStatusGUI/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = response.read()
    except urllib.error.URLError:
        return None

    try:
        return tk.PhotoImage(data=data)
    except tk.TclError:
        return None


class NetworkStatusApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Stan sieci")
        self.geometry("480x360")
        self.resizable(False, False)

        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.flag_image: Optional[tk.PhotoImage] = None

        self._create_widgets()
        self._populate_initial_values()

    def _create_widgets(self) -> None:
        padding = {"padx": 12, "pady": 8}

        header = ttk.Label(self, text="Monitor bezpieczeństwa internetu", font=("Segoe UI", 16, "bold"))
        header.pack(pady=(16, 12))

        self.flag_label = ttk.Label(self)
        self.flag_label.pack()

        self.status_var = tk.StringVar()
        self.latency_var = tk.StringVar()
        self.proxy_var = tk.StringVar()
        self.wifi_var = tk.StringVar()
        self.ip_var = tk.StringVar()
        self.country_var = tk.StringVar()
        self.error_var = tk.StringVar()

        info_frame = ttk.Frame(self)
        info_frame.pack(fill="both", expand=True, **padding)

        self._add_row(info_frame, "Połączenie:", self.status_var)
        self._add_row(info_frame, "Opóźnienie:", self.latency_var)
        self._add_row(info_frame, "Proxy:", self.proxy_var)
        self._add_row(info_frame, "Wi-Fi:", self.wifi_var)
        self._add_row(info_frame, "Adres IP:", self.ip_var)
        self._add_row(info_frame, "Kraj:", self.country_var)

        self.error_label = ttk.Label(info_frame, textvariable=self.error_var, foreground="red")
        self.error_label.pack(anchor="w", pady=(12, 0))

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=(0, 16))

        refresh_btn = ttk.Button(button_frame, text="Odśwież", command=self.refresh_status)
        refresh_btn.pack(side="left", padx=8)

        quit_btn = ttk.Button(button_frame, text="Wyjście", command=self.destroy)
        quit_btn.pack(side="left", padx=8)

    def _add_row(self, parent: ttk.Frame, label: str, variable: tk.StringVar) -> None:
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=4)
        ttk.Label(frame, text=label, width=14, anchor="w").pack(side="left")
        ttk.Label(frame, textvariable=variable, anchor="w").pack(side="left", fill="x", expand=True)

    def _populate_initial_values(self) -> None:
        self.status_var.set("Sprawdzanie...")
        self.latency_var.set("-")
        self.proxy_var.set("-")
        self.wifi_var.set("-")
        self.ip_var.set("-")
        self.country_var.set("-")
        self.error_var.set("")
        self.refresh_status()

    def refresh_status(self) -> None:
        threading.Thread(target=self._update_status, daemon=True).start()

    def _update_status(self) -> None:
        self._set_status("Połączenie", "Sprawdzanie...")
        self.error_var.set("")

        connectivity = check_connectivity()
        if connectivity.is_connected:
            status_text = "Aktywne"
            latency_text = f"{connectivity.latency_ms:.1f} ms" if connectivity.latency_ms else "n/d"
        else:
            status_text = "Nieaktywne"
            latency_text = "-"
            if connectivity.error:
                self.error_var.set(f"Błąd połączenia: {connectivity.error}")

        self.status_var.set(status_text)
        self.latency_var.set(latency_text)

        proxy = get_proxy_info()
        if proxy.http or proxy.https:
            proxy_details = []
            if proxy.http:
                proxy_details.append(f"HTTP: {proxy.http}")
            if proxy.https:
                proxy_details.append(f"HTTPS: {proxy.https}")
            self.proxy_var.set(" | ".join(proxy_details))
        else:
            self.proxy_var.set("brak aktywnych proxy")

        if proxy.no_proxy:
            self.proxy_var.set(self.proxy_var.get() + f" (no_proxy: {proxy.no_proxy})")

        ssid = get_wifi_ssid()
        self.wifi_var.set(ssid or "nie wykryto Wi-Fi")

        ip_info = fetch_public_ip_info()
        if ip_info.error:
            self.ip_var.set("brak danych")
            self.country_var.set("brak danych")
            self.error_var.set((self.error_var.get() + "\n" if self.error_var.get() else "") + f"IP: {ip_info.error}")
            self._update_flag(None)
        else:
            self.ip_var.set(ip_info.ip or "brak danych")
            country_text = ip_info.country_name or "brak danych"
            if ip_info.isp:
                country_text += f" | ISP: {ip_info.isp}"
            self.country_var.set(country_text)
            self._update_flag(ip_info.country_code)

    def _set_status(self, label: str, value: str) -> None:
        if label == "Połączenie":
            self.status_var.set(value)

    def _update_flag(self, country_code: Optional[str]) -> None:
        if not country_code:
            self.flag_label.configure(image="", text="")
            self.flag_image = None
            return

        image = fetch_flag_image(country_code)
        if image:
            self.flag_image = image
            self.flag_label.configure(image=self.flag_image, text=country_code)
        else:
            self.flag_label.configure(image="", text=country_code)
            self.flag_image = None


def main() -> None:
    app = NetworkStatusApp()
    app.mainloop()


if __name__ == "__main__":
    main()
