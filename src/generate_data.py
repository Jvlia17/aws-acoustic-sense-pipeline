import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_sensor_data(rows=10000):

    np.random.seed(42)

    data = {
        "sensor_id": np.random.randint(1, 20, rows),

        "timestamp": [
            datetime.now() + timedelta(seconds=i)
            for i in range(rows)
        ],

        "x": np.random.uniform(0, 100, rows),
        "y": np.random.uniform(-1, 1, rows),
        "z": np.random.uniform(-1, 1, rows),

        "frequency": np.random.uniform(
            1e6,
            5e6,
            rows
        ),

        "temperature": np.random.normal(
            25,
            2,
            rows
        )
    }


    df = pd.DataFrame(data)


    # normal signal
    df["amplitude"] = np.random.normal(
        0.1,
        0.02,
        rows
    )


    # add defects
    defects = np.random.choice(
        rows,
        size=100,
        replace=False
    )


    df.loc[
        defects,
        "amplitude"
    ] = np.random.uniform(
        0.7,
        1.0,
        100
    )


    return df



if __name__ == "__main__":

    df = generate_sensor_data()

    df.to_csv(
        "data/raw/sensor_measurements.csv",
        index=False
    )

    print(df.head())
    print(df.shape)