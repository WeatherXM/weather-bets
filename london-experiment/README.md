# PoC Oracle Service for London Monthly Average Temperature

##### Table of Contents  
- [Overview](#overview)
- [Functional Requirements](#functional-requirements)  
- [Experiment Scope](#experiment-scope)
- [Key Terms](#key-terms)
- [In-Depth Analysis](#in-depth-analysis)
   - [Data Sources](#data-source-for-london-boundaries)
   - [Data Verification](#data-verification)
- [Usage](#usage)
- [Example](#example)
- [Next Steps](#next-steps)
- [License](#license)
- [Technologies](#technologies)

## Overview

This is a PoC for the first weather oracle service leveraging data from the [**WeatherXM Data Index**](https://index.weatherxm.com/). The experiment involves calculating the average temperature for a major city (in this case, London) over a 30-day period. This result can potentially be used to resolve a weather bet, where users can predict whether the actual average temperature falls within a certain range or not. This experiment serves as a prototype.

---

## Functional Requirements

### 1. **Data Acquisition**
   - Use the dataset from the **WeatherXM Web3 Storage** called **Proofs** to calculate the average temperature for an area (e.g., London) over a 30-day period.

### 2. **Device Filtering**
   - **Active Device List Creation**: Calculate the active devices that should be considered based on:
     - **Quality-of-Data (QoD) >= 0.8**.
     - **Proof-of-Location (PoL) > 0**.
   - The filtered list ensures only the most accurate and trustworthy weather data is used.

### 3. **Computation and Publication**
   - Develop the algorithm that computes the **average temperature** for the London area over the last 30 days.
   - Fetch, filter, and compute data based on a set of predefined criteria.
   - Calculate the final average temperature.

---

## Experiment Scope

This project can be divided into the following steps:

1. **Dataset Creation**
   - Generate a dataset containing the necessary fields to verify weather station data based on public keys. 
   - The fields include: 
     - `public_key_PEM`: to verify the authenticity of the device's data.
     - `ws_packet_b64` and `ws_packet_sig`: signed data packets from the weather stations.
   - These fields ensure that the data comes from valid, secure devices and is tamper-proof.

2. **Dataloading**
   - Publish the proofs dataset, including the calculated Quality-of-Data, Proof-of-Location and Reward scores to **Tableland**. This publication will form the basis of the experiment and future verifications.

3. **Filtering**
   - Write a script to calculate the average temperature for the last 30 days using the proofs dataset. This calculation should exclusively include data from devices that meet the required criteria:
     - **Geolocation** (London region).
     - **QoD > 0.8** and **PoL > 0**.
     - **Verification of data authenticity** using the public keys, signatures and base64 encoded data packets from the weather devices.

4. **Verification**
   - Ensure that all data can be verified using the device’s public key and is signed with the corresponding private key.

---
## Key Terms

### Proof-of-Location (PoL)
PoL is an algorithm that evaluates the location data of a weather station. It ensures that the weather station is accurately placed in its registered location. If a weather station is relocated, its PoL score drops to 0, and its standing in the network is reset.

### Quality-of-Data (QoD)
QoD is an algorithm that assesses the quality of weather data provided by a weather station. It evaluates various metrics such as accuracy and consistency, generating a score that reflects confidence in the data. Weather stations must maintain a high QoD score to be considered reliable for inclusion in this experiment.

### H3 Hexagons
H3 is a geospatial indexing system that subdivides the Earth's surface into hexagonal cells, offering several advantages for geographic analysis, including uniformity and flexibility in terms of precision. For this experiment, **resolution 7** is used, which corresponds to hexagons with an approximate edge length of **1.22 km**. This level of granularity is well-suited for filtering weather stations within city boundaries like London.

The weather stations' geolocation is mapped into their corresponding H3 hexagons. Any weather station whose coordinates fall within a hexagon covering the London area (defined by its administrative boundaries) is included in the dataset.

---

## In-Depth Analysis

For this experiment, weather devices will be filtered based on their geolocation in the **London area**. The geolocation filtering is performed using **H3 hexagons at resolution 7**, which divide the Earth into hexagonal cells that allow for efficient spatial indexing. 

<img src="https://github.com/WeatherXM/weather-bets/blob/main/london-bet/resolver/geojson/london_h3_plot.png?raw=true" alt="H3 London Map" width="500" height="500">

### Data Source for London Boundaries
In addition to H3-based filtering, administrative boundaries from the [**UK Open Geography Portal**](https://geoportal.statistics.gov.uk/) are used for validation. This resource provides downloadable datasets, including **GeoJSON files** for the [**London area**](https://geoportal.statistics.gov.uk/datasets/d1dd6053dc7f4b14987e093b30a64435_0/explore?location=51.533145%2C0.201410%2C10.45). These files are based on official data from the Ordnance Survey and Office for National Statistics, and they offer detailed administrative boundaries such as boroughs and wards.

You can explore and download the relevant GeoJSON files from the UK Open Geography Portal [here](https://geoportal.statistics.gov.uk/).

By combining H3 hexagons and official administrative boundaries, the geo-filtering process ensures that only relevant weather station data from the London area is used in this experiment.

#### Generate the Boundary Coordinates for the London Area Polygon

The boundary coords for the London area using an official [GeoJson](https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAC_Dec_2018_Boundaries_EN_BFE_2022/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson) can be dynamically by invoking the following command and the results will be stored in *geojson* folder:

`python3 location/london_bd_creation.py`

---

### Data Source for Weather Data

The datasource for this expirement are **WeatherXM's** raw data which are stored in IPFS through the **Basin** with all the necessary information, *public keys, packet signature, etc* to verify their authenticity. These datasets are in **Parquet** format and can be overviewed through the category **Proofs** in the [**WeatherXM Data Index**](https://index.weatherxm.com/).

### Data Verification

Weather stations employ a secure mechanism to ensure the authenticity and integrity of the data they transmit. Each station is equipped with a secure element, a specialized hardware component responsible for cryptographic operations. This secure element plays a critical role in generating digital signatures that make the transmitted data tamperproof and verifiable.

Here’s how the process works:

#### Packet Signing: 
Weather stations generate data packets on a daily basis. To conserve resources, certain models are configured to send signed packets periodically, for example, every X packets. The secure element creates a digital signature using its private key. This private key is securely stored within the secure element, making it inaccessible to anyone including WeatherXM's team.

#### Verification Process: 
On the receiving side, the authenticity of a packet is verified using the raw data, the corresponding public key of the device, and the generated signature. The public key is associated with the specific device and is used to confirm that the packet was genuinely signed by the station’s private key.

#### Tamperproof Data: 
Because the signature is uniquely tied to both the raw data and the private key, any attempt to alter the packet's content would render the signature invalid. This guarantees that the data received by the other side has not been tampered with and originates from the intended device.

#### Data Inclusion for Weather Bets: 
For applications such as weather bets, only verified data—packets that successfully pass the signature validation process—are considered. This ensures fairness and accuracy by excluding potentially corrupted or unauthenticated information.

The use of secure elements and cryptographic signing ensures that the data transmitted by weather stations is both reliable and tamperproof, reinforcing trust in systems that rely on this information.

---

## Usage
1. Clone the repository.

2. Run the experiment:
` docker-compose up`

## Development

1. Clone the repository.
2. Ensure versions for Python and pip are the following:
```
Python 3.12.7 
pip 24.2
```
3. Ensure all dependencies are installed:
```
python3 -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
```
4. There are 2 ways to run the program that resolves the bet for only-one **.parquet** file:
   - With chunks enabled using low memory:
   `python3 main.py -f data.parquet -lm true`
   - Without chunks requiring over 16G RAM and 30G Swap:
   `python3 main.py -f data.parquet`

5. Run the **runner.py** in order to get the result for the time period defined using the env variables *AFTER, BEFORE*:
   `python3 runner.py`
   The runner is always in low-memory mode in order to get the result with the minimum impact on the host.

## Example

After executing the runner, the necessary files will be retrieved from **Basin**, proper geo location and weather filtering will take place and then the data verifiaction will be evaluated before calculting the average temperature. 

The following is the output when evaluating a **.parquet** file without chunks:

```
LOADING WITHOUT CHUNKS
GEO VERIFIED DEVICES COUNT: 34
GEO LOCATION VERIFICATION IS COMPLETED
WEATHER VERIFIED DEVICES COUNT WITH QOD>=0.8 AND POL>0: 13
WEATHER DATA FILTERING IS COMPLETED
VERIFIED DEVICES ['Tricky Brunette Tornado' 'Magic Opaque Fog' 'Dizzy Champagne Sun'
 'Brave Veronica Drought' 'Sweet Raspberry Earth'
 'Delightful Taupe Troposphere' 'Eager Bole Haze' 'Great Peach Cloud'
 'Delightful Nylon Air']
DATA VERIFICATION IS COMPLETED
DATA VERIFIED DEVICES COUNT: 9
LONDON DEVICES FROM DATAFRAME PARTICIPATING IN RESOLUTION AFTER FILTERING: 26%
AVG TEMP: 9.49 Celsius
```

The daily average temperature is the output in the end `AVG TEMP: 9.49 Celsius`

The following is the output when executing the **runner.py** for a period of time:

```
GEO LOCATION VERIFICATION IS COMPLETED
WEATHER VERIFIED DEVICES COUNT WITH QOD>=0.8 AND POL>0: 1
WEATHER DATA FILTERING IS COMPLETED
DATA VERIFICATION IS COMPLETED
DATA VERIFIED DEVICES COUNT: 1
LONDON DEVICES FROM DATAFRAME PARTICIPATING IN BET RESOLUTION AFTER FILTERING: 100%
Processed chunk 29: 5035 rows
GEO VERIFIED DEVICES COUNT: 1
GEO LOCATION VERIFICATION IS COMPLETED
WEATHER VERIFIED DEVICES COUNT WITH QOD>=0.8 AND POL>0: 0
WEATHER DATA FILTERING IS COMPLETED
DATA VERIFICATION IS COMPLETED
DATA VERIFIED DEVICES COUNT: 0
LONDON DEVICES FROM DATAFRAME PARTICIPATING IN BET RESOLUTION AFTER FILTERING: 0%
CHUNK 30 WAS FILTERED OUT (NO ROWS MEET THE FILTERING CRITERIA)
GEO VERIFIED DEVICES COUNT: 2
GEO LOCATION VERIFICATION IS COMPLETED
WEATHER VERIFIED DEVICES COUNT WITH QOD>=0.8 AND POL>0: 1
WEATHER DATA FILTERING IS COMPLETED
DATA VERIFICATION IS COMPLETED
DATA VERIFIED DEVICES COUNT: 1
LONDON DEVICES FROM DATAFRAME PARTICIPATING IN BET RESOLUTION AFTER FILTERING: 50%
Processed chunk 31: 5033 rows
FINAL DATAFRAME SHAPE: (113961, 11)
PROCESSED 32 CHUNKS FOR FILE downloads/bafybeihogsuzu5of6lzrafdfzb6ie2jtd2hozvqofvregevknidk2gr7hi.parquet
AVG TEMP: 8.3 Celsius

```
After running the filtering in chunks for all **.parquet** files, the average temperature is calculated for the chosen time using the env variables *AFTER and BEFORE*. The output in the end `AVG TEMP: 9.3 Celsius` indicates the average temperature for this time period.

---

## Next Steps

To build on the success of this experiment, future efforts may include the following:
- **30 Days Resolver**: Run the above script for over 30 days, and then find the average temperature for the last 30 days.
- **Decentralized Data Pipelines**: Implement a system that continuously ingests and processes weather data using decentralized, distributed pipelines. This approach will ensure data integrity and eliminate central points of failure.

- **Trustless Computation**: Leverage a decentralized computation framework to perform temperature calculations across multiple nodes. This guarantees that the results are produced transparently and can be verified by any party.

- **Verifiable Compute Network**: Introduce a verifiable compute layer where multiple nodes process and validate the results independently. This will add an additional layer of trust and decentralization, ensuring that the computed results are reliable and unbiased.

- **Scalability**: Enable the experiment to scale beyond a single city by incorporating distributed data processing and computation, paving the way for real-time bets and support for a larger number of participants and datasets.

---

By incorporating these advancements, the experiment can evolve to be more secure, transparent, and scalable, enabling future predictions and bet scenarios across a global network.


---

## License

This project is licensed under the MIT License.

## Technologies

* [Tableland](https://docs.tableland.xyz/)
* [H3](https://h3geo.org/docs)
* [OSMnx](https://osmnx.readthedocs.io/en/stable/)
* [GeoPandas](https://geopandas.org/en/stable/)
* [Pandas](https://pandas.pydata.org/)
* [NumPy](https://numpy.org/)
* [Matplotlib](https://matplotlib.org/)

