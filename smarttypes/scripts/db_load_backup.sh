#!/bin/bash

dropdb smarttypes
createdb smarttypes
createlang plpgsql smarttypes
zcat $1 | psql smarttypes 

