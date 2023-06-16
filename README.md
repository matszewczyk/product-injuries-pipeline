


MinIO

mkdir -p /mnt/data/compose

nano /etc/default/minio


data grabbed from:

https://data.world/awram/us-product-related-injuries

https://public.opendatasoft.com/explore/dataset/us-national-electronic-injury-surveillance-system-neiss-product-codes/export/?refine.code=0102


prefect deployment build -n "ACI Test Flow" -sb azure/blob-storage-flows -ib azure-container-instance-job/aci-job my_flows.py:healthcheck -q default -a