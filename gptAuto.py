import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
from multiprocessing import Pool, cpu_count

# Scans Directories
source_dir = r"C:\Users\honde\Downloads"  # Specify the source directory to monitor
dest_dir_base = r"C:\Users\honde\Downloads"  # Base directory for organizing files
dest_dir_mapping = {
    # Document Extensions
    '.pdf': 'docs',
    '.ppt': 'docs',
    '.pptx': 'docs',
    '.xls': 'docs',
    '.xlsx': 'docs',
    '.csv': 'docs',
    '.doc': 'docs',
    '.docx': 'docs',
    '.rtf': 'docs',
    '.accdb': 'docs',
    '.mdb': 'docs',
    '.vsd': 'docs',

    # Picture Extensions
    '.jpg': 'pics',
    '.jpeg': 'pics',
    '.png': 'pics',
    '.gif': 'pics',
    '.bmp': 'pics',
    '.tiff': 'pics',
    '.webp': 'pics',
    '.PNG': 'pics',

    # Archive Extensions
    '.zip': 'archives',
    '.rar': 'archives',
    '.7z': 'archives',
    '.tar': 'archives',
    '.gz': 'archives',
    '.bz2': 'archives',

    # Sound/Video Extensions
    '.mp3': 'soundANDvid',
    '.wav': 'soundANDvid',
    '.mp4': 'soundANDvid',
    '.avi': 'soundANDvid',
    '.mkv': 'soundANDvid',
    '.mov': 'soundANDvid',
    '.flv': 'soundANDvid',

}  # Define a mapping for file extensions to destination directories


def move(dest, entry, name):
    try:
        # Create the destination folder and ensure it exists
        destination_folder = os.path.join(dest_dir_base, dest)
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        destination_file = os.path.join(destination_folder, name)
        counter = 1

        # Handle file name collisions by appending a counter
        while os.path.exists(destination_file):
            filename, extension = os.path.splitext(name)
            new_name = f"{filename}({counter}){extension}"
            destination_file = os.path.join(destination_folder, new_name)
            counter += 1

        # Move the file to the destination
        shutil.move(entry, destination_file)
        print(f"Moved: {name} to {destination_file}")
    except (IOError, OSError) as e:
        # Handle file-related errors, e.g., log or report them
        logging.error(f"Error while processing {name}: {e}")


class MoveHandler(FileSystemEventHandler):
    def __init__(self, pool):
        super().__init__()
        self.pool = pool

    def on_created(self, event):
        # Process a newly created file using multiprocessing
        name = os.path.basename(event.src_path)
        extension = os.path.splitext(name)[1]
        if extension in ('.crdownload', '.part', '.tmp'):
            return
        dest = dest_dir_mapping.get(extension, 'other')
        self.pool.apply_async(move, (dest, event.src_path, name))
        print(f"Processing: {name} to {dest_dir_base}/{dest}/{name}")


def organize_existing_files():
    # Organize existing files in the source directory
    for filename in os.listdir(source_dir):
        extension = os.path.splitext(filename)[1]
        if extension in ('.crdownload', '.part', '.tmp'):
            return
        if os.path.isfile(os.path.join(source_dir, filename)):
            dest = dest_dir_mapping.get(extension, 'other')
            source_file = os.path.join(source_dir, filename)
            move(dest, source_file, filename)


if __name__ == "__main__":
    # Organize existing files when the script is first executed
    organize_existing_files()

    # Configure logging for the script
    logging.basicConfig(level=logging.DEBUG,  # Set to DEBUG for more detailed logging
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    path = source_dir  # Specify the source directory
    event_handler = MoveHandler(Pool(cpu_count()))  # Create a handler for file events
    observer = Observer()  # Create an observer for monitoring the directory
    observer.schedule(event_handler, path, recursive=False)  # Set up the observer with recursive=False
    observer.start()  # Start monitoring

    try:
        while True:
            time.sleep(600)  # Monitor for changes every 10 minutes
    except KeyboardInterrupt:
        # Handle a user interruption (e.g., Ctrl+C)
        observer.stop()
        observer.join()
        event_handler.pool.close()
        event_handler.pool.join()
