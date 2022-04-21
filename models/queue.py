from dataclasses import dataclass,field
import pandas as pd
import numpy as np

@dataclass
class Queue:
    arrival_rate: float
    service_rate: float
    simulations: int
    capacity: int = 0  # Unlimited capacity by default
    system: pd.DataFrame = field(init=False)

    def __post_init__(self):
        M = self.simulations
        self.system = pd.DataFrame(dict({
            'arrival_headway': np.zeros(M),
            'arrival_time': np.zeros(M),
            'service_time': np.zeros(M),
            'departure_time': np.zeros(M),
            'waiting_time': np.zeros(M),
            'time_in_system': np.zeros(M)
        }))

    def simulate(self):

        M = self.simulations
        sim1 = np.random.random(M)
        sim2 = np.random.random(M)  

        for j in range(M):
            
            if j == 0:
                self.system['arrival_headway'].iloc[j] = 0
                self.system['arrival_time'].iloc[j] = 0
                self.system['service_time'].iloc[j] = -np.log(sim2[j])/self.service_rate
                self.system['departure_time'].iloc[j] = self.system['service_time'].iloc[j]

            else:
                self.system['arrival_headway'].iloc[j] = -np.log(sim1[j])/self.arrival_rate
                self.system['arrival_time'].iloc[j] = self.system['arrival_time'].iloc[j-1] + self.system['arrival_headway'].iloc[j]
                self.system['service_time'].iloc[j] = -np.log(sim2[j])/self.service_rate
                self.system['departure_time'].iloc[j] = self.system['service_time'].iloc[j] + max(self.system['arrival_time'].iloc[j], self.system['departure_time'].iloc[j-1-self.capacity])

        self.system['waiting_time'] = self.system['departure_time'] - (self.system['arrival_time'] + self.system['service_time'])
        self.system['time_in_system'] = self.system['departure_time'] - self.system['arrival_time']

        return self.system


    def values(self):

        M = self.simulations
        T = (self.system['departure_time'] - self.system['arrival_time']).sum()/M
        print(f"Expected time in the system by user = {T} minutes")
        Tq = (self.system['departure_time'] - self.system['arrival_time'] - self.system['service_time']).sum()/M
        print(f"Expected time in queuing system by user = {Tq} minutes")
        N = (self.system['departure_time'] - self.system['arrival_time']).sum()/self.system['departure_time'].max()
        print(f"Expected number of users in queing system = {N}")
        Nq = (self.system['departure_time'] - self.system['arrival_time'] - self.system['service_time']).sum()/self.system['departure_time'].max()
        print(f"Expected number of users in queue = {Nq}")


