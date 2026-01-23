from django.shortcuts import render
from django.shortcuts import render
from music21 import stream, note, chord, meter, clef, layout
import music21
import io
import json
import re
from music21 import stream, clef, note, pitch
import json
import os
from django.shortcuts import render
from music21 import stream, note, chord, key, clef

# Create your views here.


def home(request):
    # Update this path to your actual JSON location
    path = r"C:\Users\Asamoah\Desktop\kofi\aseda_a\adom\static\hymns.json"
    
    # 1. Get the hymn ID from the URL
    hymn_to_find = request.GET.get('hymn', 'mhb444') 

    # 2. Load the JSON data
    try:
        with open(path, 'r', encoding='utf-8') as file:
            all_data = json.load(file)
            
        target_hymn = next((item for item in all_data if item.get("title") == hymn_to_find), None)
        
        if not target_hymn:
            target_hymn = all_data[0]
            hymn_to_find = target_hymn.get("title")

    except (FileNotFoundError, json.JSONDecodeError) as e:
        return render(request, 'school_app/home.html', {'error': f"Data error: {str(e)}"})

    # 3. Processing Logic
    note_bank = target_hymn.get("Notes", [])
    
    def normalize_music_durations(data):
        final_result = []
        # Target string to remove
        artifact = "Instr. Pf38174694e739a42c62da322f6bf8e73"
        
        for sublist in data:
            parsed_notes = []
            for item in sublist:
                try:
                    # Remove the unwanted instrument string from the item
                    clean_item = item.replace(artifact, "").strip()
                    
                    note_val, duration = clean_item.rsplit(' ', 1)
                    parsed_notes.append([note_val, float(duration)])
                except ValueError: 
                    continue
            
            current_working_notes = parsed_notes
            while current_working_notes:
                durations = [n[1] for n in current_working_notes]
                min_dur = min(durations)
                normalized_sublist = []
                surplus_list = []
                for n_val, dur in current_working_notes:
                    normalized_sublist.append(f"{n_val} {min_dur}")
                    remainder = dur - min_dur
                    if remainder > 0:
                        surplus_list.append([n_val, remainder])
                final_result.append(normalized_sublist)
                current_working_notes = surplus_list
        return final_result

    music_hat = normalize_music_durations(note_bank)
    music_is = []
    for group in music_hat:
        notes_only = []
        duration = 1.0
        for item in group:
            parts = item.split()
            if len(parts) >= 2:
                notes_only.append(parts[0])
                duration = float(parts[1])
        music_is.append((notes_only, duration))

    # --- Music21 Scoring ---
    key_map = {
        "A major": key.Key('A'), "A- major": key.Key('A-'), "B- major": key.Key('B-'),
        "C major": key.Key('C'), "C# major": key.Key('C#'), "D major": key.Key('D'),
        "E major": key.Key('E'), "E- major": key.Key('E-'), "F major": key.Key('F'),
        "G major": key.Key('G')
    }

    my_score = stream.Score()
    current_key = key_map.get(target_hymn.get("Key"), key.Key('C'))
    top = stream.Part(); top.append(clef.TrebleClef()); top.append(current_key)
    bottom = stream.Part(); bottom.append(clef.BassClef()); bottom.append(current_key)

    for pitches, dur in music_is: 
        treble, bass = [], []
        for p in pitches:
            try:
                if note.Pitch(p).ps < 60: bass.append(p)
                else: treble.append(p)
            except: continue # Skip if pitch parsing fails after cleaning
            
        if treble:
            c = chord.Chord(treble); c.quarterLength = dur; top.append(c)
        if bass:
            c = chord.Chord(bass); c.quarterLength = dur; bottom.append(c)

    top.makeMeasures(inPlace=True); bottom.makeMeasures(inPlace=True)
    my_score.insert(0, top); my_score.insert(0, bottom)


    def clean_note_text(text):
        # This regex looks for "Instr." followed by any non-whitespace characters
        return re.sub(r'Instr\.\s*\S+', '', text).strip()

    def normalize_music_durations(data):
        final_result = []
        for sublist in data:
            parsed_notes = []
            for item in sublist:
                try:
                    # Clean the item before splitting
                    clean_item = clean_note_text(item)
                    note_val, duration = clean_item.rsplit(' ', 1)
                    parsed_notes.append([note_val, float(duration)])
                except ValueError: continue
            # ... (rest of your existing duration logic)
        return final_result

    # --- XML Generation Cleaning ---
    top.partName = ""
    bottom.partName = ""
    
    out_xml = my_score.write('musicxml')
    with open(out_xml, 'r', encoding='utf-8') as f:
        xml_content = f.read()
    # Final sweep of the XML string to remove any leftover instrument tags
    xml_content = re.sub(r'Instr\.\s*\S+', '', xml_content)

    if os.path.exists(out_xml): os.remove(out_xml)
    
    # ... (rest of your context and return)
    # 4. Final Context
    context = {
        'all_hymns': all_data,
        'hymn_title': hymn_to_find,
        'tune': target_hymn.get("Tune"),
        'key_signature': target_hymn.get("Key"),
        'xml_data': xml_content,
        'progression_json': json.dumps(music_is),
    }
    
    return render(request, 'choir/home.html', context)