# Network Status GUI

Prosta aplikacja w Pythonie/Tkinter, która pokazuje podstawowe informacje o stanie połączenia internetowego w formie przyjaznego pulpitu.

## Funkcje

- **Status połączenia** – test z wykorzystaniem połączenia TCP do serwera DNS i pomiar opóźnienia.
- **Proxy** – odczyt zmiennych środowiskowych `http_proxy`, `https_proxy` i `no_proxy`.
- **Sieć Wi-Fi** – próba wykrycia aktualnego SSID (obsługiwane narzędzia: `nmcli`, `iwgetid`, `netsh`).
- **Adres publiczny i kraj** – zapytanie do `ipapi.co` z informacją o państwie i dostawcy (ISP) wraz z pobraniem flagi kraju.
- **Ręczne odświeżanie** – przycisk do ponownego sprawdzenia stanu sieci.

Wszystkie operacje wykonywane są w osobnym wątku, dzięki czemu GUI pozostaje responsywne.

## Wymagania

- Python 3.9+
- Dostępny moduł Tkinter (standardowo w pakiecie instalacyjnym Pythona).
- Dostęp do internetu (dla pobrania danych o IP i flagi). Aplikacja działa również w trybie offline, ale część informacji może być niedostępna.

## Uruchomienie

```bash
python3 network_status_gui.py
```

## Uwagi

- W systemach, gdzie polecenia `nmcli`/`iwgetid` nie są dostępne, wykrywanie Wi-Fi może zwrócić komunikat „nie wykryto Wi-Fi”.
- Pobieranie flag odbywa się z serwisu [flagcdn.com](https://flagcdn.com); w przypadku braku dostępu internetowego flaga nie zostanie wyświetlona.
