#!/usr/bin/env bash
# One ElevenLabs take per segment, trimmed and loudness-matched like the Gemini script. The API key is added by the credential proxy.
# Usage: ./generar-segmentos-elevenlabs.sh [voice_id] [ids] [model]
set -euo pipefail
cd "$(dirname "$0")"
VOICE="${1:-rpqlUOplj0Q0PIilat8h}"; SOLO="${2:-}"; MODEL="${3:-eleven_multilingual_v2}"
mkdir -p seg
n=$(jq length segmentos.json)
for i in $(seq 0 $((n-1))); do
  id=$(jq -r ".[$i].id" segmentos.json); text=$(jq -r ".[$i].text" segmentos.json)
  if [ -n "$SOLO" ] && [[ ",$SOLO," != *",$id,"* ]]; then continue; fi
  body=$(jq -n --arg t "$text" --arg m "$MODEL" '{text:$t, model_id:$m, voice_settings:{stability:0.45, similarity_boost:0.8, style:0.25, use_speaker_boost:true}}')
  code=$(curl -sS -m 120 -o "seg/$id.mp3" -w "%{http_code}" -H "Content-Type: application/json" -H "xi-api-key: dummy" \
    "https://api.elevenlabs.io/v1/text-to-speech/$VOICE?output_format=mp3_44100_128" -d "$body")
  [ "$code" = "200" ] || { echo "$id: HTTP $code $(head -c 200 seg/$id.mp3)"; exit 1; }
  ffmpeg -y -loglevel error -i "seg/$id.mp3" -af "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,loudnorm=I=-19:TP=-2:LRA=7" -ar 44100 -ac 1 "seg/$id.wav"
  rm -f "seg/$id.mp3"
  echo "$id $(ffprobe -v error -show_entries format=duration -of csv=p=0 seg/$id.wav)"
done
