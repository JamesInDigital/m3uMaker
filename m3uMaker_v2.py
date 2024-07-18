import os
import re
import shutil

def find_multi_disc_identifier(file_name):
    multi_disc_identifiers = ['diskside', 'discside', 'disc', 'disk']
    for identifier in multi_disc_identifiers:
        if identifier.lower() in file_name.lower():
            return identifier

    match = re.search(r'[-(](?:\s*)disc(?:\s*)(\d+)[)-]', file_name, re.IGNORECASE)
    if match:
        return f"disc{match.group(1)}"
    
    return None

def find_diskside_identifier(file_name):
    diskside_match = re.search(r'diskside(\d+)', file_name, re.IGNORECASE)
    if diskside_match:
        return "diskside"

    diskside_match_space = re.search(r'diskside\s*(\d+)', file_name, re.IGNORECASE)
    if diskside_match_space:
        return "diskside"
    
    return None

def separate_games(folder_path):
    multi_disc_games = {}
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if os.path.splitext(file)[1].lower() in ['.7z', '.chd', '.zip', '.cue', '.pbp', '.dsk']:
                multi_disc_identifier = find_multi_disc_identifier(file)
                diskside_identifier = find_diskside_identifier(file)

                if multi_disc_identifier or diskside_identifier:
                    if root not in multi_disc_games:
                        multi_disc_games[root] = []
                    multi_disc_games[root].append(os.path.join(root, file))
    
    return multi_disc_games

def m3u_multi(parent_directory, multi_disc_games):
    for folder, files in multi_disc_games.items():
        grouped_games = {}
        
        for game_path in files:
            folder_name, file_name = os.path.split(game_path)
            identifier = find_multi_disc_identifier(file_name)
            if identifier == "diskside":
                base_name, _ = os.path.splitext(file_name)
            else:
                base_name, extension = os.path.splitext(re.sub(r'\(.*\)|\[.*\]', '', file_name).strip())
                last_hyphen_index = base_name.rfind('- ')
                if last_hyphen_index != -1:
                    base_name = base_name[:last_hyphen_index].strip()
            
            if base_name not in grouped_games:
                grouped_games[base_name] = {'identifier': identifier, 'files': []}
            grouped_games[base_name]['files'].append(game_path)

        hidden_folder_path = os.path.join(folder, ".hidden")
        if not os.path.exists(hidden_folder_path):
            os.makedirs(hidden_folder_path)
        
        for base_name, data in grouped_games.items():
            m3u_file_path = os.path.join(folder, f"{base_name}.m3u")
            with open(m3u_file_path, 'w', newline='\n') as m3u_file:
                for file_path in data['files']:
                    dest_path = os.path.join(hidden_folder_path, os.path.basename(file_path))
                    shutil.move(file_path, dest_path)
                    m3u_file.write(f".hidden/{os.path.basename(dest_path).replace(os.sep, '/').replace(' /', '/ ')}\n")

if __name__ == "__main__":
    current_directory = os.getcwd()
    multi_disc_games = separate_games(current_directory)
    
    m3u_multi(current_directory, multi_disc_games)
