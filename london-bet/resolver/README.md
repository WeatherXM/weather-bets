# London Bet Resolver: Monthly Average Temperature Calculation

## Overview

This is the weather bet leveraging data from the [**WeatherXM Data Index**](https://index.weatherxm.com/). The experiment involves calculating the average temperature for a major city (in this case, London) over a 30-day period. This data will then be used to propose a weather bet, where users can predict whether the actual average temperature falls within a certain range. This experiment serves as a prototype, with potential for more weather-based bets if successful.

The experiment utilizes **Web3 Storage** and **Enriched Weather Data** to perform these calculations, with strict verification protocols based on public keys, Proof-of-Location (PoL), and Quality-of-Data (QoD) scores.

---

## Functional Requirements

### 1. **Data Acquisition**
   - Use the dataset from the **WeatherXM Web3 Storage** called **Enriched Weather Data** to calculate the average temperature for an area (e.g., London) over a 30-day period.

### 2. **Device Filtering**
   - **Active Device List Creation**: Calculate the active devices that should be considered based on:
     - **Quality-of-Data (QoD) >= 0.8**.
     - **Proof-of-Location (PoL) = 1**.
   - The filtered list ensures only the most accurate and trustworthy weather data is used.

### 3. **Computation and Publication**
   - Develop a script or algorithm that computes the **average temperature** for the London area over the last 30 days.
   - Store this script in a GitHub repository, ensuring it can fetch, filter, and compute data based on predefined criteria.
   - Optionally research using **Bacalhau** to automate the temperature computation for a period of 30 days.

### 4. **Result Integration and Bet Resolution**
   - Integrate the calculated average temperature with the **UMA Oracle**, which will act as the final arbiter for the weather bet.
   - Publish the calculated result to resolve the bet.

---

## Experiment Scope

This project can be divided into the following steps:

1. **Dataset Creation**
   - Generate a dataset containing the necessary fields to verify weather station data based on public keys. 
   - The fields include: 
     - `public_key`: to verify the authenticity of the device's data.
     - `ws_packet_b64` and `ws_packet_sig`: signed data packets from the weather stations.
   - These fields ensure that the data comes from valid, secure devices and is tamper-proof.

2. **Data Publication**
   - Publish the enriched weather data, including the calculated QoD, PoL, and RM scores to **Tableland**. This publication will form the basis of the experiment and future verifications.

3. **Average Temperature Calculation**
   - Write a script to calculate the average temperature for the last 30 days using the enriched weather data. This calculation should only include data from devices that pass the filter based on:
     - **Geolocation** (London region).
     - **QoD > 0.8** and **PoL = 1**.
     - **Verification of data authenticity** using the public keys and signatures from the weather devices.

4. **Verification and Result Publication**
   - Ensure that all data can be verified using the device’s public key and is signed with the corresponding private key.
   - Integrate with a betting platform, using a decentralized and verifiable solution such as the UMA Oracle to publish the final result.

---
## Key Terms

### Proof-of-Location (PoL)
PoL is an algorithm that evaluates the location data of a weather station. It ensures that the weather station is accurately placed in its registered location. If a weather station is relocated, its PoL score drops to 0, and its standing in the network is reset.

### Quality-of-Data (QoD)
QoD is an algorithm that assesses the quality of weather data provided by a weather station. It evaluates various metrics such as accuracy and consistency, generating a score that reflects confidence in the data. Weather stations must maintain a high QoD score to be considered reliable for inclusion in this experiment.

---

## Data Source and Geo Filtering

For this experiment, weather devices will be filtered based on their geolocation in the **London area**. The geolocation filtering is performed using **H3 hexagons at resolution 7**, which divide the Earth into hexagonal cells that allow for efficient spatial indexing. 

### H3 Hexagons
H3 is a geospatial indexing system that subdivides the Earth's surface into hexagonal cells, offering several advantages for geographic analysis, including uniformity and flexibility in terms of precision. For this experiment, **resolution 7** is used, which corresponds to hexagons with an approximate edge length of **1.22 km**. This level of granularity is well-suited for filtering weather stations within city boundaries like London.

The weather stations' geolocation is mapped into their corresponding H3 hexagons. Any weather station whose coordinates fall within a hexagon covering the London area (defined by its administrative boundaries) is included in the dataset.

<img src="./geojson/london-h3-plot.png" alt="H3 London Map" width="500" height="500">


### Data Source for London Boundaries
In addition to H3-based filtering, administrative boundaries from the [**UK Open Geography Portal**](https://geoportal.statistics.gov.uk/) are used for validation. This resource provides downloadable datasets, including **GeoJSON files** for [**London area**](https://geoportal.statistics.gov.uk/datasets/d1dd6053dc7f4b14987e093b30a64435_0/explore?location=51.533145%2C0.201410%2C10.45). These files are based on official data from the Ordnance Survey and Office for National Statistics, and they offer detailed administrative boundaries such as boroughs and wards.

You can explore and download the relevant GeoJSON files from the UK Open Geography Portal [here](https://geoportal.statistics.gov.uk/).

By combining H3 hexagons and official administrative boundaries, the geo-filtering process ensures that only relevant weather station data from the London area is used in this experiment.

### Implementation

The boundary coords for the London area using an official [GeoJson](https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAC_Dec_2018_Boundaries_EN_BFE_2022/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson) can be dynamically by invoking the following command and the results will be stored in *geojson* folder:

`python3 location/london_bd_creation.py`

---

## Conclusion

This experiment aims to bring reliable and secure weather data into a novel betting scenario. By ensuring that the data is accurate, verifiable, and enriched with meaningful metrics like PoL and QoD, we can build confidence in the results and potentially scale the experiment for additional cities or datasets in the future.

The final result of the temperature calculation will be used to resolve the bet via a decentralized solution such as the **UMA Oracle**, providing a fully transparent process from data acquisition to bet resolution.

---

## How to Run

1. Clone the repository.
2. Ensure all dependencies are installed:
```
python3 -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
```
3. Run the script to calculate the average temperature using verifiable weather station data:
`python3 main.py`
4. The output will display the average temperature for the last 30 days, which can then be used to resolve the bet.

For more details on the implementation, please refer to the individual sections within the repository.

---

## Next Steps

To build on the success of this experiment, future efforts may include the following:

- **Decentralized Data Pipelines**: Implement a system that continuously ingests and processes weather data using decentralized, distributed pipelines. This approach will ensure data integrity and eliminate central points of failure.

- **Trustless Computation**: Leverage a decentralized computation framework to perform temperature calculations across multiple nodes. This guarantees that the results are produced transparently and can be verified by any party.

- **Verifiable Compute Network**: Introduce a verifiable compute layer where multiple nodes process and validate the results independently. This will add an additional layer of trust and decentralization, ensuring that the computed results are reliable and unbiased.

- **Scalability**: Enable the experiment to scale beyond a single city by incorporating distributed data processing and computation, paving the way for real-time bets and support for a larger number of participants and datasets.

---

By incorporating these advancements, the experiment can evolve to be more secure, transparent, and scalable, enabling future predictions and bet scenarios across a global network.


---

### License

This project is licensed under the MIT License.