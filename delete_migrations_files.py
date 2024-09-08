import os


def delete_migration_files(app_folder):
    for root, dirs, files in os.walk(app_folder):
        if 'migrations' in root.split(os.sep):
            for file in files:
                if file != '__init__.py':
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")
                    except Exception as e:
                        print(f"Error deleting {file_path}: {e}")


if __name__ == "__main__":
    app_folder = 'apps'  # Replace with the path to your app folder
    delete_migration_files(app_folder)
