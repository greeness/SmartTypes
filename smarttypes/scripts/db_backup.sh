#!/bin/bash

ssh cottie "pg_dump smarttypes | gzip > /tmp/dump.gz"
scp cottie:/tmp/dump.gz /home/timmyt/projects/smarttypes/smarttypes/backups/dump.`/bin/date +"%Y_%m_%d"`.gz
ssh cottie "rm /tmp/dump.gz"


#ssh cottie "/opt/mongodb/bin/mongodump --db smarttypes --out smarttypes_dump"
#scp -Cr cottie:/home/timmyt/smarttypes_dump /home/timmyt/projects/smarttypes/smarttypes/backups/smarttypes_`/bin/date +"%Y_%m_%d"`
#/opt/mongodb/bin/mongorestore --db smarttypes --drop /home/timmyt/projects/smarttypes/smarttypes/backups/smarttypes_`/bin/date +"%Y_%m_%d"`/smarttypes/

