#!/usr/bin/python3
from flask import Flask, Response, render_template_string, request, redirect
import requests

app = Flask(__name__)


username = "7576"
password = "7576"


#=======================================================================================================================

channels_ids = "https://mw.nimitv.net/wbs/api/media/channels/?categoryId=0&type=TV"


@app.route('/stream/<channel_id>.m3u8')
def stream(channel_id):
    try:
        sessionId = get_sessionId(username, password)
        channel_url = f"https://mw.nimitv.net/wbs/api/v2/tv/{channel_id}"
        headers = {
            "Cookie": f"JSESSIONID={sessionId}"
        }
        response = requests.get(channel_url, headers=headers, verify=False)
        response.raise_for_status()
        stream_url = response.json()["playbackUrl"]
        return redirect(stream_url)
    except Exception as e:
        return Response(f"Error: {str(e)}", status=500)




@app.route('/generated_playlist.m3u')
def generated_playlist():
    sessionId = get_sessionId(username, password)

    headers = {
        "Cookie": f"JSESSIONID={sessionId}"
    }

    channels_response = requests.get(channels_ids, headers=headers, verify=False).json()
    
    # Start building M3U playlist
    playlist = "#EXTM3U\n"
    
    for channel in channels_response:
        channel_id = channel['id']
        channel_name = channel['name']
        
        # Add channel info and stream URL
        playlist += f"#EXTINF:-1,{channel_name}\n"
        playlist += f"https://nimi-2ba10c703527.herokuapp.com:80/stream/{channel_id}.m3u8\n"

    return Response(
        playlist,
        mimetype='application/x-mpegurl',
        headers={'Content-Disposition': 'attachment; filename=playlist.m3u'}
    )
        

def get_sessionId(username, password):
 
    payload = {
        "model": "Electron App",
        "userName": username,
        "password": password,
        "serialNumber": "pc.7d48b247bc4dd3921c961ba0bf9f6d55",
        "macAddress": "00:15:5d:f4:05:72"
    }
    headers = {
        "Content-Type": "application/json"
    }   
    response = requests.post(url, json=payload, headers=headers, verify=False)
    # Get the Set-Cookie header
   
    String header = response.headers().get("Set-Cookie");
       String arr[] = header.split("=");
       String jsessionid = arr[1];
       jsessionid = jsessionid.substring(0,jsessionid.length()-5);
    return jsessionid

app.run(host='0.0.0.0', port=80)
