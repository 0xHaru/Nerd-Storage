## Examples

| /            |     | directory_1/ |
| ------------ | --- | ------------ |
|              |     |              |
| ..           |     | ..           |
| directory_1/ |     | directory_2/ |
| file_1.txt   |     | file_2.txt   |

### Commands

1. List directory content of `/`: `nerdcli`

2. Login: `nerdcli --login`

3. Logout: `nerdcli --logout`

4. List directory content of `directory_2/`: `nerdcli --ls directory_1/directory_2`

5. Download `file_1.txt`: `nerdcli --download file_1.txt`

6. Make a sub-directory inside of `directory_1`: `nerdcli --mkdir directory_1/new_directory`

7. Upload a file to `/`: `nerdcli --upload / /path/to/file`

8. Upload a .zip as a directory to `directory_1`: `nerdcli --upload-dir directory_1 /path/to/file.zip`

9. Delete `file_2.txt`: `nerdcli --delete directory_1/file_2.txt`
