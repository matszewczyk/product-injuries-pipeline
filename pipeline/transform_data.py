from prefect import task

@task
def prepare_db():
    pass

@task
def read_from_minio():
    # MINIO_CLIENT.get_object("injuries", "injuries")
    pass

    
