

sudo docker build -t harbor.zenith-bio.com:5000/dev/ocr_recognition:2025070801 -f  ./docker/Dockerfile-python-web .
sudo docker push jiedu.zenith-bio.com:5000/dev/ocr_recognition:2025070801

docker run  --name=ocr -d -p 8080:8080 harbor.zenith-bio.com:5000/dev/ocr_recognition:2025070801 