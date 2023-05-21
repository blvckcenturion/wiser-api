from urllib.parse import urlparse, parse_qs
from models.youtube_video_resource import YoutubeVideoResourceModel
from sqlalchemy.orm.session import Session

class YoutubeVideoResourceService:

    @staticmethod
    def parse_video_id(youtube_video_url) -> str:
        """
        Parse the video id from a YouTube video URL

        Parameters
        ----------
        youtube_video_url : str
            YouTube video URL

        Returns
        -------
        str
            YouTube video id
        """
        # Parse the URL
        url = urlparse(youtube_video_url)
        # Check if the URL is a valid YouTube URL
        if url.netloc not in {"www.youtube.com", "youtu.be"}:
            raise ValueError("Invalid YouTube URL")

        # Get the video id from the URL
        video_id = None

        # If the URL is a youtu.be URL, the video id is the path of the URL
        if url.netloc == "youtu.be":
            # Remove the leading slash from the path
            video_id = url.path[1:]
        # If the URL is a www.youtube.com URL, the video id is the value of the v query parameter
        else:
            # Parse the query string of the URL
            query = parse_qs(url.query)
            # Get the video id from the query string
            video_id = query.get("v", [None])[0]

        # If the video id is not found, raise a ValueError
        if not video_id:
            raise ValueError("Invalid YouTube URL")

        # Return the video id
        return video_id

    @staticmethod
    def get_by_video_id(video_id: str, db: Session) -> YoutubeVideoResourceModel:
        """
        Get a YouTube video resource by video id

        Parameters
        ----------
        video_id : str
            Video id of the YouTube video
        db : Session
            Database session

        Returns
        -------
        YoutubeVideoResourceModel
            YouTube video resource model
        """

        # Query the database for the YouTube video resource with the provided video id
        youtube_video_resource = db.query(YoutubeVideoResourceModel).filter(YoutubeVideoResourceModel.youtube_video_id == video_id).first()
        # If the YouTube video resource is not found, raise an HTTPException
        return youtube_video_resource

    @staticmethod
    def create(video_id: str, transcription_url: str, summarization_url: str, title: str, db: Session) -> YoutubeVideoResourceModel:
        """
        Create a YouTube video resource

        Parameters
        ----------
        video_id : str
            Video id of the YouTube video
        transcription_url : str
            Transcription URL of the YouTube video
        summarization_url : str
            Summarization URL of the YouTube video
        db : Session
            Database session

        Returns
        -------
        YoutubeVideoResourceModel
            YouTube video resource model
        """
        # Create a new YouTube video resource
        youtube_video_resource = YoutubeVideoResourceModel(youtube_video_id=video_id, transcription_url=transcription_url, summarization_url=summarization_url, title=title)
        # Add the new YouTube video resource to the database session and commit the changes
        db.add(youtube_video_resource)
        # Commit the changes
        db.commit()
        # Refresh the new YouTube video resource to get the updated id
        db.refresh(youtube_video_resource)
        return youtube_video_resource