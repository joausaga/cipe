#!/bin/bash
# cleanup 
docker-compose -f docker-compose.prod.yml  down -v --rmi all --remove-orphans
# remove mysql 
echo ""
echo "Don't forget to remove volume ./mysql directory with"
echo "sudo rm -rf ./mysql"
sleep 1
echo "Your docker images: "
# list remaining images
docker images
echo ""
echo "If you see dangling images you can clean them up by running"
echo "docker system prune"

