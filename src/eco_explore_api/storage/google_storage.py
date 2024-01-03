import os
from fastapi_gcs import FGCSUpload as Fupload
from eco_explore_api.config import GOOGLE_STORAGE
from fastapi import UploadFile
from eco_explore_api.config import GOOGLE_PROJECT, BUCKET_NAME


class gstorage:
    def __init__(self):
        self.project_id = GOOGLE_PROJECT
        self.bucket_name = BUCKET_NAME
        self.file_path = "eco_explore"

    def upload_single_file(self, file: UploadFile):
        try:
            response = Fupload.file(
                project_id=self.project_id,
                bucket_name=self.bucket_name,
                file=file,
                file_path=self.file_path,
                maximum_size=2_097_152,
                allowed_extension=["png", "jpeg", "jpg"],
                file_name=file.filename,
                is_public=True,
            )
            # response["file_path"] = (
            #     "https://storage.googleapis.com/" + response["file_path"]
            # )
            return response
        except Exception as e:
            raise e

    # def upload_files(self, files: )
    # def upload_file(self, file: UploadFile):
    #     bucket = self.storage_client.get_bucket(self.bucket_name)
    #     file_path = "eco_explore/" + file.name
    #     blob = bucket.blob(file_path)
    #     blob.upload_file(file.file, content_type="image/jpeg")
    #     return "https://storage.cloud.google.com/{}/{}".format(
    #         self.bucket_name, file_path
    #     )
