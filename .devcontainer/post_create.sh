
KEY=./key

if [ ! -f ${KEY} ]; then
    echo 'Create dummy key file'
    echo 'tivi_mac=AA:BB:CC:DD:EE:FF' >> ${KEY}
else
    echo 'key file found ...'
fi

curl -o mapping.py https://raw.githubusercontent.com/harrygg/plugin.program.tvbgpvr.backend/master/resources/lib/mapping.py

pip install -r requirements.txt
