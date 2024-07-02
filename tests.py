# Testing
# 1. setUp -> Create a temporary dir for src and replica
# 2. rm_temp_dirs -> Remove temporary dir after test
# 3. test_create_replica_folder -> If replica folder doesnt exist ensure that is created
# 4. test_copy_new_files -> Verify is files in src are copied to replica
# 5. test_remove_files_not_in_src -> Verify if files that dont exist in src are removed from replica
# 6. test_sync_recursive -> Verify if the subsirs are being sync
# 7. test_update_changed_files -> Verify that changed files in src are being updated in replica

import unittest
import tempfile
import os
import shutil
import filecmp
from sync_script import sync_folders

class TestSyncFolders(unittest.TestCase):

    def setUp(self):
        self.src = tempfile.mkdtemp()
        self.replica = tempfile.mkdtemp()

    def rm_temp_dirs(self):
        shutil.rmtree(self.src)
        shutil.rmtree(self.replica)

    def test_create_replica_folder(self):
        shutil.rmtree(self.replica)
        sync_folders(self.src, self.replica)
        self.assertTrue(os.path.exists(self.replica))
        self.assertEqual(os.listdir(self.replica), [])

    def test_copy_new_files(self):
        with open(os.path.join(self.src, 'test.txt'), 'w') as f:
            f.write('This is a test file.')

        sync_folders(self.src, self.replica)
        self.assertTrue(filecmp.cmp(os.path.join(self.src, 'test.txt'), os.path.join(self.replica, 'test.txt')))

    def test_remove_files_not_in_src(self):
        with open(os.path.join(self.replica, 'old_file.txt'), 'w') as f:
            f.write('This file should be removed.')

        sync_folders(self.src, self.replica)
        self.assertFalse(os.path.exists(os.path.join(self.replica, 'old_file.txt')))

    def test_sync_recursive(self):
        os.mkdir(os.path.join(self.src, 'subdir'))
        with open(os.path.join(self.src, 'subdir', 'subfile.txt'), 'w') as f:
            f.write('This is a test file in a subdir.')

        sync_folders(self.src, self.replica)
        self.assertTrue(os.path.isdir(os.path.join(self.replica, 'subdir')))
        self.assertTrue(filecmp.cmp(os.path.join(self.src, 'subdir', 'subfile.txt'), os.path.join(self.replica, 'subdir', 'subfile.txt')))

    def test_update_changed_files(self):
        with open(os.path.join(self.src, 'test.txt'), 'w') as f:
            f.write('Original content.')

        sync_folders(self.src, self.replica)

        with open(os.path.join(self.src, 'test.txt'), 'w') as f:
            f.write('Updated content.')

        sync_folders(self.src, self.replica)
        self.assertTrue(filecmp.cmp(os.path.join(self.src, 'test.txt'), os.path.join(self.replica, 'test.txt')))

if __name__ == '__main__':
    unittest.main()
