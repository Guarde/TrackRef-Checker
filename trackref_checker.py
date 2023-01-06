import os, json, time

def write(text:str):
    try:
        with open(os.path.join(dir, "trackRefs.txt"), mode="x", encoding="utf-8") as f:
            f.write(text)
    except FileExistsError:
        with open(os.path.join(dir, "trackRefs.txt"), mode="w", encoding="utf-8") as f:
            f.write(text)
    except:
        quit()


dir = os.getcwd()
trackrefs = []
tracktuple = []
errors = []
for folder in os.listdir(dir):
    subdir = os.path.join(dir, folder)
    try:
        if "song.tmb" in os.listdir(subdir):
            songfile = os.path.join(subdir, "song.tmb")
            shortpath = os.path.join(folder, "song.tmb")
            song = None
            with open(songfile, mode="r", encoding="utf-8") as f:
                try:
                    song = json.loads(f.read())
                except:
                    errors.append("Could not read song.tmb: " + shortpath)
                    continue
            if not "trackRef" in song.keys():
                errors.append("No trackRef found in song.tmb: " + shortpath)
                continue
            trackrefs.append(song["trackRef"])
            tracktuple.append((song["trackRef"], folder))
    except:
        continue
if len(trackrefs) == 0:
    write("No trackRefs found in current directory. Please place this script in your CustomSongs folder")
    quit()

doubles = {}
for ref in trackrefs:
    if trackrefs.count(ref) > 1:
        doubles[ref] = True

doubles = doubles.keys()
if len(doubles) == 0:
    write("No duplicates found. Congratulations!")
    quit()

results = {}
for tup in tracktuple:
    if tup[0] in doubles:
        try:
            results[tup[0]].append(tup[1])
        except:
            results[tup[0]] = [tup[1]]
output = ""
output += "The following duplicate trackRefs were discovered:"
for res in results.keys():    
    output +=  f"\n- trackRef \"{str(res)}\" used by :\n  - ./" + "\n  - ./".join(results[res]) + "\n"
if len(errors) > 0:
    output += "\nThe following errors were encountered while searching:\n- "
    output +=  "\n- ".join(errors)


write(output)

