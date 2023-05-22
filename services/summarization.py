from schemas.summarization import SummarizationCreate, SummarizationGet
from models.youtube_video_resource import YoutubeVideoResourceModel
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.summarization import SummarizationModel
from services.youtube_video_resource import YoutubeVideoResourceService
from services.google_storage import GoogleStorageService
from services.openai import OpenAIService
import tempfile
from pytube import YouTube
import os
from moviepy.editor import *

class SummarizationService:

    @staticmethod
    def generate_video_summarization(summarization: SummarizationCreate, user_id: int, db: Session):
        """
        Create a summarization for a user

        Parameters
        ----------
        summarization : SummarizationCreate
            Summarization create model
        user_id : int
            Id of the user
        db : Session
            Database session
        """

        try:
            # Parse the youtube video id from the youtube video url
            video_id = YoutubeVideoResourceService.parse_video_id(summarization.youtube_video_url)

            # Verify that the video id is not already in the database
            youtube_video_resource = YoutubeVideoResourceService.get_by_video_id(video_id, db)
            
            # If the video id is in the database then check if the summarization already exists for the user
            if youtube_video_resource:
                # Query the database for the summarization
                summarization = db.query(SummarizationModel).filter(SummarizationModel.user_id == user_id, SummarizationModel.youtube_video_resource_id == youtube_video_resource.id).first()
                # If the summarization already exists for the user then raise an HTTPException
                if summarization:
                    raise Exception("Summarization for this video & user already exists")

            else:
                # If the video id is not in the database then create a new youtube video resource and store it in the database
                # Download the video, store it in a temporary directory, and transcribe it
                with tempfile.TemporaryDirectory() as temp_dir:
                    # Find the video
                    yt = YouTube("https://www.youtube.com/watch?v=" + video_id)
                    # Get length of video
                    length = yt.length
                    # Get the title of the video
                    title = yt.title
                    
                    # Check if video is too long (30 minutes)
                    if length > 1800:
                        # If video is too long, raise an exception
                        raise Exception("Video is too long")

                    # Get the audio stream of the video (mp3)
                    audio_stream = yt.streams.filter(only_audio=True).first()
                    # Download the audio stream and store it in the temporary directory
                    audio_stream.download(output_path=temp_dir)
                    # Get the path of the audio stream
                    audio_path = os.path.join(temp_dir, audio_stream.default_filename)
                    # Convert the audio stream to mp3
                    audio_clip = AudioFileClip(audio_path)
                    # Write the audio clip to a file
                    audio_clip.write_audiofile(os.path.join(temp_dir, f"{video_id}.mp3"))
                    # Form the temporary path of the audio clip
                    audio_path = f"{temp_dir}/{video_id}.mp3"
                    # Transcribe the audio
                    transcript = OpenAIService.transcribe(audio_path)
                    # Upload the transcription to Google Cloud Storage
                    transcription_url = GoogleStorageService.create_and_upload_file(os.path.join(temp_dir, f"transcription-{video_id}.txt"), transcript.text, f"transcription-{video_id}.txt")
                    # Summarize the transcription
                    summary = OpenAIService.summarize(transcript.text)
                    # Upload the summarization to Google Cloud Storage
                    summarization_url = GoogleStorageService.create_and_upload_file(os.path.join(temp_dir, f"summarization-{video_id}.txt"), summary, f"summarization-{video_id}.txt")
                    # Create a youtube video resource
                    youtube_video_resource = YoutubeVideoResourceService.create(video_id, transcription_url, summarization_url,title, db)
            # Create a summarization
            summarization = SummarizationService.create_summarization(user_id, youtube_video_resource.id, db)
            # Return the summarization
            return SummarizationGet(id=summarization.id, title=youtube_video_resource.title, youtube_video_id=youtube_video_resource.youtube_video_id)

        except Exception as e:
            db.rollback()
            if "regex_search" in str(e):
                raise HTTPException(status_code=400, detail="Invalid YouTube URL")
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    def create_summarization(user_id: int, youtube_video_resource_id: int, db: Session) -> SummarizationModel:
        """
        Create a summarization

        Parameters
        ----------
        user_id : int
            Id of the user
        youtube_video_resource_id : int
            Id of the youtube video resource
        db : Session
            Database session

        Returns
        -------
        SummarizationModel
            Summarization model
        """

        # Create a summarization
        summarization = SummarizationModel(user_id=user_id, youtube_video_resource_id=youtube_video_resource_id)
        # Add the summarization to the database
        db.add(summarization)
        # Commit the changes to the database
        db.commit()
        # Refresh the summarization
        db.refresh(summarization)
        # Return the summarization
        return summarization

    @staticmethod
    def get_summarizations_by_user(user_id: int, db: Session) -> list[SummarizationGet]:
        """
        Get all summarizations for a user

        Parameters
        ----------
        user_id : int
            Id of the user
        db : Session
            Database session

        Returns
        -------
        list[SummarizationGet]
            List of summarization get models
        """

        # Query the database for all summarizations for the user and join the youtube video resource
        summarizations = db.query(SummarizationModel).join(YoutubeVideoResourceModel).filter(SummarizationModel.user_id == user_id).all()
        
        # Map the summarizations to summarization get models and return them
        return [SummarizationGet(id=summarization.id, transcription_url=summarization.youtube_video_resource.transcription_url, summarization_url=summarization.youtube_video_resource.summarization_url, title=summarization.youtube_video_resource.title, youtube_video_id=summarization.youtube_video_resource.youtube_video_id) for summarization in summarizations]