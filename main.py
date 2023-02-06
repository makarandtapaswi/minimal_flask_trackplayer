import os
import pdb
import json
import random
import collections

# Flask imports
from flask import Flask, render_template, redirect, flash, request, url_for, make_response, send_file

# Create the main Flask application
app = Flask(__name__)
# openssl rand -base64 64
app.secret_key = 'KH3UmcjdhBWqTAwjmRfRVBvvE4cS5NjezSC10JAvkRM68gFQPy42Y2hKz5tp/xoEsYB8j+UN9ZbRgzLb2wCUGw=='
# Reload when template file changes!
# app.config['TEMPLATES_AUTO_RELOAD'] = True

DATA_ROOT = 'data'
TRACK_ROOT = 'data'

@app.route('/')
def home():
    vids = [vid for vid in os.listdir(DATA_ROOT) if vid.endswith('mp4')]
    return render_template('list_videos.html', vids=vids)


@app.route('/video/<clip>/')
def play_video(clip):
    return send_file(os.path.join(DATA_ROOT, clip))


def convert_track_to_web_json(fname, fn_ts):
    """Load and convert to web display format

    JSON is a list of dictionaries, each containing: bbox, fn, ts, ftid, ftname, idx
    """

    with open(fname, 'rb') as fid:
        data = json.load(fid)
    tracks, frame2tracks = data['ftracks'], data['frame2ftracks']

    # create placeholder frames
    frames = []
    for fn, ts in fn_ts:
        frames.append({'fn': fn, 'ts': ts, 'bbox': [], 'ftid': []})

    # convert tracks to frames
    for track in tracks:
        for det in track:
            fn = det['frame']
            x, y, w, h = det['x'], det['y'], det['w'], det['h']
            frames[fn]['bbox'].append([x, y, w, h])
            frames[fn]['ftid'].append(det['ftrack_id'])

    return frames


def load_matidx(clip):
    """Load the frame-number timestamp mappings
    """
    fname = os.path.join(DATA_ROOT, os.path.splitext(clip)[0] + '.matidx')
    with open(fname, 'r') as fid:
        data = fid.readlines()
    data = [d.strip().split() for d in data if d.strip()]
    fn_ts = [(int(d[0]), float(d[1])) for d in data]
    return fn_ts


@app.route('/play_tracks/<clip>/')
def play_tracks(clip):
    """Page to play track files
    """
    # load framenumber - timestamp
    fn_ts = load_matidx(clip)

    # load tracks
    track_fname = os.path.join(TRACK_ROOT, os.path.splitext(clip)[0] + '.track')
    tracks = convert_track_to_web_json(track_fname, fn_ts)

    # max num-boxes per frame
    N = max([len(frame_dets['bbox']) for frame_dets in tracks])

    # send video name and tracks to player
    return render_template('track_player.html', clip=clip, N=N,
                                     tracks=tracks)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2341, threaded=True, debug=True)
    # app.run()


