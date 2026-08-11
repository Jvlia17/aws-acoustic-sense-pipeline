import json
import boto3

glue = boto3.client("glue")


def lambda_handler(event, context):

    print("S3 event received:")
    print(json.dumps(event, indent=2))

    # Get bucket and object key from S3 event
    record = event["Records"][0]

    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]

    print(f"Bucket: {bucket}")
    print(f"Object key: {key}")

    # Start Glue job and pass the input path
    response = glue.start_job_run(
        JobName="acoustic-sense-transform-job",
        Arguments={
            "--INPUT_PATH": f"s3://{bucket}/{key}"
        }
    )

    job_run_id = response["JobRunId"]

    print(f"Started Glue Job Run: {job_run_id}")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Glue job started successfully",
            "input_path": f"s3://{bucket}/{key}",
            "job_run_id": job_run_id
        })
    }