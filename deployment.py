from os import environ, path
import sys

#Prefect 2
from prefect.deployments import Deployment

from prefect_azure.container_instance import AzureContainerInstanceJob
from prefect.filesystems import Azure

#Replace with your block name
azure_container_instance_job_block = AzureContainerInstanceJob.load("aci-job")
az_block = Azure.load("blob-storage-flows")

#Without a storage block for remote storage, the PATH of the flow, and the ENTRYPOINT are required to locate the flow in docker.
#The flow is at /opt/prefect/flows/flow.py from step 4 when we built the image

deployment = Deployment(
    name="InstanceJobACI",
    version="latest",
    flow_name="healthcheck",
    work_queue_name="default",
    infrastructure=azure_container_instance_job_block,
    storage=az_block,
    # path="/opt/prefect/flows",
    entrypoint="my_flows.py:healthcheck"
)
deployment.apply()