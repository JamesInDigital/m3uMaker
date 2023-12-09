import os
import re

def find_multi_disc_identifier(file_name):
    # Check for multidisc identifiers in the file name
    multi_disc_identifiers = ['diskside', 'discside', 'disc', 'disk']
    for identifier in multi_disc_identifiers:
        if identifier.lower() in file_name.lower():
            return identifier

    # Check for multidisc patterns after a dash or within parentheses
    match = re.search(r'[-(](?:\s*)disc(?:\s*)(\d+)[)-]', file_name, re.IGNORECASE)
    if match:
        return f"disc{match.group(1)}"
    
    return None

def find_diskside_identifier(file_name):
    # Check for "diskside" followed by a number
    diskside_match = re.search(r'diskside(\d+)', file_name, re.IGNORECASE)
    if diskside_match:
        return "diskside"

    # Check for "diskside" followed by a space and a number
    diskside_match_space = re.search(r'diskside\s*(\d+)', file_name, re.IGNORECASE)
    if diskside_match_space:
        return "diskside"
    
    return None

def separate_games(folder_path):
    multi_disc_games = []
    single_disc_games = []
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if os.path.splitext(file)[1].lower() in ['.7z', '.chd', '.zip', '.cue', '.pbp', '.dsk']:
                multi_disc_identifier = find_multi_disc_identifier(file)
                diskside_identifier = find_diskside_identifier(file)

                if multi_disc_identifier or diskside_identifier:
                    multi_disc_games.append(os.path.join(root, file))
                else:
                    single_disc_games.append(os.path.join(root, file))
    
    return multi_disc_games, single_disc_games

def m3u_multi(parent_directory, multi_disc_games):
    grouped_games = {}
    
    for game_path in multi_disc_games:
        folder_name, file_name = os.path.split(game_path)
        identifier = find_multi_disc_identifier(file_name)
        if identifier == "diskside":
            base_name, _ = os.path.splitext(file_name)
        else:
            # Use hyphen followed by a space ("- ") as the split point
            base_name, extension = os.path.splitext(re.sub(r'\(.*\)|\[.*\]', '', file_name).strip())
            last_hyphen_index = base_name.rfind('- ')
            if last_hyphen_index != -1:
                base_name = base_name[:last_hyphen_index].strip()
        
        if base_name not in grouped_games:
            grouped_games[base_name] = {'identifier': identifier, 'files': []}
        grouped_games[base_name]['files'].append(game_path)
    
    for base_name, data in grouped_games.items():
        m3u_file_path = os.path.join(parent_directory, f"{base_name}.m3u")
        with open(m3u_file_path, 'w', newline='\n') as m3u_file:  # Set newline='\n' for Unix format
            for file_path in data['files']:
                m3u_file.write(f"./{file_path[len(parent_directory)+1:].replace(os.sep, '/').replace(' /', '/ ')}\n")  # Add preceding period and forward slash

def m3u_single(parent_directory, single_disc_games):
    for game_path in single_disc_games:
        folder_name, file_name = os.path.split(game_path)
        game_name = os.path.splitext(file_name)[0]
        m3u_file_path = os.path.join(parent_directory, f"{game_name}.m3u")
        with open(m3u_file_path, 'w', newline='\n') as m3u_file:  # Set newline='\n' for Unix format
            m3u_file.write(f"./{game_path[len(parent_directory)+1:].replace(os.sep, '/').replace(' /', '/ ')}\n")  # Add preceding period and forward slash

if __name__ == "__main__":
    current_directory = os.getcwd()
    multi_disc_games, single_disc_games = separate_games(current_directory)
    
    m3u_multi(current_directory, multi_disc_games)
    m3u_single(current_directory, single_disc_games)
