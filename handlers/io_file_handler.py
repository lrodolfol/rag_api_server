import os
from static.LogginService import LoggerService


class IOFileHandler:

    def __init__(self, base_path: str = "."):
        self.base_path = os.path.abspath(base_path)
        self.logger = LoggerService(self.__class__.__name__, "INFO")

    def _resolve_path(self, relative_path: str) -> str:
        candidate = os.path.abspath(os.path.join(self.base_path, relative_path))
        if not candidate.startswith(self.base_path):
            message = f"Path {relative_path} escapes the base directory."
            self.logger.error(message)
            raise ValueError(message)
        return candidate

    def read(self, relative_path: str, encoding: str = "utf-8") -> str:
        resolved = self._resolve_path(relative_path)
        try:
            with open(resolved, "r", encoding=encoding) as file:
                return file.read()
        except FileNotFoundError:
            return ""
        except Exception as error:
            self.logger.error(f"Failed to read {relative_path}: {error}")
            raise

    def write(
        self,
        relative_path: str,
        content: str,
        encoding: str = "utf-8",
        extension: str = ".md",
        overwrite: bool = True,
    ) -> None:
        resolved = self._resolve_path(relative_path)
        os.makedirs(os.path.dirname(resolved), exist_ok=True)
        if not overwrite and os.path.exists(resolved):
            message = f"{relative_path} already exists."
            self.logger.error(message)
            raise FileExistsError(message)
        with open(f"{resolved}{extension}", "w", encoding=encoding) as file:
            file.write(content)

    def merge_directory_into_file(
        self,
        directory_path: str,
        output_file: str,
        encoding: str = "utf-8",
    ) -> None:
        resolved_dir = self._resolve_path("./")
        if not os.path.isdir(resolved_dir):
            self.logger.error(f"{directory_path} is not a directory.")
            raise NotADirectoryError(f"{directory_path} is not a directory.")

        contents: list[str] = []
        for root, dirs, files in os.walk(resolved_dir):
            dirs.sort()
            for filename in sorted(files):
                if filename.replace(".md","") == output_file:
                    continue

                file_path = os.path.join(root, filename)
                if not os.path.isfile(file_path):
                    continue
                contents.append(self.read(os.path.relpath(file_path, self.base_path), encoding=encoding))

        merged_content = "\n".join(contents)
        self.write(output_file, merged_content, encoding=encoding, extension=".md", overwrite=True)

    def delete(self, relative_path: str) -> bool:
        resolved = self._resolve_path(relative_path)
        if not os.path.exists(resolved):
            return False
        os.remove(resolved)
        return True
