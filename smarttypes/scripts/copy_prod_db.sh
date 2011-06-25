
ssh cottie "/opt/mongodb/bin/mongodump --db smarttypes --out smarttypes_dump"
scp -Cr cottie:/home/timmyt/smarttypes_dump /home/timmyt/projects/smarttypes/smarttypes/backups/smarttypes_`/bin/date +"%Y_%m_%d"`
/opt/mongodb/bin/mongorestore --db smarttypes --drop /home/timmyt/projects/smarttypes/smarttypes/backups/smarttypes_`/bin/date +"%Y_%m_%d"`/smarttypes/

