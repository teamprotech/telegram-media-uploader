# telegram-media-uploader

Based onto Python 3 scripting, it uploads given file-paths in argument to any Telegram chat/group/channel.
This script takes at least one argument i.e file. If more files are passed, then also it will work automatically uploading all files.
And in that case it keeps tack of every-file completed out of the given arguments of file-path list...
As such, one may pass `ls someDirPath/*` as files to be uploaded or any other Linux-syntax resolving to a list of paths. eg: dir/* too.
In case the process was interupted due to any reason like power/net failure, you just run same command again, say:
```
python uploader.py myVideos/*
```
And this script will automatically, resume from where it was failed!!!

BUT, if 1st-Argument is passed as "--fresh", then script will NOT resume and will treat that you want to execute a fresh-new set of files.

## Features are listed below:

1. Resuming the upload
2. Chat-Title based : no headache of finding & working with chat-id
3. progress-BAR reporting
4. Speed reporting for each file uploaded
5. Takes multiple file-path list, from different directories in a sinle command
6. Log file_Size & taken_Time for every uploaded-file
7. Set Caption, enable-Streaming automatically


## Dependencies are given into the requirements-file and can be installed using pip as below:

```
$ pip install -r requirements.txt
```

## Usage

```
$ python uploader.py myVideos/*
```
	=> Will start a fresh-set of uploads, if you running this first time else it will resume the previous set you ran before.
	   And wil do the upload again or will tell you if previous set already finihed...
```
$ python uploader.py --fresh myVideos/*
```
	=> Run with "--fresh" flag any time you want to FORCE to start the file-sets as new (NOT resume)...

### zsh shell 
Default globbing is always alphabetical in most shells.
zsh shell is recommended to force file sequncing in time based shorting (instead of Alphabatical shorting) with option (Om) as:

```
$ python uploader.py myVideos/*(Om)
```

## Some Fixes for reference
To fix the error of "telethon.errors.rpcbaseerrors.AuthKeyError: RPCError 406: UPDATE_APP_TO_LOGIN (caused by SignInRequest)..."
Use below code to update to v-1.25++ at the time of writing...

```
$ python3 -m pip install --upgrade telethon
```
Ref: https://github.com/LonamiWebs/Telethon/issues/3215#issuecomment-985954619

To let telethon determine metadata from audio and video files automatically while uploading the video file, so that the uploaded video shows the proper duratin,
instead of the false 0:0, you may install the python module "hachoir" as:
```
$ python3 -m pip install -U hachoir
```