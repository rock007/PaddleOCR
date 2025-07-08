

sudo docker build -t harbor.zenith-bio.com:5000/dev/ocr_recognition:2025070701 -f  ./docker/Dockerfile-python-web .
sudo docker push jiedu.zenith-bio.com:5000/dev/ocr_recognition:2024050101

docker run  --name=ocr -d -p 10080:8080 harbor.zenith-bio.com:5000/dev/ocr_recognition:2025070701 