```mermaid
classDiagram
Monopoli "1" -- "1" Pelilauta
Pelilauta "1" -- "40" Ruutu
Ruutu "1" -- Ruutu
Ruutu "1" -- "1-8" Pelinappula
Monopoli "1" -- "2" Noppa
Monopoli "1" -- "2..8" Pelaaja
Pelaaja "1" -- "1" Pelinappula
```
