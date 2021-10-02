
from pathlib import Path
from importlib_metadata import pathlib
from pydantic import BaseModel, HttpUrl, validator, root_validator, Field
import typing
import httpx


content_type_images = [
    "image/apng",
    "image/avif",
    "image/flif",
    "image/gif",
    "image/jpeg",
    "image/jxl",
    "image/png",
    "image/svg+xml",
    "image/webp",
    "image/x-mng"
]

class Attachment(BaseModel):
    """A respresentation of an attachment suppied by a user.."""
    id: int
    filename: str
    content_type: typing.Optional[str] = Field(None)
    size: int
    url: HttpUrl
    proxy_url: str
    height: typing.Optional[int] = Field(None)
    width: int = Field(None)
    ephemeral: typing.Optional[bool] = Field(False)
    
    @validator("height", "width")
    def verify_image_height(cls, v):
        if cls.content_type in content_type_images:
            if v is None:
                raise ValueError("Image must have a height and width")
        return v
    
    async def download(self, specified_file_path: typing.Union[Path, str] = Path()) -> Path:
        """Downloads the file based on the proxy_url provided. Returns a Path object to the file upon completion.

        Args:
            specified_file_path (typing.Union[Path, str]): Overrides the default saved file name.

        Raises:
            FileExistsError: If the file name already exists.

        Returns:
            Path: If the file was successfully downloaded.
        """
        if isinstance(specified_file_path, str):
            specified_file_path = Path(specified_file_path)
        
        if (specified_file_path / self.filename).exists():
            raise FileExistsError(f"File {self.filename} already exists in {specified_file_path}.")
        
        # TODO: Add version in header.
        with httpx.AsyncClient(headers={"User-Agent": f"dispike"}) as client:
            async with client.stream("GET", self.proxy_url) as response:
                with open(specified_file_path / self.filename, "wb") as f:
                    async for chunk in response.aiter_bytes():
                        f.write(chunk)
        return (specified_file_path / self.filename)