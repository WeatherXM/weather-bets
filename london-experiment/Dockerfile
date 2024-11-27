FROM python:3.12
ENV GEOJSON_URL="https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/LAC_Dec_2018_Boundaries_EN_BFE_2022/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"
ENV AFTER="2024-10-10"
ENV BEFORE="2024-11-10"
ENV BASIN_NAMESPACE="wxm.proofs"
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
COPY runner.py runner.py
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "runner.py"]