# specify the base image
FROM python:3
# where to set up the app in the python container, optional
# tells docker where all the commands run from
WORKDIR /usr/src/app

# copy the requirements.txt from local machine to container, ./ copies it to the current working directory (would ned full path if workdir not included)
COPY requirements.txt ./

# run a command responsible for installing dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copies everything from our current dir to the current dir in container, same applies again wrt WORKDIR
COPY . .
# when docker runs, actually treats each step as a layer; run top to bottom and caches results of each step. If nothing changes, keeps the cached result. If nothing changes, knows nothing has changed and if the source code changes for example, doesn't change the initial steps but only changes 'COPY . .' - but if we change requirements.txt then it'll rerun STEP 3 onwards, which is the longest step. This is primarily for optimisation

# give it the command to run when it starts the container
# want to run 'uvicorn app.main:app --host 0.0.0.0 --port 8000' like on ubuntu. Comma indicates a space
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]