from pathlib import Path
import zipfile
from CONSTANTS import final_dataset_dirpath
# Specify the directory containing the zip files


def rmdir_recursive(dir_path: Path):
    for item in dir_path.iterdir():
        if item.is_dir():
            rmdir_recursive(item)
        else:
            item.unlink()
    dir_path.rmdir()

for root_dir in Path(final_dataset_dirpath).iterdir():
    if root_dir.is_dir():
        # Loop through all the .zip files in the directory
        for zip_file in root_dir.glob("*.zip"):
            # Use the zipfile module to open the zip file
            with zipfile.ZipFile(zip_file, 'r') as z:
                # Construct the path to gene.fna inside the zip file
                fna_path_in_zip = f"ncbi_dataset/data/gene.fna"
                # Check if gene.fna exists inside the zip file
                if fna_path_in_zip in z.namelist():
                    # Extract gene.fna to the directory
                    z.extract(fna_path_in_zip, root_dir)
                    # The path of the extracted gene.fna in the filesystem
                    extracted_path = root_dir / fna_path_in_zip
                    # New name for the gene.fna file
                    new_name = zip_file.stem + ".fna"
                    # Rename the extracted file
                    extracted_path.rename(root_dir / new_name)
                    # Delete the ncbi_dataset directory after extracting and renaming
                    rmdir_recursive(root_dir / "ncbi_dataset")
            zip_file.unlink()
