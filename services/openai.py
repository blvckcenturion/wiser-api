from langchain.document_loaders import YoutubeLoader
from langchain import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv
from langchain.docstore.document import Document
import openai

# load environment variables for OpenAI
load_dotenv()

class OpenAIService:
    """
    Service class for OpenAI related operations
    """

    @staticmethod
    def summarize(transcript) -> str:
        """
        Summarize a transcript using OpenAI's API

        Parameters
        ----------
        transcript : str
            Transcript to summarize

        Returns
        -------
        str
        """
        
        # create an OpenAI instance, set the temperature to 0 to get deterministic results
        llm = OpenAI(temperature=0)
        # create a text splitter to split the transcript into chunks of 1000 characters with 0 character overlap
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        # split the transcript into chunks of 1000 characters with 0 character overlap
        texts = text_splitter.split_text(transcript)
        # create a list of documents from the chunks of text
        docs = [Document(page_content=t) for t in texts[:3]]
        # create a summarize chain
        chain = load_summarize_chain(llm, chain_type="map_reduce")
        # run the chain on the documents and return the result
        return chain.run(docs)
    
    @staticmethod
    def transcribe(audio_path: str) -> str:
        """
        Transcribe an audio file using OpenAI's API

        Parameters
        ----------
        audio_path : str
            Path to the audio file
        
        Returns
        -------
        str

        """

        # load environment variables for OpenAI
        with open(audio_path, "rb") as audio_file:
            # transcribe the audio file using whisper-1
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            
        # return the transcript
        return transcript