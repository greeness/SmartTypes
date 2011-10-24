
rsync -ra --stats --delete \
--exclude-from '/home/timmyt/projects/smarttypes/smarttypes/scripts/exclude_from_github.txt' \
/home/timmyt/projects/smarttypes/smarttypes/ \
/home/timmyt/projects/smarttypes_github/smarttypes/

cp /home/timmyt/projects/smarttypes/README /home/timmyt/projects/smarttypes_github/README

cp /home/timmyt/projects/smarttypes/smarttypes/config.py.blank /home/timmyt/projects/smarttypes_github/smarttypes/config.py
