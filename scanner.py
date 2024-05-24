import os
class FileSystemScanner:
    """
    This class is used to parse the folder with Python projects and extract all paths to Python files.

    :param folder_path: The path to a folder containing Python projects.
    Each project should be in a separate sub-folder.
    The default value is "./Python_Projects".
    """

    folder_path = None

    def __init__(self, folder_path=".."):
        """
        Initialize the parser.

        :param folder_path: The path to a folder containing Python projects.
        Each project should be in a separate sub-folder.
        The default value is "./PycharmProjects".

        """
        self.folder_path = folder_path

    def parse(self):
        """
        Parse the folder with Python projects and extract all paths to Python files.
        :return: List of paths to Python files.
        :raises Exception: If the folder does not exist or no Python files are found.
        """
        # handle the case when the folder does not exist
        if not os.path.exists(self.folder_path):
            exception_message = "The folder " + self.folder_path + " does not exist."
            raise Exception(exception_message)

        projects = self._parse_folder()

        for folder_name in projects:
            project = projects[folder_name]

            python_files = []

            for root, dirs, files in os.walk(project["path"]):
                for file in files:
                    if file.endswith(".py"):
                        python_files.append(os.path.join(root, file))

            projects[folder_name]["files"] = python_files

        return projects

    def _parse_folder(self):
        """
        Parse a folder with Python projects and extracts all project names.
        :return: A dictionary with project names as keys and a dictionary as values:

        - "path" - the path to the project folder
        - "files" - a list of paths to Python files in the project
        """

        folder_path = self.folder_path

        # handle the case when the folder does not exist
        if not os.path.exists(folder_path):
            exception_message = "The folder " + folder_path + " does not exist."
            raise Exception(exception_message)

        items_in_dir = os.listdir(folder_path)
        # filter out non-folders
        folder_names = [item for item in items_in_dir if os.path.isdir(os.path.join(folder_path, item))]

        if len(folder_names) == 0:
            exception_message = "No Python projects found in the folder " + folder_path + "."
            raise Exception(exception_message)

        print("Found " + str(len(folder_names)) + " Python project(s):")
        print("\n".join(folder_names))
        print("\n")
        
        projects = {}
        for folder_name in folder_names:
            project_path = os.path.join(folder_path, folder_name)
            projects[folder_name] = {"path": project_path, "files": []}
        return projects

