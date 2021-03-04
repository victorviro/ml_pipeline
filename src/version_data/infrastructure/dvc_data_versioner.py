import logging
import subprocess

from src.utils.files import get_json_from_file_path


logger = logging.getLogger(__name__)


class DVCDataVersioner():
    def __init__(self, relative_data_path: str, data_name: str, data_version: float,
                 git_remote_name: str, git_branch_name: str):
        self.relative_data_path = relative_data_path  # 'data/01_raw'
        self.data_name = data_name
        self.relative_full_data_path = f'{relative_data_path}/{data_name}.json'
        self.data_version = data_version
        self.git_remote_name = git_remote_name  # origin
        self.git_branch_name = git_branch_name  # master

    def version_data(self):

        # Track the data in DVC repository
        try:
            subprocess.run(["dvc", "add", self.relative_full_data_path])
        except Exception as err:
            message = ('Error trying to track the data in the DVC repository.\nTraceback'
                       f' of error: {str(err)}')
            logger.error(message)
            raise Exception(message)
        # TODO check when dataset has not changed

        # Add and commit the DVC metadata of the data to the git repository
        relative_full_metadata_path = f'{self.relative_full_data_path}.dvc'
        commit_message = f'Added max_char_per_line raw data, version: {self.data_version}'
        try:
            subprocess.run(["git", "add", relative_full_metadata_path])
            subprocess.run(["git", "add", f'{self.relative_data_path}/.gitignore'])
            subprocess.run(["git", "commit", "-m", commit_message])
        except Exception as err:
            message = ('Error trying to track and commit the metadata (dvc) in the git '
                       f'repository.\nTraceback of error: {str(err)}')
            logger.error(message)
            raise Exception(message)

        # Push the DVC metadata of the data to the git repository
        try:
            subprocess.run(["git", "push", self.git_remote_name, self.git_branch_name])
        except Exception as err:
            message = ('Error trying to push the metadata (dvc) in the git repository.'
                       f'\nTraceback of error: {str(err)}')
            logger.error(message)
            raise Exception(message)

        # TODO add command to push data versioned in dvc storage (`push dvc`)
        #  see documentation dvc
