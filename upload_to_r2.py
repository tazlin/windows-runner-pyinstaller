import argparse
import boto3
import pathlib
import zipfile


def upload_windows_dist_folder_to_s3(
    *, bucket_name: str, dist_folder: str, target_folder: str = "default"
):
    s3 = boto3.client("s3")
    dist_folder_path = pathlib.Path(dist_folder)

    if not dist_folder_path.exists():
        raise FileNotFoundError(f"{dist_folder} does not exist")

    if not dist_folder_path.is_dir():
        raise NotADirectoryError(f"{dist_folder} is not a directory")

    # Create a zip file out of dist_folder
    zip_file_name = dist_folder_path.name + ".zip"
    with zipfile.ZipFile(zip_file_name, "w") as zipf:
        for file in dist_folder_path.rglob("*"):
            zipf.write(file, file.relative_to(dist_folder_path))

    # Upload the zip file to S3
    target_folder = target_folder.strip("/")
    if target_folder == "default":
        target_folder = dist_folder_path.name

    s3.upload_file(
        zip_file_name,
        bucket_name,
        f"{target_folder}/{zip_file_name}",
    )
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket_name", type=str, required=True)
    parser.add_argument("--dist_folder", type=str, required=True)
    parser.add_argument("--target_folder", type=str, default="default")

    args = parser.parse_args()

    upload_windows_dist_folder_to_s3(
        bucket_name=args.bucket_name,
        dist_folder=args.dist_folder,
        target_folder=args.target_folder,
    )
