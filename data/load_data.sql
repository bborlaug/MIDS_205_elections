\cd /data/MIDS_205_elections/data
COPY data.results FROM 'election_results.csv' CSV HEADER;
COPY data.google FROM 'google_traffic.csv' CSV HEADER;
