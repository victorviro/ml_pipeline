import logging
import subprocess
import os

from src.version_data.domain.data_versioner import IDataVersioner


logger = logging.getLogger(__name__)


class DVCDataVersioner(IDataVersioner):
    """
    A class which implements the interface IDataVersioner to version the dataset.
    It versions the dataset using DVC.
    """

    def version_data(self, relative_data_file_path: str, data_version: float,
                     git_remote_name: str, git_branch_name: str):
        """
        Version the dataset using DVC.

        :param relative_data_file_path: Relative path of the data file stored
        :type relative_data_file_path: str
        :param data_version: Version of the data
        :type data_version: float
        :param git_remote_name: Name of the remote to the git repository
        :type git_remote_name: str
        :param git_branch_name: Name of the branch of the git repository
        :type git_branch_name: str
        """

        # Track the data in DVC repository
        try:
            subprocess.run(["dvc", "add", relative_data_file_path])
        except Exception as err:
            message = ('Error trying to track the data in the DVC repository.\nTraceback'
                       f' of error: {str(err)}')
            logger.error(message)
            raise Exception(message)
        # TODO check when dataset has not changed

        # Add and commit the DVC metadata of the data to the git repository
        relative_metadata_file_path = f'{relative_data_file_path}.dvc'
        relative_data_path = os.path.dirname(relative_data_file_path)
        commit_message = f'Added max_char_per_line raw data, version: {data_version}'
        try:
            subprocess.run(["git", "add", relative_metadata_file_path])
            subprocess.run(["git", "add", f'{relative_data_path}/.gitignore'])
            # see changes stagged: git diff --name-only --cached
            subprocess.run(["git", "commit", "-m", commit_message])
        except Exception as err:
            message = ('Error trying to track and commit the metadata (dvc) in the git '
                       f'repository.\nTraceback of error: {str(err)}')
            logger.error(message)
            raise Exception(message)

        # Push the DVC metadata of the data to the git repository
        try:
            subprocess.run(["git", "push", git_remote_name, git_branch_name])
        except Exception as err:
            message = ('Error trying to push the metadata (dvc) in the git repository.'
                       f'\nTraceback of error: {str(err)}')
            logger.error(message)
            raise Exception(message)

        # TODO add command to push data versioned in dvc storage (`push dvc`)
        #  see documentation dvc
