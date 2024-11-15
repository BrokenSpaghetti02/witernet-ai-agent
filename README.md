# witernet-ai-agent
This project is a simple webapp that allows the user to upload a set of PDF files to form the knowledge base of the AI agent.

## Step 1
Open up a new terminal window, clone this repository, and go to the root directory of the repo.
```
git clone git@github.com:BrokenSpaghetti02/witernet-ai-agent.git
cd witernet-ai-agent
```

## Step 2
Install all the dependencies.
```
pip3 install -r requirements.txt
```

## Step 3
Next, download Ollama from the official [website](https://ollama.com/) depending on your OS: Windows, Linux, or Mac.

## Step 4
After downloading ollama, open up a new terminal window and type 
```ollama pull llama3.2```
and then
```ollama serve```
This will start the Ollama Llama3.2 LLM model server locally.

## Step 5
As the Ollama server is running, go back to the previous terminal and type:
```
streamlit run app.py
```

## Step 6
Select ```Browse Files``` to select the PDF files for creating the desired knowledge base. This process will take some time depending on the system's resources.

## Step 7
After the PDF files are processed, ask away.

If any issues or bugs are faced, please post an issue and I will get back to you shortly.
