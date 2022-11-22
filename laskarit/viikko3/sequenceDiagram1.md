``` mermaid
sequenceDiagram
main ->> Machine: Machine()
activate Machine
Machine->>FuelTank: FuelTank()
Machine ->> FuelTank: fill(40)
Machine ->> Engine: Engine(tank)
deactivate Machine
main ->> Machine: drive()
activate Machine
Machine->> Engine: start()
activate Engine
Engine ->> FuelTank: consume(5)
deactivate Engine
Machine->> Engine: is_running()
activate Engine
Engine -->> Machine: True
deactivate Engine
Machine ->> Engine: use_energy()
deactivate Machine
activate Engine
Engine ->> FuelTank: consume(10)
deactivate Engine
```
