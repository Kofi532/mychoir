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
from django.conf import settings

# Create your views here.


# def home(request):
#     # Update this path to your actual JSON location
#     # path = r"C:\Users\Asamoah\Desktop\kofi\aseda_a\adom\static\hymns.json"


#     # This builds the path dynamically based on your current environment
#     path = os.path.join(settings.BASE_DIR, 'static', 'hymns.json')

#     with open(path, 'r', encoding='utf-8') as f:
#         data = json.load(f)
    
#     # 1. Get the hymn ID from the URL
#     hymn_to_find = request.GET.get('hymn', 'mhb444') 

#     # 2. Load the JSON data
#     try:
#         with open(path, 'r', encoding='utf-8') as file:
#             all_data = json.load(file)
            
#         target_hymn = next((item for item in all_data if item.get("title") == hymn_to_find), None)
        
#         if not target_hymn:
#             target_hymn = all_data[0]
#             hymn_to_find = target_hymn.get("title")

#     except (FileNotFoundError, json.JSONDecodeError) as e:
#         return render(request, 'choir/home.html', {'error': f"Data error: {str(e)}"})

#     # 3. Processing Logic
#     note_bank = target_hymn.get("Notes", [])
    
#     def normalize_music_durations(data):
#         final_result = []
#         # Target string to remove
#         artifact = "Instr. Pf38174694e739a42c62da322f6bf8e73"
        
#         for sublist in data:
#             parsed_notes = []
#             for item in sublist:
#                 try:
#                     # Remove the unwanted instrument string from the item
#                     clean_item = item.replace(artifact, "").strip()
                    
#                     note_val, duration = clean_item.rsplit(' ', 1)
#                     parsed_notes.append([note_val, float(duration)])
#                 except ValueError: 
#                     continue
            
#             current_working_notes = parsed_notes
#             while current_working_notes:
#                 durations = [n[1] for n in current_working_notes]
#                 min_dur = min(durations)
#                 normalized_sublist = []
#                 surplus_list = []
#                 for n_val, dur in current_working_notes:
#                     normalized_sublist.append(f"{n_val} {min_dur}")
#                     remainder = dur - min_dur
#                     if remainder > 0:
#                         surplus_list.append([n_val, remainder])
#                 final_result.append(normalized_sublist)
#                 current_working_notes = surplus_list
#         return final_result

#     music_hat = normalize_music_durations(note_bank)
#     music_is = []
#     for group in music_hat:
#         notes_only = []
#         duration = 1.0
#         for item in group:
#             parts = item.split()
#             if len(parts) >= 2:
#                 notes_only.append(parts[0])
#                 duration = float(parts[1])
#         music_is.append((notes_only, duration))

#     # --- Music21 Scoring ---
#     key_map = {
#         "A major": key.Key('A'), "A- major": key.Key('A-'), "B- major": key.Key('B-'),
#         "C major": key.Key('C'), "C# major": key.Key('C#'), "D major": key.Key('D'),
#         "E major": key.Key('E'), "E- major": key.Key('E-'), "F major": key.Key('F'),
#         "G major": key.Key('G')
#     }

#     my_score = stream.Score()
#     current_key = key_map.get(target_hymn.get("Key"), key.Key('C'))
#     top = stream.Part(); top.append(clef.TrebleClef()); top.append(current_key)
#     bottom = stream.Part(); bottom.append(clef.BassClef()); bottom.append(current_key)

#     for pitches, dur in music_is: 
#         treble, bass = [], []
#         for p in pitches:
#             try:
#                 if note.Pitch(p).ps < 60: bass.append(p)
#                 else: treble.append(p)
#             except: continue # Skip if pitch parsing fails after cleaning
            
#         if treble:
#             c = chord.Chord(treble); c.quarterLength = dur; top.append(c)
#         if bass:
#             c = chord.Chord(bass); c.quarterLength = dur; bottom.append(c)

#     top.makeMeasures(inPlace=True); bottom.makeMeasures(inPlace=True)
#     my_score.insert(0, top); my_score.insert(0, bottom)


#     def clean_note_text(text):
#         # This regex looks for "Instr." followed by any non-whitespace characters
#         return re.sub(r'Instr\.\s*\S+', '', text).strip()

#     def normalize_music_durations(data):
#         final_result = []
#         for sublist in data:
#             parsed_notes = []
#             for item in sublist:
#                 try:
#                     # Clean the item before splitting
#                     clean_item = clean_note_text(item)
#                     note_val, duration = clean_item.rsplit(' ', 1)
#                     parsed_notes.append([note_val, float(duration)])
#                 except ValueError: continue
#             # ... (rest of your existing duration logic)
#         return final_result

#     # --- XML Generation Cleaning ---
#     top.partName = ""
#     bottom.partName = ""
    
#     out_xml = my_score.write('musicxml')
#     with open(out_xml, 'r', encoding='utf-8') as f:
#         xml_content = f.read()
#     # Final sweep of the XML string to remove any leftover instrument tags
#     xml_content = re.sub(r'Instr\.\s*\S+', '', xml_content)

#     if os.path.exists(out_xml): os.remove(out_xml)
    
#     # ... (rest of your context and return)
#     # 4. Final Context
#     context = {
#         'all_hymns': all_data,
#         'hymn_title': hymn_to_find,
#         'tune': target_hymn.get("Tune"),
#         'key_signature': target_hymn.get("Key"),
#         'xml_data': xml_content,
#         'progression_json': json.dumps(music_is),
#     }
    
#     return render(request, 'choir/home.html', context)


import os
import json
import re
from django.conf import settings
from django.shortcuts import render
from music21 import stream, note, chord, clef, key

def homeworl(request):
    # 1. Setup Path and Load All Data
    path = os.path.join(settings.BASE_DIR, 'static', 'hymns_cleaned.json')
    
    try:
        with open(path, 'r', encoding='utf-8') as file:
            all_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return render(request, 'choir/home.html', {'error': f"Data error: {str(e)}"})

    # 2. Get the hymn ID from the URL (NO DEFAULT VALUE HERE)
    hymn_to_find = request.GET.get('hymn') 

    # Initialize variables for the template
    target_hymn = None
    xml_content = ""
    music_is = []
    tune = ""
    key_sig = ""

    # Helper function for cleaning text
    def clean_note_text(text):
        return re.sub(r'Instr\.\s*\S+', '', text).strip()

    # Helper function for duration logic
    def normalize_music_durations(data):
        final_result = []
        for sublist in data:
            parsed_notes = []
            for item in sublist:
                try:
                    clean_item = clean_note_text(item)
                    note_val, duration = clean_item.rsplit(' ', 1)
                    parsed_notes.append([note_val, float(duration)])
                except ValueError: 
                    continue
            
            current_working_notes = parsed_notes
            while current_working_notes:
                durations = [n[1] for n in current_working_notes]
                if not durations: break
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

    # 3. Only Process if a Hymn is Selected
    if hymn_to_find:
        target_hymn = next((item for item in all_data if item.get("title") == hymn_to_find), None)
        
        if target_hymn:
            tune = target_hymn.get("Tune")
            key_sig = target_hymn.get("Key")
            note_bank = target_hymn.get("Notes", [])
            
            # --- Processing Logic ---
            music_hat = normalize_music_durations(note_bank)
            
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
            current_key = key_map.get(key_sig, key.Key('C'))
            
            top = stream.Part()
            top.append(clef.TrebleClef())
            top.append(current_key)
            
            bottom = stream.Part()
            bottom.append(clef.BassClef())
            bottom.append(current_key)

            for pitches, dur in music_is: 
                treble, bass = [], []
                for p in pitches:
                    try:
                        if note.Pitch(p).ps < 60: bass.append(p)
                        else: treble.append(p)
                    except: continue 
                
                if treble:
                    c = chord.Chord(treble)
                    c.quarterLength = dur
                    top.append(c)
                if bass:
                    c = chord.Chord(bass)
                    c.quarterLength = dur
                    bottom.append(c)

            top.makeMeasures(inPlace=True)
            bottom.makeMeasures(inPlace=True)
            my_score.insert(0, top)
            my_score.insert(0, bottom)

            # --- XML Generation ---
            top.partName = ""
            bottom.partName = ""
            
            out_xml = my_score.write('musicxml')
            with open(out_xml, 'r', encoding='utf-8') as f:
                xml_content = f.read()
            
            # Final sweep of XML string
            xml_content = re.sub(r'Instr\.\s*\S+', '', xml_content)

            if os.path.exists(out_xml): 
                os.remove(out_xml)
        else:
            # If the title in URL doesn't exist in JSON, reset title to show welcome screen
            hymn_to_find = None

    # 4. Final Context
    context = {
        'all_hymns': all_data,           # Always needed for sidebar
        'hymn_title': hymn_to_find,      # If None, template shows Welcome Screen
        'tune': tune,
        'key_signature': key_sig,
        'xml_data': xml_content,
        'progression_json': json.dumps(music_is),
    }
    
    return render(request, 'choir/home.html', context)


import os
import base64
from django.shortcuts import render

def homes(request):
    xml_folder = r"C:\Users\Asamoah\Desktop\kofi\tunes"
    
    # 1. Get the list of files for the sidebar
    all_hymn_files = []
    if os.path.exists(xml_folder):
        all_hymn_files = [f for f in os.listdir(xml_folder) if f.lower().endswith(('.xml', '.musicxml'))]
        all_hymn_files.sort()
    
    hymn_filename = request.GET.get('hymn') 
    xml_base64 = "" 
    hymn_display_title = ""

    # 2. If a hymn is selected, encode it
    if hymn_filename:
        file_path = os.path.join(xml_folder, hymn_filename)
        if os.path.exists(file_path):
            hymn_display_title = hymn_filename.rsplit('.', 1)[0].replace('_', ' ').upper()
            try:
                with open(file_path, 'rb') as f: # Read as BINARY
                    raw_data = f.read()
                    # Convert binary data to a Base64 string
                    xml_base64 = base64.b64encode(raw_data).decode('utf-8')
            except Exception as e:
                print(f"Error encoding file: {e}")

    context = {
        'all_hymns': all_hymn_files,
        'selected_hymn_file': hymn_filename,
        'hymn_title': hymn_display_title,
        'xml_data_b64': xml_base64, 
    }
    return render(request, 'choir/home.html', context)





import base64
import re
from django.shortcuts import render

def homep(request):
    xml_path = r"C:\Users\Asamoah\Documents\Myriad Documents\PDFtoMusic\Export\773.xml"
    
    try:
        with open(xml_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()

        # THE FIX: Remove tags that cause the TempoExpressions crash
        # 1. Remove sound tempo attributes
        xml_content = re.sub(r'tempo="\d+"', '', xml_content)
        # 2. Remove metronome definitions entirely
        xml_content = re.sub(r'<metronome.*?>.*?</metronome>', '', xml_content, flags=re.DOTALL)
        # 3. Remove direction-type words that might be interpreted as tempo
        xml_content = re.sub(r'<direction-type>\s*<metronome.*?</direction-type>', '', xml_content, flags=re.DOTALL)
        
        encoded_string = base64.b64encode(xml_content.encode('utf-8')).decode('utf-8')
    except Exception as e:
        encoded_string = ""
        print(f"File Error: {e}")
    
    return render(request, 'choir/home.html', {'xml_data_b64': encoded_string})




def home1(request):
    xml_folder = r"C:\Users\Asamoah\Desktop\kofi\tunes"
    
    all_hymn_data = [] # List of dictionaries
    if os.path.exists(xml_folder):
        filenames = [f for f in os.listdir(xml_folder) if f.lower().endswith(('.xml', '.musicxml'))]
        filenames.sort()
        
        for f in filenames:
            all_hymn_data.append({
                'filename': f,
                'display_name': f.rsplit('.', 1)[0].replace('_', ' ').upper()
            })
    
    hymn_filename = request.GET.get('hymn') 
    xml_base64 = "" 
    hymn_display_title = ""

    if hymn_filename:
        safe_filename = os.path.basename(hymn_filename)
        file_path = os.path.join(xml_folder, safe_filename)
        
        if os.path.exists(file_path):
            hymn_display_title = safe_filename.rsplit('.', 1)[0].replace('_', ' ').upper()
            try:
                with open(file_path, 'rb') as f:
                    xml_base64 = base64.b64encode(f.read()).decode('utf-8')
            except Exception as e:
                print(f"Error: {e}")

    context = {
        'all_hymns': all_hymn_data, # Now passing a list of dicts
        'selected_hymn_file': hymn_filename,
        'hymn_title': hymn_display_title,
        'xml_data_b64': xml_base64, 
    }
    return render(request, 'choir/home.html', context)



import os
import base64
import xml.etree.ElementTree as ET
from django.shortcuts import render

def homen(request):
    xml_folder = r"C:\Users\Asamoah\Desktop\kofi\tunes"
    all_hymn_data = []

    if os.path.exists(xml_folder):
        filenames = [f for f in os.listdir(xml_folder) if f.lower().endswith(('.xml', '.musicxml'))]
        filenames.sort()
        
        for f in filenames:
            file_path = os.path.join(xml_folder, f)
            hymn_info = {
                'filename': f,
                'display_name': f.rsplit('.', 1)[0].replace('_', ' ').upper(),
                'key': "Unknown Key",
                'tune': "Standard"
            }

            # QUICK PARSE: Extract Key and Tune from the XML
            try:
                tree = ET.parse(file_path)
                root = tree.getroot()
                
                # Find Key Signature (fifths)
                fifths = root.find(".//fifths")
                if fifths is not None:
                    # Basic mapping of fifths to Key names
                    key_map = {
                        '0': 'C Maj', '1': 'G Maj', '2': 'D Maj', '3': 'A Maj', '4': 'E Maj', '5': 'B Maj', 
                        '-1': 'F Maj', '-2': 'Bb Maj', '-3': 'Eb Maj', '-4': 'Ab Maj', '-5': 'Db Maj'
                    }
                    hymn_info['key'] = key_map.get(fifths.text, f"Key: {fifths.text}")

                # Find Tune/Work Title
                work_title = root.find(".//work-title")
                if work_title is not None and work_title.text:
                    hymn_info['tune'] = work_title.text.strip()

            except Exception:
                pass # Fallback to defaults if file is messy
            
            all_hymn_data.append(hymn_info)
    
    # Selection Logic
    hymn_filename = request.GET.get('hymn') 
    xml_base64 = "" 
    hymn_display_title = ""

    if hymn_filename:
        safe_filename = os.path.basename(hymn_filename)
        selected_path = os.path.join(xml_folder, safe_filename)
        
        if os.path.exists(selected_path):
            hymn_display_title = safe_filename.rsplit('.', 1)[0].replace('_', ' ').upper()
            try:
                with open(selected_path, 'rb') as f:
                    xml_base64 = base64.b64encode(f.read()).decode('utf-8')
            except Exception as e:
                print(f"Error: {e}")

    context = {
        'all_hymns': all_hymn_data,
        'selected_hymn_file': hymn_filename,
        'hymn_title': hymn_display_title,
        'xml_data_b64': xml_base64, 
    }
    return render(request, 'choir/home.html', context)




from django.shortcuts import render
from music21 import converter, chord, note
import json

def home_(request):
    # Path to your uploaded file
    file_path = "C:\\Users\\Asamoah\\Desktop\\kofi\\tunes\\ang3.xml"
    score = converter.parse(file_path)
    
    # Use chordify to get vertical harmonies and rests
    chorded_score = score.chordify()
    
    musical_events = []
    current_time = 0 # Cumulative time in seconds
    tempo = 115 # Based on ang3.xml metadata
    quarter_note_duration = 60 / tempo

    for element in chorded_score.recurse().getElementsByClass(['Chord', 'Rest']):
        # Convert quarterLength duration to seconds
        duration_sec = element.duration.quarterLength * quarter_note_duration
        
        event = {
            "time": current_time,
            "duration": duration_sec,
            "pitches": []
        }
        
        if isinstance(element, chord.Chord):
            # Extract pitch names with octaves (e.g., "C4")
            event["pitches"] = [p.nameWithOctave for p in element.pitches]
        
        # Add to timeline and increment time (even for rests)
        musical_events.append(event)
        current_time += duration_sec

    return render(request, 'choir/home.html', {
        'song_data': json.dumps(musical_events)
    })







from django.shortcuts import render
from music21 import converter, chord, note
import json

def home_good(request):
    # Path to the MusicXML file provided
    file_path = "C:\\Users\\Asamoah\\Desktop\\kofi\\tunes\\mhb356.xml"
    score = converter.parse(file_path)
    chorded_score = score.chordify()
    
    tempo = 115 # From ang3.xml metadata
    qn_duration = 60 / tempo
    
    musical_timeline = []
    
    # Iterate through every vertical slice of the music
    for i, element in enumerate(chorded_score.recurse().getElementsByClass(['Chord', 'Rest'])):
        event = {
            "id": i,
            "measure": element.measureNumber,
            "duration": element.duration.quarterLength * qn_duration,
            "display_name": "",
            "pitches": []
        }
        
        if isinstance(element, chord.Chord):
            event["pitches"] = [p.nameWithOctave for p in element.pitches]
            # Create a readable name for the UI, e.g., "C4, E4, G4"
            event["display_name"] = ", ".join([p.name for p in element.pitches])
        else:
            event["display_name"] = "Rest (Silence)"
            
        musical_timeline.append(event)

    return render(request, 'choir/home.html', {
        'timeline_json': json.dumps(musical_timeline),
        'timeline_list': musical_timeline
    })



import os
import json
from django.shortcuts import render
from music21 import converter, chord, note

def homer(request):
    # Path to your resources
    tunes_path = r"C:\\Users\\Asamoah\\Desktop\\kofi\\tunes"
    json_path = "C:\\Users\\Asamoah\\Desktop\\kofi\\aseda_a\\adom\\static\\hymns.json" # Ensure this is in your project root or accessible path
    
    # 1. Load Sidebar Data from JSON (Very Fast)
    with open(json_path, 'r', encoding='utf-8') as f:
        sidebar_songs = json.load(f)

    # 2. Handle Song Selection
    selected_song_id = request.GET.get('song')
    current_song_data = None
    selected_meta = None

    if selected_song_id:
        # Construct the XML filename (assuming filename matches title in JSON)
        # For example: "mhb105.xml"
        xml_filename = f"{selected_song_id}.xml"
        file_full_path = os.path.join(tunes_path, xml_filename)
        
        if os.path.exists(file_full_path):
            try:
                # Parse ONLY the selected XML file
                score = converter.parse(file_full_path)
                chorded = score.chordify()
                
                # Extract Chords, Rests, and Durations for playback
                current_song_data = []
                tempo = 115 
                multiplier = 60 / tempo
                
                for element in chorded.recurse().getElementsByClass(['Chord', 'Rest']):
                    event = {
                        "measure": element.measureNumber,
                        "duration": element.duration.quarterLength * multiplier,
                        "pitches": [p.nameWithOctave for p in element.pitches] if isinstance(element, chord.Chord) else [],
                        "display": element.commonName if isinstance(element, chord.Chord) else "Rest"
                    }
                    current_song_data.append(event)
                
                # Find metadata in the JSON list to display title/key
                selected_meta = next((s for s in sidebar_songs if s['title'] == selected_song_id), None)
            except Exception as e:
                print(f"Error parsing {xml_filename}: {e}")

    return render(request, 'choir/home.html', {
        'songs': sidebar_songs,
        'current_song_json': json.dumps(current_song_data),
        'selected_song': selected_meta
    })





import os
import json
from django.shortcuts import render
from music21 import converter, chord, note

def homez(request):
    tunes_path = r"C:\\Users\\Asamoah\\Desktop\\kofi\\tunes"
    json_path = "C:\\Users\\Asamoah\\Desktop\\kofi\\aseda_a\\adom\\static\\hymns.json"
    
    with open(json_path, 'r', encoding='utf-8') as f:
        sidebar_songs = json.load(f)

    selected_song_id = request.GET.get('song')
    current_timeline = []
    selected_meta = None

    if selected_song_id:
        xml_filename = f"{selected_song_id}.xml"
        file_full_path = os.path.join(tunes_path, xml_filename)
        
        if os.path.exists(file_full_path):
            try:
                score = converter.parse(file_full_path)
                chorded = score.chordify()
                
                tempo = 115 
                multiplier = 60 / tempo
                
                for i, element in enumerate(chorded.recurse().getElementsByClass(['Chord', 'Rest'])):
                    event = {
                        "id": i,
                        "measure": element.measureNumber,
                        "duration": element.duration.quarterLength * multiplier,
                        "pitches": [],
                        "display_name": ""
                    }
                    
                    if isinstance(element, chord.Chord):
                        # Get pitch names with octaves: ['C4', 'E4', 'G4']
                        pitch_list = [p.nameWithOctave for p in element.pitches]
                        event["pitches"] = pitch_list
                        # Display them as a string: "C4, E4, G4"
                        event["display_name"] = ", ".join(pitch_list)
                    else:
                        event["display_name"] = "Rest (Silence)"
                        
                    current_timeline.append(event)
                
                selected_meta = next((s for s in sidebar_songs if s['title'] == selected_song_id), None)
            except Exception as e:
                print(f"Error: {e}")

    return render(request, 'choir/home.html', {
        'songs': sidebar_songs,
        'timeline_json': json.dumps(current_timeline),
        'timeline_list': current_timeline,
        'selected_song': selected_meta
    })




import os
import json
from django.shortcuts import render
from music21 import converter, chord, note

def homed(request):
    tunes_path = r"C:\Users\Asamoah\Desktop\kofi\tunes"
    json_path = "C:\\Users\\Asamoah\\Desktop\\kofi\\aseda_a\\adom\\static\\hymns.json"
    
    # Load Sidebar from JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        sidebar_songs = json.load(f)

    selected_song_id = request.GET.get('song')
    current_timeline = []
    selected_meta = None

    if selected_song_id:
        xml_filename = f"{selected_song_id}.xml"
        file_full_path = os.path.join(tunes_path, xml_filename)
        
        if os.path.exists(file_full_path):
            try:
                score = converter.parse(file_full_path)
                chorded = score.chordify()
                
                tempo = 115 
                multiplier = 60 / tempo
                
                for i, element in enumerate(chorded.recurse().getElementsByClass(['Chord', 'Rest'])):
                    event = {
                        "id": i,
                        "measure": element.measureNumber,
                        "duration": element.duration.quarterLength * multiplier,
                        "pitches": [p.nameWithOctave for p in element.pitches] if isinstance(element, chord.Chord) else [],
                        "display_name": ", ".join([p.nameWithOctave for p in element.pitches]) if isinstance(element, chord.Chord) else "Rest (Silence)"
                    }
                    current_timeline.append(event)
                
                selected_meta = next((s for s in sidebar_songs if s['title'] == selected_song_id), None)
            except Exception as e:
                print(f"Error: {e}")

    return render(request, 'choir/home.html', {
        'songs': sidebar_songs,
        'timeline_json': json.dumps(current_timeline),
        'timeline_list': current_timeline,
        'selected_song': selected_meta
    })




def homee(request):
    tunes_path = r"C:\Users\Asamoah\Desktop\kofi\tunes"
    json_path = "C:\\Users\\Asamoah\\Desktop\\kofi\\aseda_a\\adom\\static\\hymns.json"
    
    with open(json_path, 'r', encoding='utf-8') as f:
        sidebar_songs = json.load(f)

    selected_song_id = request.GET.get('song')
    current_timeline = []
    selected_meta = None
    xml_content = "" # 1. Initialize an empty string for the XML

    if selected_song_id:
        xml_filename = f"{selected_song_id}.xml"
        file_full_path = os.path.join(tunes_path, xml_filename)
        
        if os.path.exists(file_full_path):
            # 2. READ THE RAW XML CONTENT FOR OSMD
            with open(file_full_path, 'r', encoding='utf-8') as f:
                xml_content = f.read()

            try:
                score = converter.parse(file_full_path)
                chorded = score.chordify()
                
                tempo = 115 
                multiplier = 60 / tempo
                
                for i, element in enumerate(chorded.recurse().getElementsByClass(['Chord', 'Rest'])):
                    event = {
                        "id": i,
                        "measure": element.measureNumber,
                        "duration": element.duration.quarterLength * multiplier,
                        "pitches": [p.nameWithOctave for p in element.pitches] if isinstance(element, chord.Chord) else [],
                        "display_name": ", ".join([p.nameWithOctave for p in element.pitches]) if isinstance(element, chord.Chord) else "Rest (Silence)"
                    }
                    current_timeline.append(event)
                
                selected_meta = next((s for s in sidebar_songs if s['title'] == selected_song_id), None)
            except Exception as e:
                print(f"Error: {e}")

    return render(request, 'choir/home.html', {
        'songs': sidebar_songs,
        'timeline_json': json.dumps(current_timeline),
        'timeline_list': current_timeline,
        'selected_song': selected_meta,
        'xml_data': xml_content  # 3. Pass the string to the template
    })





import os
import json
from django.shortcuts import render
from django.contrib.staticfiles import finders # Import this to find static files
from music21 import converter, chord

def homez(request):
    # 1. Update paths to point to your static folder
    # Assuming your files are in: static/tunes/
    json_static_path = "hymns_cleaned.json" # Relative path within static
    
    # Use finders to get the absolute path of the JSON
    json_full_path = finders.find(json_static_path)
    
    sidebar_songs = []
    if json_full_path and os.path.exists(json_full_path):
        with open(json_full_path, 'r', encoding='utf-8') as f:
            sidebar_songs = json.load(f)

    selected_song_id = request.GET.get('song')
    current_timeline = []
    selected_meta = None
    xml_content = "" 

    if selected_song_id:
        # 2. Look for the XML in static/tunes/
        xml_static_path = f"tunes/{selected_song_id}.xml"
        file_full_path = finders.find(xml_static_path)
        
        if file_full_path and os.path.exists(file_full_path):
            # Read the raw XML content for the OSMD display
            with open(file_full_path, 'r', encoding='utf-8') as f:
                xml_content = f.read()

            try:
                # Use music21 to parse for the player logic
                score = converter.parse(file_full_path)
                chorded = score.chordify()
                
                tempo = 115 
                multiplier = 60 / tempo
                
                for i, element in enumerate(chorded.recurse().getElementsByClass(['Chord', 'Rest'])):
                    event = {
                        "id": i,
                        "measure": element.measureNumber,
                        "duration": element.duration.quarterLength * multiplier,
                        "pitches": [p.nameWithOctave for p in element.pitches] if isinstance(element, chord.Chord) else [],
                        "display_name": ", ".join([p.nameWithOctave for p in element.pitches]) if isinstance(element, chord.Chord) else "Rest (Silence)"
                    }
                    current_timeline.append(event)
                
                selected_meta = next((s for s in sidebar_songs if s['title'] == selected_song_id), None)
            except Exception as e:
                print(f"Error parsing music21: {e}")

    return render(request, 'choir/home.html', {
        'songs': sidebar_songs,
        'timeline_json': json.dumps(current_timeline),
        'timeline_list': current_timeline,
        'selected_song': selected_meta,
        'xml_data': xml_content # This sends the notation data to the HTML
    })





import os
import json
from django.shortcuts import render
from django.conf import settings
from music21 import converter, chord

def home(request):
    # 1. Use settings.BASE_DIR to find files on the server disk
    # This assumes your files are inside your project's 'static' folder
    static_root = os.path.join(settings.BASE_DIR, 'static')
    json_full_path = os.path.join(static_root, 'hymns_cleaned.json')
    
    sidebar_songs = []
    
    # 2. Load the JSON data for the sidebar
    if os.path.exists(json_full_path):
        try:
            with open(json_full_path, 'r', encoding='utf-8') as f:
                sidebar_songs = json.load(f)
        except Exception as e:
            print(f"Error reading JSON file: {e}")
    else:
        # This will show up in your PythonAnywhere server logs
        print(f"File not found: {json_full_path}")

    selected_song_id = request.GET.get('song')
    current_timeline = []
    selected_meta = None
    xml_content = "" 

    if selected_song_id:
        # 3. Construct path for the specific XML file
        xml_full_path = os.path.join(static_root, 'tunes', f"{selected_song_id}.xml")
        
        if os.path.exists(xml_full_path):
            # Read raw XML for OpenSheetMusicDisplay (OSMD)
            try:
                with open(xml_full_path, 'r', encoding='utf-8') as f:
                    xml_content = f.read()

                # 4. Use music21 to parse for the player logic
                score = converter.parse(xml_full_path)
                chorded = score.chordify()
                
                tempo = 115 
                multiplier = 60 / tempo
                
                for i, element in enumerate(chorded.recurse().getElementsByClass(['Chord', 'Rest'])):
                    event = {
                        "id": i,
                        "measure": element.measureNumber,
                        "duration": element.duration.quarterLength * multiplier,
                        "pitches": [p.nameWithOctave for p in element.pitches] if isinstance(element, chord.Chord) else [],
                        "display_name": ", ".join([p.nameWithOctave for p in element.pitches]) if isinstance(element, chord.Chord) else "Rest (Silence)"
                    }
                    current_timeline.append(event)
                
                # Find metadata in the loaded sidebar_songs list
                selected_meta = next((s for s in sidebar_songs if s.get('title') == selected_song_id), None)
                
            except Exception as e:
                print(f"Error parsing music21 or reading XML: {e}")
        else:
            print(f"XML file not found: {xml_full_path}")

    return render(request, 'choir/home.html', {
        'songs': sidebar_songs,
        'timeline_json': json.dumps(current_timeline),
        'timeline_list': current_timeline,
        'selected_song': selected_meta,
        'xml_data': xml_content
    })