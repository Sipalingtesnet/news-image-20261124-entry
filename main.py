import os
import shutil
import hashlib

def main():
    repo_img = "entry.png"
    if not os.path.exists(repo_img):
        raise FileNotFoundError(f"{repo_img} not found in repo root.")

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    target_path = os.path.join(output_dir, "entry.png")

    # Compute expected sha256 from repo entry.png
    sha_orig = hashlib.sha256()
    with open(repo_img, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            sha_orig.update(chunk)
    orig_sum = sha_orig.hexdigest()

    shutil.copyfile(repo_img, target_path)

    # Verify target sha256 matches
    sha_target = hashlib.sha256()
    with open(target_path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            sha_target.update(chunk)
    target_sum = sha_target.hexdigest()

    if orig_sum != target_sum:
        raise RuntimeError("SHA256 checksum mismatch between repo entry.png and written target!")

    print(f"Successfully wrote entry.png to {target_path}")
    print(f"SHA256: {target_sum}")

if __name__ == "__main__":
    main()
