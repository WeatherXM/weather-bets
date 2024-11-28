FROM python:3.12
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    && apt-get clean

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV GEOJSON_URL="https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAC_Dec_2018_Boundaries_EN_BFE_2022/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"
ENV BASIN_NAMESPACE="wxm.data_proofs"
ENV IPFS_GATEWAY_URL="https://ipfs.io/ipfs"
ENV BASIN_API_BASE_URL="https://basin.tableland.xyz/vaults"
WORKDIR /app
ENV PYTHONPATH=/app
COPY data data
COPY decision decision
COPY weather weather
COPY geojson geojson
COPY location location
COPY requirements.txt requirements.txt
COPY .env .env
COPY runner.py runner.py
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "runner.py"]