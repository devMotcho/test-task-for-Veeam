# 1. Verify if dir replica exists, if not it is created.
# 2. List all items in src dir
# 3. List all items in replica dir
# 4. Get path of each item in src and replica dir
# 5. Check if the item is a dir
# 6. If is a dir use sync_folders as a recursive func
# 7. If is a file perform a deep comparation and copy the modified files from src to replica
# 8. Remove files at replica that dont exist in src
# 9. While True call the sync_folders func at a interval
# 10. Add logging configuration to keep track of the operations to a file and to the console
# 11. Create a main function that allows user to provide folder paths, interval and log file path via command line args

import os
import shutil
import filecmp
import time
import logging
import argparse

# logging config
def configure_logging(log_file):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler(log_file),
                            logging.StreamHandler()
                        ])


def sync_folders(src, replica):
    
    if not os.path.exists(replica):
        os.makedirs(replica)
        logging.info(f'Create: {replica} folder')
    
    src_files = os.listdir(src)
    replica_files = os.listdir(replica)


    for item in src_files:
        # get the path for each item in the folder
        src_path = os.path.join(src, item)
        replica_path = os.path.join(replica, item)

        if os.path.isdir(src_path):
            # if is dir use sync_folders recursively
            sync_folders(src_path, replica_path)
        else:
            if item not in replica_files or not filecmp.cmp(src_path, replica_path, shallow=False):
                shutil.copy2(src_path, replica_path)
                logging.info(f'Copied: {src_path} to {replica_path}')
            
    
    # Remove files from replica that doesn't exist in src
    for item in replica_files:
        if item not in src_files:
            replica_path = os.path.join(replica, item)
            if os.path.isdir(replica_path):
                shutil.rmtree(replica_path)
            else:
                os.remove(replica_path)
            logging.info(f'Removed: {replica_path}')
   
def periodic_sync(src, replica, interval):
    while True:
        sync_folders(src, replica)
        time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(description="Sync two folders periodically.")
    parser.add_argument('src', type=str, help='Source folder path.')
    parser.add_argument('replica', type=str, help='Replica folder path.')
    parser.add_argument('interval', type=int, help='Sync interval (seconds)')
    parser.add_argument('log_file', type=str, help='Log file path')

    args = parser.parse_args()

    configure_logging(args.log_file)

    periodic_sync(args.src, args.replica, args.interval)

if __name__ == '__main__':
    main()

# python sync_script.py ./src ./replica 10 ./logfile.log
