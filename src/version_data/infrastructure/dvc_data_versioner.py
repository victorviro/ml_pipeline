import logging
import os
import subprocess
from subprocess import CalledProcessError
from typing import Dict, List

from dvc.api import get_url
from dvc.exceptions import OutputNotFoundError
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

from src.version_data.domain.data_versioner import IDataVersioner

logger = logging.getLogger(__name__)


class DVCDataVersioner(IDataVersioner):
    def __init__(self, git_remote_name: str, git_branch_name: str):
        """
        :param git_remote_name: Name of the remote to the git repository
        :type git_remote_name: str
        :param git_branch_name: Name of the branch of the git repository
        :type git_branch_name: str
        """
        self.git_remote_name = git_remote_name
        self.git_branch_name = git_branch_name

    def version_data(self, data_file_path: str, data_version: float) -> Dict[str, str]:
        relative_data_file_path: str = os.path.relpath(
            path=data_file_path, start=os.getcwd()
        )
        # Track the dataset in DVC repository
        self._track_data_to_dvc(relative_data_file_path)
        # Get the metadata file path of the dataset generated by DVC
        relative_metadata_file_path = f"{relative_data_file_path}.dvc"

        # Get git repo object
        git_repository: Repo = self._get_git_repository()

        # Check if the dataset has changed
        diff_output = git_repository.git.diff(relative_metadata_file_path)
        if diff_output:
            logger.info("The dataset has changed.")
            # Add and commit the DVC metadata of the dataset to the git repository
            commit_message = (
                f"Added max_char_per_line raw data, version: {data_version}"
            )
            relative_data_path = os.path.dirname(relative_data_file_path)
            relative_data_file_paths_to_commit = [
                relative_metadata_file_path,
                f"{relative_data_path}/.gitignore",
            ]
            self._commit_files_to_git_repository(
                commit_message=commit_message,
                relative_file_paths=relative_data_file_paths_to_commit,
                git_repository=git_repository,
            )

            # Push the DVC metadata of the dataset to the git repository
            self._push_to_git_repository(git_repository)

            # Push the dataset versioned in dvc storage
            self._push_to_dvc_storage()
        else:
            logger.warning("The dataset has not changed.")

        # Get information to track
        dvc_data_path = self._get_data_path_in_dvc_storage(relative_data_file_path)
        information_to_track: Dict[str, str] = {
            "dvc data path": dvc_data_path,
            "data version": str(data_version),
            "data file path": data_file_path,
        }
        return information_to_track

    @staticmethod
    def _track_data_to_dvc(relative_data_file_path: str) -> None:
        """
        Track data in DVC repository.

        :param relative_data_file_path: Relative path of data to be tracked
        :type relative_data_file_path: str
        """
        try:
            output = subprocess.run(
                ["dvc", "add", relative_data_file_path], capture_output=True, check=True
            )
            logger.info(
                "Tracked the dataset in the DVC repository using subprocess. "
                f"Stdout: {output.stdout.decode('utf-8')}"
            )
        except CalledProcessError as err:
            msg = (
                "Error tracking the dataset in the DVC repository using subprocess. "
                f"Command: {err.cmd}. Error: {err.stderr}"
            )
            logger.error(msg)
            raise Exception(msg) from err

    @staticmethod
    def _get_git_repository() -> Repo:
        """
        Get git repository (GitPython) from current project.

        :return: Object representing a git repository
        :rtype: Repo
        """
        repo_path: str = os.getcwd()
        try:
            git_repository: Repo = Repo(path=repo_path)
            logger.info(f"Obtained git repository of project in path {repo_path}.")
            return git_repository
        except InvalidGitRepositoryError as err:
            msg = (
                "Error getting git repository using GitPython. There is no .git file "
                f"in the path: {repo_path}."
            )
            logger.info(msg)
            raise InvalidGitRepositoryError(msg) from err

    @staticmethod
    def _commit_files_to_git_repository(
        commit_message: str, relative_file_paths: List[str], git_repository: Repo
    ) -> None:
        """
        Add and commit files to the git repository.

        :param commit_message: Text of the message for the commit
        :type commit_message: str
        :param relative_file_paths: Relative path of files to be commited
        :type relative_file_paths: list
        :param git_repository: Object representing a git repository
        :type git_repository: Repo
        """
        try:
            for relative_file_path in relative_file_paths:
                git_repository.git.add(relative_file_path)
            git_repository.git.commit(m=commit_message)
        except GitCommandError as err:
            msg = (
                "Error tracking or committing files to git repository. "
                f"Command: {err.command}. Error: {err.stderr}."
            )
            logger.error(msg)
            raise Exception(msg) from err

    def _push_to_git_repository(self, git_repository: Repo) -> None:
        """
        Push changes to git repository.

        :param git_repository: Object representing a git repository
        :type git_repository: Repo
        """

        try:
            origin = git_repository.remote(name=self.git_remote_name)
            output = origin.push(refspec=self.git_branch_name)
            commit_hash = output[0].summary
            logger.info(
                f"Pushed changes to git repository in the branch "
                f"{self.git_branch_name}. Commit hash: {commit_hash}."
            )
        except ValueError as err:
            message = (
                f"Error getting remote named {self.git_remote_name} of the git repo."
            )
            logger.error(message)
            raise ValueError(message) from err
        except GitCommandError as err:
            msg = (
                "Error pushing commited changes in the branch named"
                f" {self.git_branch_name}. Command: {err.command}. Error: {err.stderr}"
            )
            logger.error(msg)
            raise Exception(msg) from err

    @staticmethod
    def _push_to_dvc_storage() -> None:
        try:
            # If GCS is the remote storage, env var GOOGLE_APPLICATION_CREDENTIALS needed
            output = subprocess.run(["dvc", "push"], capture_output=True, check=True)
            logger.info(
                "Dataset versioned pushed in the DVC storage using subprocess"
                f". Stdout: {output.stdout.decode('utf-8')}"
            )
        except CalledProcessError as err:
            msg = (
                "Error pushing the dataset versioned in the DVC storage. "
                f"Command: {err.cmd}. Error: {err.stderr}."
            )
            logger.error(msg)
            raise Exception(msg) from err

    @staticmethod
    def _get_data_path_in_dvc_storage(relative_data_file_path: str) -> str:
        """
        Get path of the data in dvc storage.

        :param relative_data_file_path: Relative local path of data tracked
        :type relative_data_file_path: str
        :return: path of the data in dvc storage
        :rtype: str
        """
        try:
            dvc_data_path: str = get_url(path=relative_data_file_path, repo=os.getcwd())
            logger.info("Dataset path in DVC storage gotten succesfully")
            return dvc_data_path
        except OutputNotFoundError as err:
            message = "Error getting dataset path in DVC storage."
            logger.error(message)
            raise Exception(message) from err
